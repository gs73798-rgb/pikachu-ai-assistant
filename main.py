import os
import requests
import mimetypes  # 核心：用于注册未知的本地多媒体类型
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# 【核心修复】：强行向系统注册 .glb 的标准规范 MIME 头，消灭 application/octet-stream 警告
mimetypes.add_type("model/gltf-binary", ".glb")
mimetypes.add_type("model/gltf+json", ".gltf")

load_dotenv()

app = FastAPI()

# 允许前端跨域访问（本地开发必配）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 【质量修复】：通用中间件，加上安全检测要求的响应头和规范缓存头
@app.middleware("http")
async def add_security_and_cache_headers(request, call_next):
    response = await call_next(request)
    # 注入必备的媒体防窥安全头
    response.headers["X-Content-Type-Options"] = "nosniff"

    # 规范缓存控制，消除部分环境下的空缓存错乱警告
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return response


# --- 请求数据结构模型 ---
class ChatRequest(BaseModel):
    query: str
    conversation_id: str = ""


class TTSRequest(BaseModel):
    text: str


# --- API 1: AI 聊天交互 (对接 Dify 阻塞型接口) ---
@app.post("/api/chat")
async def chat_with_dimo(request: ChatRequest):
    api_key = os.getenv("DIFY_API_KEY")
    api_url = os.getenv("DIFY_API_URL")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8"  # 规避编码格式不齐警告
    }

    payload = {
        "inputs": {},
        "query": request.query,
        "response_mode": "blocking",
        "user": "lock_player_vrm",
        "conversation_id": request.conversation_id
    }

    try:
        response = requests.post(f"{api_url}/chat-messages", json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        dify_data = response.json()
        return {
            "answer": dify_data.get("answer"),
            "conversation_id": dify_data.get("conversation_id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- API 2: 微软 Azure 级高级童声 TTS 语音生成 ---
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """
    接收文本，调用第三方异步边缘语音接口生成高级童声 MP3 并落地到 static/audio
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # 使用 edge-tts 库本地生成
        import edge_tts

        # 挑选极为逼真自然的中国儿童/青少年音色 (微软 YunjianNeural)
        voice = "zh-CN-YunxiNeural"

        output_dir = "static/audio"
        os.makedirs(output_dir, exist_ok=True)

        # 使用哈希避免重叠，重复文本直接命中本地文件
        filename = f"tts_{hash(request.text)}.mp3"
        output_path = os.path.join(output_dir, filename)

        # 如果文件不存在，再启动网络通信进行转换生成
        if not os.path.exists(output_path):
            communicate = edge_tts.Communicate(request.text, voice)
            await communicate.save(output_path)

        return {"audio_url": f"/audio/{filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS语音合成处理失败: {str(e)}")


# --- 静态文件挂载区 (必须放在最末尾！) ---
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    # 本地主进程运行
    uvicorn.run(app, host="127.0.0.1", port=8000)