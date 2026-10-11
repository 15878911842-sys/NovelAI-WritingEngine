from __future__ import annotations

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.main import app
from engine.novel_generator import NovelGenerator
from models.novel_models import Novel, Character, Chapter


class CharacterPayload(BaseModel):
    name: str
    role: str
    age: int | None = None
    personality: list[str] = Field(default_factory=list)
    background: str = ""
    relationships: dict[str, str] = Field(default_factory={})
    tone: str = "自然、克制、真实"


class ChapterGeneratePayload(BaseModel):
    title: str
    chapter_number: int
    outline: str
    previous_chapters: list[dict] = Field(default_factory=list)
    characters: dict[str, dict] = Field(default_factory={})


def _make_generator():
    return NovelGenerator()


@app.post("/api/novels")
def create_novel(title: str, outline: str = ""):
    novel_id = f"novel_{abs(hash(title))}"
    novel = Novel(novel_id=novel_id, title=title, outline=outline)
    return {
        "novel_id": novel.novel_id,
        "title": novel.title,
        "outline": novel.outline,
        "message": "小说项目创建成功。",
    }


@app.post("/api/novels/{novel_id}/characters")
def add_character(novel_id: str, payload: CharacterPayload):
    generator = _make_generator()
    character = generator.add_character(
        payload.name,
        payload.role,
        age=payload.age,
        personality=payload.personality,
        background=payload.background,
        relationships=payload.relationships,
        tone=payload.tone,
    )
    return {
        "novel_id": novel_id,
        "character": character,
    }


@app.post("/api/novels/{novel_id}/chapters/generate")
def generate_chapter(novel_id: str, payload: ChapterGeneratePayload):
    generator = _make_generator()
    chapter = generator.generate_chapter(
        title=payload.title,
        chapter_number=payload.chapter_number,
        outline=payload.outline,
        previous_chapters=payload.previous_chapters,
        characters=payload.characters,
    )
    return {
        "novel_id": novel_id,
        "chapter": chapter,
    }


@app.post("/api/novels/{novel_id}/chapters/{chapter_id}/rewrite")
def rewrite_chapter(novel_id: str, chapter_id: str, text: str):
    generator = _make_generator()
    refined = generator.ai_detector.refine(text)
    return {
        "novel_id": novel_id,
        "chapter_id": chapter_id,
        "rewritten_text": refined,
        "anti_ai_score": generator.ai_detector.score(refined),
    }
