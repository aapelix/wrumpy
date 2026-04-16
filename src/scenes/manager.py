from msg.messages import Message
from scenes.dict import scene_dict
from scenes.base import Scene


class Manager:
    current_scene: Scene | None = None

    def switch(self, scene: Scene):
        self.current_scene = scene

    def switch_by_name(self, name: str):
        if name in scene_dict:
            self.current_scene = scene_dict[name](self)
        else:
            raise ValueError(f"Scene {name} not found")

    def handle_msg(self, msg: Message):
        if self.current_scene is not None:
            self.current_scene.handle_msg(msg)
