from __future__ import annotations

from typing import Dict, List, Any


class CharacterManager:
    """用于维护人物卡、背景、口味和关系线。"""

    def __init__(self):
        self.characters: Dict[str, Dict[str, Any]] = {}

    def add_character(self, name: str, role: str, age: int = None, **kwargs):
        self.characters[name] = {
            "name": name,
            "role": role,
            "age": age,
            "personality": kwargs.get("personality", []),
            "background": kwargs.get("background", ""),
            "relationships": kwargs.get("relationships", {}),
            "tone": kwargs.get("tone", "克制、真实、带一点锋利"),
        }
        return self.characters[name]

    def get_character(self, name: str):
        return self.characters.get(name)

    def export(self):
        return self.characters
