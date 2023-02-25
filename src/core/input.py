from typing import Dict, Tuple
import pygame

pygame.K_0

def clamp_value(x, l, h):
    return min(max(x, l), h)

class Input:
    def __init__(self) -> None:
        self._actions: Dict[str, Dict[int, float]] = dict()
        self._pressed_keys: set[int] = set()
        self._prev_pressed_keys: set[int] = set()
        self._just_pressed_keys: set[int] = set()
        self._just_released_keys: set[int] = set()

    def add_action_key(self, action: str, key: int, scale: float = 1) -> None:
        if not action in self._actions:
            self._actions[action] = dict()

        self._actions[action][key] = scale

    def clear_actions(self) -> None:
        self._actions.clear()

    # Returns the current value of the action.
    def get_action_value(self, action: str, clamp: bool = False) -> float:
        if not action in self._actions:
            return 0

        value = 0

        for key in self._actions[action]:
            if key in self._pressed_keys:
                value += self._actions[action][key]

        if clamp:
            return clamp_value(value, -1, 1)
        else:
            return value

    # Checks if any key participating in the action is currently pressed.
    def is_action_pressed(self, action: str) -> bool:
        if not action in self._actions:
            return False

        for key in self._actions[action]:
            if key in self._pressed_keys:
                return True

        return False

    # Checks if any key participating in the action was just pressed.
    def is_action_just_pressed(self, action: str) -> bool:
        if not action in self._actions:
            return False

        for key in self._actions[action]:
            if key in self._just_pressed_keys:
                return True

        return False

    # Checks if any key participating in the action was just released.
    def is_action_just_released(self, action: str) -> bool:
        if not action in self._actions:
            return False

        for key in self._actions[action]:
            if key in self._just_released_keys:
                return True

        return False

    # Retrieves current mouse position.
    def get_mouse_pos(self) -> Tuple[int, int]:
        return pygame.mouse.get_pos()

    def _update_key_state(self, key: int, state: bool) -> None:
        if state:
            self._pressed_keys.add(key)
        else:
            self._pressed_keys.remove(key)

    def _integrate_updates(self) -> None:
        # Find keys that were just pressed or released
        self._just_pressed_keys = self._pressed_keys - self._prev_pressed_keys
        self._just_released_keys = self._prev_pressed_keys - self._pressed_keys
        self._prev_pressed_keys = self._pressed_keys.copy()
