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

WIDTH = 1024
HEIGHT = WIDTH
LAYERS = 1


class MainWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Trex Effect"
    window_size = (WIDTH, HEIGHT)
    aspect_ratio = WIDTH / HEIGHT
    resource_dir = Path().absolute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Random RGB, A=1
        data = np.random.randint(
            0,
            256,
            (WIDTH, HEIGHT, LAYERS, 4),
            dtype="u1",
        )
        data[:, :, :, 3] = 255  # Set alpha to 255

        self.texture = self.ctx.texture_array(
            (WIDTH, HEIGHT, LAYERS),
            4,
            data=data,
        )
        self.bg_quad = geometry.quad_fs()
        self.rect_quad = geometry.quad_2d(
            size=(0.5, 0.5),
        )
        self.prog = self.load_program("shader1.glsl")

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear()

        self.texture.use(location=0)
        self.prog["texture0"].value = 0
        self.prog["num_layers"].value = 0
        self.prog["depth"].value = 0
        self.prog["time"].value = time * 0.1
        self.texture.use(location=0)
        self.bg_quad.render(self.prog)

        self.prog["depth"].value = 1
        self.rect_quad.render(self.prog)


def main():
    mglw.run_window_config(MainWindow)


if __name__ == "__main__":
    main()
