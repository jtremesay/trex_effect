import subprocess
from tempfile import TemporaryDirectory

import numpy as np
from PIL import Image


def main():
    width = 512
    height = 512
    fps = 60
    duration_seconds = 10

    noise_data = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    noise_roll_data = noise_data.copy()

    mask = np.array(Image.open("mask.png").convert("1"), dtype=bool)
    with TemporaryDirectory() as temp_dir:
        for i in range(fps * duration_seconds):
            print(f"Generating frame {i}")
            noise_roll_data = np.roll(noise_roll_data, shift=1, axis=0)

            frame_data = noise_data.copy()
            frame_data[mask] = noise_roll_data[mask]

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
