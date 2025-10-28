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
from pathlib import Path

import moderngl_window as mglw
import numpy as np
from moderngl_window import geometry

WIDTH = 512
HEIGHT = WIDTH


class MainWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Trex Effect"
    window_size = (WIDTH, HEIGHT)
    aspect_ratio = WIDTH / HEIGHT
    resource_dir = Path().absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Generate the noise texture
        # Random RGB, A=1
        data = np.random.randint(
            0,
            256,
            (WIDTH, HEIGHT, 4),
            dtype="u1",
        )
        data[:, :, 3] = 255  # Set alpha to 255
        self.noise_texture = self.ctx.texture(
            (WIDTH, HEIGHT),
            4,
            data=data,
        )

        # Create the fullscreen quad and program
        self.trex_quad = geometry.quad_fs()
        self.trex_prog = self.load_program("shader_trex.glsl")

        # Create a depth buffer texture with test data
        # Speed data, between -16 and 16
        data = np.zeros((WIDTH, HEIGHT), dtype="f4")

        # Rect1
        rect_size = WIDTH * 3 // 4
        start = (WIDTH - rect_size) // 2
        end = start + rect_size
        data[start:end, start:end] = 3.0

        # Rect2
        rect_size = WIDTH // 2
        start = (WIDTH - rect_size) // 2
        end = start + rect_size
        data[start:end, start:end] = 0.0

        # Rect3
        rect_size = WIDTH // 4
        start = (WIDTH - rect_size) // 2
        end = start + rect_size
        data[start:end, start:end] = -3.0

        data = (data + 16) / 32  # Normalize to [0, 1] range

        self.depth_buffer = self.ctx.depth_texture((WIDTH, HEIGHT), data=data)

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear()

        # TODO: render scene to get depth values

        # Final pass
        self.noise_texture.use(location=0)
        self.depth_buffer.use(location=1)
        self.trex_prog["noise_texture"].value = 0
        self.trex_prog["depth_texture"].value = 1
        self.trex_prog["time"].value = time
        self.noise_texture.use(location=0)
        self.trex_quad.render(self.trex_prog)


def main():
    mglw.run_window_config(MainWindow)


if __name__ == "__main__":
    main()
