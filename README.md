# NovelAI-WritingEngine

一个面向长篇小说创作的智能写作引擎，目标是：
- 让 AI 生成的内容更接近真人写作
- 维持角色一致性与上下文连续性
- 支持连载式章节生成
- 具备反 AI 味处理机制
- 提升读者感受：人物可信、情绪真实、情节顺畅

## 功能概览

- 角色卡管理：姓名、性格、成长轨迹、关系网、口吻
- 连载上下文连续：根据前几章自动记忆人物、情节、时间线
- 章节自动生成：支持标题、开头、重点、结尾、反转
- AI 反检测：多样化句型、避免机械重复、加强自然表达
- 章节改写：对生成内容进行“真人化”润色
- 质量评估：检查重复度、人物一致性、情绪节奏

## 目录结构

```text
NovelAI-WritingEngine/
├── README.md
├── .gitignore
├── requirements.txt
├── app/
│   ├── __init__.py
│   └── main.py
├── engine/
│   ├── __init__.py
│   ├── anti_ai_detector.py
│   ├── character_manager.py
│   ├── context_manager.py
│   ├── novel_generator.py
│   └── quality_checker.py
├── models/
│   ├── __init__.py
│   └── novel_models.py
└── data/
    └── sample_novels/
```

## 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

默认会启动本地 FastAPI 服务，访问：
- http://127.0.0.1:8000/docs

## 核心 API

### 1. 创建小说

```http
POST /api/novels
```

### 2. 添加人物卡

```http
POST /api/novels/{novel_id}/characters
```

### 3. 生成章节

```http
POST /api/novels/{novel_id}/chapters/generate
```

### 4. 改写章节

```http
POST /api/novels/{novel_id}/chapters/{chapter_id}/rewrite
```

## 说明

这是一个可扩展的基础版本，适合用来做：
- AI 小说助手
- 长篇连载生成器
- 角色一致性写作工具
- 内容润色与反 AI 味工具

如果接入真实 LLM（如 OpenAI / Claude / DeepSeek），可以进一步提升生成效果。
