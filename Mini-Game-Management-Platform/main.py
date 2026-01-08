from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mini-Game Platform API")


# 允许跨域（方便以后前端调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据库中的游戏数据
GAMES_DB = [
    {"id": "snake", "name": "经典贪吃蛇", "category": "休闲", "url": "/static/games/snake/index.html"},
    {"id": "2048", "name": "数字2048", "category": "益智", "url": "/static/games/2048/index.html"}
]


@app.get("/")
async def root():
    return {"status": "Platform Running", "message": "欢迎来到小游戏管理平台"}


@app.get("/api/games")
async def get_games():
    return GAMES_DB

# 关键步骤：挂载静态文件目录，以后你的小游戏代码全放在这里
# 访问路径：http://localhost:8000/static/games/...
app.mount("/static", StaticFiles(directory="static"), name="static")