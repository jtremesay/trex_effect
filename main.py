from pathlib import Path

import glm
from moderngl import CULL_FACE, DEPTH_TEST, Context
from moderngl_window import geometry, run_window_config
from moderngl_window.context.base.window import WindowConfig
from moderngl_window.meta.program import ProgramDescription
from moderngl_window.resources.programs import programs
from moderngl_window.scene.camera import Camera, OrbitCamera


class Scene:
    def __init__(self):
        pass

    def update(self, time: float, frame_time: float, camera: Camera):
        pass

    def render(self, ctx: Context, camera: Camera):
        pass


class CubesScene(Scene):
    def __init__(self):
        self.cubes = [geometry.cube(size=(2, 2, 2)) for _ in range(3)]
        self.prog = programs.load(ProgramDescription("programs/cube_simple.glsl"))
        self.prog["color"].value = 1.0, 1.0, 1.0, 1.0

    def update(self, time: float, frame_time: float, camera: OrbitCamera):
        camera.rot_state(frame_time * 360, 0)
        pass

    def render(self, ctx: Context, camera: Camera):
        ctx.enable_only(CULL_FACE | DEPTH_TEST)

        self.prog["m_proj"].write(camera.projection.matrix)
        self.prog["m_camera"].write(camera.matrix)
        for i, cube in enumerate(self.cubes):
            # rotation = glm.mat4(glm.quat(glm.vec3(time, time, time)))
            rotation = glm.mat4(glm.quat(glm.vec3(0, 0, 0)))
            translation = glm.translate(glm.vec3(0.0 + 3 * (i - 1), 0.0, 0.0))
            modelview = translation @ rotation

            self.prog["m_model"].write(modelview)

            cube.render(self.prog)


class MainWindow(WindowConfig):
    gl_version = (3, 3)
    window_size = (1920, 1080)
    window = "pygame2"
    resource_dir = (Path(__file__).parent / "resources").resolve()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = OrbitCamera(radius=10, aspect_ratio=self.wnd.aspect_ratio)
        self.camera_enabled = True
        self.scene = CubesScene()

    def on_render(self, time: float, frame_time: float):
        self.scene.update(time, frame_time, self.camera)
        self.scene.render(self.ctx, self.camera)

    def on_key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    # def on_mouse_position_event(self, x: int, y: int, dx, dy):
    #     if self.camera_enabled:
    #         self.camera.rot_state(dx, dy)

    def on_mouse_scroll_event(self, x_offset: float, y_offset: float):
        if self.camera_enabled:
            self.camera.zoom_state(y_offset)

    def on_resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)


def main():
    run_window_config(MainWindow, args=["--window", MainWindow.window])


if __name__ == "__main__":
    main()
