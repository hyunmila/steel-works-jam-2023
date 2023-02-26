from typing import List
from components.dialog_box import DialogBox
from core.animation import Animation
from core.window import Window

class NPC:
    def __init__(self, dialog_box: DialogBox, animation: Animation, text: List[str]):
        self.dialog_box = dialog_box
        self.animation = animation
        self.text = text

    def update(self, window: Window):
        self.dialog_box.update(window)
        self.animation.update(window)
    
    def interact(self) -> DialogBox:
        self.dialog_box.show(self.text)
        return self.dialog_box

    def __hash__(self):
        return hash(id(self))
