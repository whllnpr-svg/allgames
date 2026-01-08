from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import mysql.connector
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 数据库连接配置
db_config = {
    "host": "localhost",
    "user": "test",        # 你的 MySQL 用户名
    "password": "SA123",  # 你的 MySQL 密码
    "database": "minigame_platform"
}

# 数据模型
class ScoreSubmit(BaseModel):
    game_key: str
    player_name: str
    score: int

# --- API 路由 ---

@app.get("/")
async def read_index():
    return FileResponse('index.html')

# 从数据库获取游戏列表
@app.get("/api/games")
async def get_games():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT game_key as id, name, description as `desc`, icon, url FROM minigame_list")
    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return games

# 提交分数
@app.post("/api/scores")
async def submit_score(data: ScoreSubmit):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO minigame_scores (game_key, player_name, score) VALUES (%s, %s, %s)"
    cursor.execute(query, (data.game_key, data.player_name, data.score))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "分数提交成功"}

# 获取排行榜前10名
@app.get("/api/scores/{game_key}")
async def get_leaderboard(game_key: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT player_name, score, recorded_at FROM minigame_scores WHERE game_key = %s ORDER BY score DESC LIMIT 10"
    cursor.execute(query, (game_key,))
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return scores

app.mount("/static", StaticFiles(directory="static"), name="static")