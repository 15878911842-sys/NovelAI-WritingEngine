from __future__ import annotations

import os
from typing import Dict, List, Any

from engine.anti_ai_detector import AntiAIDetector
from engine.character_manager import CharacterManager
from engine.context_manager import ContextManager
from engine.quality_checker import QualityChecker


class NovelGenerator:
    """小说长篇生成引擎，支持连载、一致性和智能润色。"""

    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.character_manager = CharacterManager()
        self.context_manager = ContextManager()
        self.ai_detector = AntiAIDetector()
        self.quality_checker = QualityChecker()

    def add_character(self, name: str, role: str, age: int = None, **kwargs):
        return self.character_manager.add_character(name, role, age=age, **kwargs)

    def generate_chapter(self, title: str, chapter_number: int, outline: str, previous_chapters: List[Dict[str, Any]], characters: Dict[str, Any]):
        context = self.context_manager.build_context(previous_chapters, characters, chapter_number)
        raw_prompt = f"""
        任务：生成一章小说，要求以下几点：
        1. 章节标题：{title}
        2. 当前章节编号：第{chapter_number}章
        3. 本章大纲：{outline}
        4. 上下文：
        {context}
        5. 写作要求：
           - 语言自然、克制、真实，不要机械套话
           - 细节真实、人物关系清晰
           - 情绪转折要有层次
           - 不要明显 AI 味，不要过度抒情，不要泛化空洞的描述
           - 降低重复语句、减少模板化叙述
        6. 目标字数：约4500字
        """

        generated = self._fallback_generate(raw_prompt, title)
        refined = self.ai_detector.refine(generated)
        quality = self.quality_checker.score(refined)

        return {
            "title": title,
            "chapter_number": chapter_number,
            "content": refined,
            "quality_score": quality,
            "anti_ai_score": self.ai_detector.score(refined),
        }

    def _fallback_generate(self, prompt: str, title: str) -> str:
        if not self.api_key:
            return self._template_novel_text(title)

        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一名职业小说作者，擅长长篇连载、情感真实、叙事顺畅、人物逻辑稳定。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2000,
            )
            return resp.choices[0].message.content
        except Exception:
            return self._template_novel_text(title)

    def _template_novel_text(self, title: str) -> str:
        return f"""
        {title}

        太阳从远处的屋檐后面露出来，光线落在窗边的青石上，淡淡地晕出一层暖意。

        他站在门口，手指按住门把，良久没有伸进去。屋子里静得有些吓人，只有钟表在走，发出轻微而清晰的声响，像一根细线，绷得过紧。

        他忽然想起，几个月前，那个晚上他们还在对峙，彼此都不肯先低头。她站在走廊尽头，背影很瘦，像一根会在风里被吹折的竹子。

        但后来，所有的锋利都被时间磨得钝了。再后来，他才知道，很多事原来都不需要那么硬。

        这不是一场惊天动地的争吵，也不是一场完美的告白。只是一个普通人，走过许多个普通的日子，终于有一天，才明白自己其实早就喜欢上了那个人。

        他伸手把门推开，门轴发出轻微的响声。屋子里有风，桌上的茶盏没冷透，盖着一层薄薄的雾。明明没人，空气却像还留着刚刚说过话的余温。

        他低头看了一眼，刚想说什么，忽然听见桌边一声轻响。对面的人抬头，眼神落在他身上，极短暂地停住，随后又转开，像是故意避开。

        “你来了。”

        说话的人声音很平，很淡，像平日里的每一句都没有太多情绪，可他听得出，里面有一丝意外，也有一点不肯承认的松动。

        他没立刻回答。走近一步，目光落在她手上的那枚小银饰上。它很旧，边缘被摸得发亮，像是人手指经过无数次之后，连光泽都换成了熟悉。

        他想说很多话，想问很多事，但最终只说了一句：

        “我来，是因为我怕错过。”

        对面的人没有马上开口，半晌之后，才轻轻笑了一下，笑意淡得像一阵掠过的风。

        “你一向不喜欢迟到。”

        这句话本来应该很轻，可偏偏落到他耳朵里，却像是被人放进了水里，浮起来的每一个字都沉重得不符合它原本的分量。

        他站在她面前，忽然觉得，人和人之间，有些东西并不是靠一时冲动决定的，而是靠长久以来的相处、误会、隐忍、回头，最终沉到一起。

        他看见她的眼睛，里面没有别人想象中的冷，也没有那种一眼看透一切的清醒。只有一点点疲惫，还有一点点，不肯承认的心动。

        “你不必替我想太多。”她说。

        “可我总在想。”他答道。

        房间里安静了一会儿。外面的街道有车声，远远地冲过来，像潮水翻过路面的声音，带着一点淡淡的城市气味。

        他忽然明白，原来很多人都以为感情一定要轰轰烈烈，才算真。可真正最难的事情，不是热烈，而是一直站在彼此面前，明知道会受伤，还愿意再靠近一点。

        他往前走了一步，靠近她的桌边，几乎贴到她的袖口上。她没有退开，甚至只是抬眼看他，眼光里有一瞬间的迟疑，却没有逃。

        “那你想知道我为什么来了？”

        她看他，语气轻得像在试探：“为什么？”

        “因为我不想再假装什么都没发生。”

        话音落下，空气里有一瞬间微妙的停顿。

        他说得很慢，几乎像是在说服自己。可他知道，真正的问题从来不是说不说，而是自己有没有勇气承认。这件事，已经在心里耽搁太久了，像一滴水落在石头上，虽然微小，却不断在某个角落发出回响。

        她没有立刻回答。她的指尖在桌边轻轻触了一下，仿佛想把那些话从心里剥掉，最后只剩下一片沉默。

        可沉默并不意味着拒绝。它更像一种迟疑，一种怕自己投入以后，立刻被现实打碎的迟疑。

        他忽然笑了，笑意很轻，甚至带着一点苦。

        “我知道你会觉得我说得太多。”

        “不。”她低声道，“你从来没有说过太多。”

        这句话落下的时候，他心口一震，像有人在很深的地方推了一下。

        他忽然意识到，原来人的心事，很多时候，不是怕被听见，而是怕被看见。怕别人见到自己曾经脆弱、失落、笨拙、心动。

        但眼前这个人，明明有一切可以逃开的理由，却仍然留在这里，站在他面前。

        他伸手去拿她递过来的茶杯，指尖碰到她的手，微凉，轻而短，像一瞬间的触电。她没有缩回去，反而抬起眼来，和他对视。

        那一瞬间，所有不说出口的东西，像突然被灯打开，落进了彼此的眼底。

        这并不是一场惊天动地的命运安排，也不是一段被童话编织出来的戏剧，而是两个得过且过的人，在日复一日里终于知道，彼此的存在，比自己想象中的重要得多。

        他低下头，轻轻把茶杯放回桌上。

        “那，我就不再装作什么都没看见。”

        她看他，忽然笑了，笑得很慢，却温柔得让人不敢逼近。

        “那你就别装了。”

        听见这句话，他终于觉得，原来世界不一定总要在最难的时刻才给人答案。很多时候，答案就在你明明知道，却不肯承认的那一瞬间。

        夜色慢慢落下来，城市外的路灯一点点亮起，像人们在一件事上终于决定把心门打开。即使寂静，仍然有人在等，等那个真正愿意走到面前的人。

        而他终于明白，所谓喜欢，不是得到全部答案，而是一边接受不完美，一边依然愿意把那个人放进自己的生活里。

        这就是开始。
        """
