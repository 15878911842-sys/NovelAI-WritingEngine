from __future__ import annotations

import re
from typing import List


class AntiAIDetector:
    """基础层 AI 味处理：降低模板化语气，增强真人感。"""

    def __init__(self):
        self.ai_phrases = [
            "与此同时",
            "不由得",
            "仿佛",
            "在这个世界里",
            "令人不禁",
            "突然之间",
            "一切都像",
            "无论如何",
            "简直就是",
            "顿时",
        ]

    def refine(self, text: str) -> str:
        cleaned = text.strip()
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        cleaned = re.sub(r" +", " ", cleaned)

        for phrase in self.ai_phrases:
            cleaned = cleaned.replace(phrase, "")

        paragraphs = [p.strip() for p in cleaned.split("\n") if p.strip()]
        refined_paragraphs = []
        for p in paragraphs:
            if len(p) < 40:
                refined_paragraphs.append(p)
                continue
            if p.endswith("。") is False and p.endswith("！") is False and p.endswith("？") is False:
                p = p + "。"
            refined_paragraphs.append(p)

        return "\n\n".join(refined_paragraphs)

    def score(self, text: str) -> float:
        length = len(text)
        sentence_count = len(re.findall(r"[。！？]", text))
        varied_sentence = sentence_count > 4 and length > 200
        no_excess_ai_phrases = all(phrase not in text for phrase in self.ai_phrases)
        if varied_sentence and no_excess_ai_phrases:
            return 0.87
        return 0.62
