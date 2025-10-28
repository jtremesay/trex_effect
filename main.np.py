import subprocess
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image


def main():
    width = 256
    height = width
    fps = 60
    duration_seconds = 10

    fg_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    bg_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

    mask = np.array(Image.open("mask.png").convert("L")) > 127

    with TemporaryDirectory() as temp_dir:
        for i in range(fps * duration_seconds):
            print(f"Generating frame {i}")

            # Move background to the left
            bg_data = np.roll(bg_data, shift=-1, axis=1)

            # Composite frame
            frame_data = bg_data.copy()
            frame_data[mask] = fg_data[mask]

            # Save frame
            frame_image = Image.fromarray(frame_data)
            frame_image.save(f"{temp_dir}/frame_{i:04d}.png")

        print("Generating video with ffmpeg...")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-i",
                f"{temp_dir}/frame_%04d.png",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "output.mp4",
            ]
        )


if __name__ == "__main__":
    main()
