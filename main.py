#!/usr/bin/env python3

import argparse
from pathlib import Path

import cv2
import numpy as np
from tqdm import tqdm

OUTPUT_MOVIE_FILE = Path("trex.webm")
FLOW_FRAMES_DIR = Path("flow_frames")
OUTPUT_FRAMES_DIR = Path("output_frames")


def generate_random_frame(width, height):
    """Generate a completely random RGB frame."""
    return np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)


def apply_flow_to_frame(frame, flow):
    """Apply optical flow vectors to warp a frame."""
    h, w = flow.shape[:2]

    # Create mesh grid
    flow_map = np.zeros((h, w, 2), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            flow_map[y, x, 0] = x
            flow_map[y, x, 1] = y

    # Add flow vectors to create remapping coordinates
    flow_map[:, :, 0] += flow[:, :, 0]
    flow_map[:, :, 1] += flow[:, :, 1]

    # Remap frame according to flow
    warped = cv2.remap(
        frame,
        flow_map[:, :, 0],
        flow_map[:, :, 1],
        cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )

    return warped


def generate_output_video(dimensions, fps, total_flows):
    """Generate output video by applying flow to evolving noise."""
    width, height = dimensions

    print("\nGenerating output frames...")

    OUTPUT_FRAMES_DIR.mkdir(exist_ok=True)

    # Generate initial random frame
    print("Generating initial random frame...")
    current_frame = generate_random_frame(width, height)

    # Save initial frame
    output_path = OUTPUT_FRAMES_DIR / "frame_000000.png"
    cv2.imwrite(str(output_path), current_frame)

    # Apply each flow field to evolve the noise
    for frame_idx in range(1, total_flows + 1):
        # Load flow field from disk
        flow_path = FLOW_FRAMES_DIR / f"flow_{frame_idx:06d}.npy"
        flow = np.load(flow_path)

        # Apply flow and get next frame
        current_frame = apply_flow_to_frame(current_frame, flow)

        # Save frame
        output_path = OUTPUT_FRAMES_DIR / f"frame_{frame_idx:06d}.png"
        cv2.imwrite(str(output_path), current_frame)

        if frame_idx % 10 == 0:
            print(f"  Generated frame {frame_idx}/{total_flows}")

    print(f"Generated {total_flows + 1} frames in {OUTPUT_FRAMES_DIR}/")


def create_final_video(dimensions, fps):
    """Assemble frames into final video."""
    width, height = dimensions

    print("\nAssembling final video...")

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*"VP80")  # VP8 codec for WebM
    out = cv2.VideoWriter(str(OUTPUT_MOVIE_FILE), fourcc, fps, (width, height))

    if not out.isOpened():
        raise RuntimeError(f"Failed to create video writer for {OUTPUT_MOVIE_FILE}")

    # Get all frame files
    frame_files = sorted(OUTPUT_FRAMES_DIR.glob("frame_*.png"))

    for frame_path in frame_files:
        frame = cv2.imread(str(frame_path))
        if frame is not None:
            out.write(frame)

    out.release()
    print(f"Final video saved: {OUTPUT_MOVIE_FILE}")
    print(f"Assembled {len(frame_files)} frames")


def cmd_extract_flow(args: argparse.Namespace):
    input_file = args.input
    output_dir = args.output
    if not output_dir:
        output_dir = input_file.parent / FLOW_FRAMES_DIR

    output_dir.mkdir(exist_ok=True)

    cap = cv2.VideoCapture(str(input_file))

    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {input_file}")

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Video: {width}x{height} @ {fps}fps, {frame_count} frames")

    # Read first frame
    ret, prev_frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read first frame")

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    for frame_idx in tqdm(range(1, frame_count + 1), desc="Extracting flow"):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute dense optical flow
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray,
            gray,
            None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
        )

        # Save flow field to disk (raw binary format)
        flow_path = output_dir / f"{frame_idx:06d}.npy"
        np.save(flow_path, flow)

        prev_gray = gray

    cap.release()
    total_flows = frame_count
    print(f"Extracted and saved {total_flows} flow fields to {output_dir}/")

    return (width, height), fps, total_flows


def cmd_generate_frames(args: argparse.Namespace):
    input_dir = args.flow_dir
    output_dir = args.output_dir
    if not output_dir:
        output_dir = input_dir.parent / OUTPUT_FRAMES_DIR
    output_dir.mkdir(exist_ok=True)

    # TODO


def cmd_assemble_video(args: argparse.Namespace):
    input_dir = args.frames_dir
    output_file = args.output
    if not output_file:
        output_file = input_dir.parent / OUTPUT_MOVIE_FILE

    # TODO


def main():
    parser = argparse.ArgumentParser(
        description="Generate chaotic patterns by applying optical flow to noise."
    )
    sub_parsers = parser.add_subparsers(dest="command", required=True)

    cmd_parser = sub_parsers.add_parser(
        "extract_flow", help="Extract optical flow from input video"
    )
    cmd_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Directory to save flow frames",
    )
    cmd_parser.add_argument("input", type=Path, help="Input video file")
    cmd_parser.set_defaults(func=cmd_extract_flow)

    cmd_parser = sub_parsers.add_parser(
        "generate_frames",
        help="Generate output frames by applying flow to evolving noise",
    )
    cmd_parser.add_argument(
        "-o",
        "--output_dir",
        type=Path,
        help="Directory to save output frames",
    )
    cmd_parser.add_argument(
        "flow_dir",
        type=Path,
        help="Directory containing flow frames",
    )
    cmd_parser.set_defaults(func=cmd_generate_frames)

    cmd_parser = sub_parsers.add_parser(
        "assemble_video", help="Assemble frames into final video"
    )
    cmd_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output video file",
    )
    cmd_parser.add_argument(
        "frames_dir",
        type=Path,
        help="Directory containing output frames",
    )
    cmd_parser.set_defaults(func=cmd_assemble_video)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.print_help()
        return

    func(args)

    return

    # Pass 1: Extract optical flow from input video and save to disk
    dimensions, fps, total_flows = extract_optical_flow(INPUT_MOVIE_FILE)

    # Pass 2: Generate output frames by applying flow to evolving noise
    generate_output_video(dimensions, fps, total_flows)

    # Pass 3: Assemble frames into final video
    create_final_video(dimensions, fps)

    print("\n✨ Done! Chaos patterns generated in trex_effect.webm ✨")


if __name__ == "__main__":
    main()
