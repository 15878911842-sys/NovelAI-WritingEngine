from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# 基础配置
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# 初始化 FastAPI
app = FastAPI(
    title="NovelAI Pro 2.0",
    description="基于 Claude 的智能小说创作工具",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============== 数据模型 ===============
class Character(BaseModel):
    name: str
    role: str
    age: Optional[int] = None
    personality: List[str] = []
    background: str = ""
    tone: str = ""

class Chapter(BaseModel):
    chapter_num: int
    title: str
    outline: str
    content: str = ""
    created_at: str = ""

class Project(BaseModel):
    project_id: str
    title: str
    description: str
    characters: List[Character] = []
    chapters: List[Chapter] = []
    outline: str = ""
    created_at: str = ""

# =============== 数据持久化 ===============
def load_data():
    """加载所有项目数据"""
    data_file = DATA_DIR / "projects.json"
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    """保存所有项目数据"""
    data_file = DATA_DIR / "projects.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =============== API 路由 ===============
@app.get("/")
def serve_index():
    """提供主页面"""
    return FileResponse(BASE_DIR / "index.html")

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "service": "NovelAI Pro 2.0"}

@app.get("/api/projects")
def list_projects():
    """列出所有项目"""
    projects = load_data()
    return {
        "projects": list(projects.keys()),
        "count": len(projects),
        "data": projects
    }

@app.post("/api/projects")
def create_project(title: str, description: str):
    """创建新项目"""
    projects = load_data()
    project_id = f"proj_{len(projects)}_{int(datetime.now().timestamp())}"
    
    new_project = {
        "project_id": project_id,
        "title": title,
        "description": description,
        "characters": [],
        "chapters": [],
        "outline": "",
        "created_at": datetime.now().isoformat()
    }
    
    projects[project_id] = new_project
    save_data(projects)
    
    return {
        "success": True,
        "project_id": project_id,
        "message": "✅ 项目创建成功"
    }

@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    """获取项目详情"""
    projects = load_data()
    if project_id not in projects:
        return JSONResponse({"error": "项目不存在"}, status_code=404)
    return projects[project_id]

@app.post("/api/projects/{project_id}/characters")
def add_character(project_id: str, character: Character):
    """添加人物卡"""
    projects = load_data()
    if project_id not in projects:
        return JSONResponse({"error": "项目不存在"}, status_code=404)
    
    projects[project_id]["characters"].append(character.dict())
    save_data(projects)
    
    return {"success": True, "message": "✅ 人物卡已添加"}

@app.post("/api/projects/{project_id}/outline")
def set_outline(project_id: str, outline: str):
    """设置大纲"""
    projects = load_data()
    if project_id not in projects:
        return JSONResponse({"error": "项目不存在"}, status_code=404)
    
    projects[project_id]["outline"] = outline
    save_data(projects)
    
    return {"success": True, "message": "✅ 大纲已保存"}

@app.post("/api/projects/{project_id}/chapters")
def add_chapter(project_id: str, chapter_num: int, title: str, outline: str, content: str = ""):
    """添加/保存章节"""
    projects = load_data()
    if project_id not in projects:
        return JSONResponse({"error": "项目不存在"}, status_code=404)
    
    chapter = {
        "chapter_num": chapter_num,
        "title": title,
        "outline": outline,
        "content": content,
        "created_at": datetime.now().isoformat()
    }
    
    # 检查是否已存在该章节
    existing = [i for i, ch in enumerate(projects[project_id]["chapters"]) if ch["chapter_num"] == chapter_num]
    if existing:
        projects[project_id]["chapters"][existing[0]] = chapter
    else:
        projects[project_id]["chapters"].append(chapter)
    
    save_data(projects)
    
    return {"success": True, "message": f"✅ 第{chapter_num}章已保存"}

@app.get("/api/demo")
def get_demo():
    """获取演示数据"""
    return {
        "project_id": "demo_001",
        "title": "互换了身体的我们",
        "description": "高冷会长与问题学弟意外互换了身体",
        "characters": [
            {
                "name": "御影真澄",
                "role": "学生会会长",
                "age": 18,
                "personality": ["冷静", "完美主义", "缺乏安全感"],
                "background": "从小在财阀环境中长大，学会压抑情绪",
                "tone": "克制、真实、带一点锋利"
            },
            {
                "name": "佐仓彻",
                "role": "二年级问题学弟",
                "age": 17,
                "personality": ["嘴硬", "善良", "叛逆"],
                "background": "来自普通家庭，曾被霸凌",
                "tone": "直率、热烈、偶尔撒娇"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
