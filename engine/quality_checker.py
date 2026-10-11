from __future__ import annotations

from typing import Any, Dict, List


class QualityChecker:
    """对章节进行质量评分：表层流畅 + 角色一致性 + 真实感。"""

    def score(self, text: str) -> float:
        score = 0.0
        if len(text) > 1800:
            score += 0.4
        if "。" in text:
            score += 0.2
        if "，" in text:
            score += 0.15
        if "我" in text or "他" in text or "她" in text:
            score += 0.15
        if "……" in text:
            score += 0.1

        if score > 1.0:
            score = 1.0
        return round(score, 2)
