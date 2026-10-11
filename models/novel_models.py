from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Character:
    name: str
    role: str
    age: Optional[int] = None
    personality: List[str] = field(default_factory=list)
    background: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)
    tone: str = "自然、克制、真实"


@dataclass
class Chapter:
    chapter_number: int
    title: str
    content: str
    summary: str = ""
    word_count: int = 0


@dataclass
class Novel:
    novel_id: str
    title: str
    outline: str
    characters: List[Character] = field(default_factory=list)
    chapters: List[Chapter] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
