# ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4)
#
# Copyright © 2025 Jonathan Tremesaygues
#
# This is anti-capitalist software, released for free use by individuals and
# organizations that do not operate by capitalist principles.
#
# Permission is hereby granted, free of charge, to any person or organization
# (the "User") obtaining a copy of this software and associated documentation
# files (the "Software"), to use, copy, modify, merge, distribute, and/or sell
# copies of the Software, subject to the following conditions:
#
# 1. The above copyright notice and this permission notice shall be included in
#    all copies or modified versions of the Software.
#
# 2. The User is one of the following:
#   a. An individual person, laboring for themselves
#   b. A non-profit organization
#   c. An educational institution
#   d. An organization that seeks shared profit for all of its members, and
#      allows non-members to set the cost of their labor
#
# 3. If the User is an organization with owners, then all owners are workers and
#    all workers are owners with equal equity and/or equal vote.
#
# 4. If the User is an organization, then the User is not law enforcement or
#     military, or working for or under either.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY
# KIND, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
