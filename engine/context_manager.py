from __future__ import annotations

from typing import List, Dict, Any


class ContextManager:
    """负责接收前置章节，并构造连续上下文。"""

    def build_context(self, previous_chapters: List[Dict[str, Any]], characters: Dict[str, Any], current_chapter: int):
        context_lines = []
        context_lines.append(f"当前章节编号：{current_chapter}")
        context_lines.append("人物档案：")
        for name, data in characters.items():
            context_lines.append(f"- {name}: {data.get('role', '角色')}，人格：{', '.join(data.get('personality', []))}")

        if previous_chapters:
            context_lines.append("前置章节摘要：")
            for ch in previous_chapters[-3:]:
                context_lines.append(f"- 第{ch.get('chapter_number')}章：{ch.get('summary') or ch.get('title')}")

        return "\n".join(context_lines)
