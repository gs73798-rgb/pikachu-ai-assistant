

```markdown
# ⚡ 宝可梦 AI 助手 - 复古掌机皮卡丘 (Pikachu AI Assistant)

这是一个基于 **FastAPI 后端**与 **Three.js 前端**构建的智能 3D 交互网页项目。它将大语言模型的灵魂与经典 GBA 像素游戏风格相结合，打造了一只既能聊天、又自带声优级音色、还能随音乐起舞的网页动态皮卡丘。

---

## ✨ 核心特性

* **📺 复古掌机 UI**：致敬经典的 Game Boy Advance 像素对战风格背景，搭配硬朗的复古游戏机外框与像素字形对话气泡。
* **🦖 3D 动态交互**：使用 Three.js 渲染高精度 3D 皮卡丘模型，智能实现自动居中与脚底贴地，支持 `Idle`、`Jump`、`Dance` 等多状态动画平滑切换。
* **🧠 智能大脑 (Dify)**：后端无缝对接 Dify 全自动对话工作流，支持上下文多轮记忆聊天。
* **🎙️ 商业级声优配音 (火山引擎)**：全面抛弃传统的机械 AI 塑料音，接入字节跳动/抖音同款语音合成技术，提供极具情绪顿挫与二次元颗粒感的超萌奶气童声。
* **🚀 现代化云部署**：完美适配 **Render** 等现代化容器托管平台，支持环境变量无缝注入与动态端口绑定。

---

## 🛠️ 技术栈

* **前端**：HTML5, CSS3 (Linear-Gradient 像素艺术), Three.js (r128), GLTFLoader
* **后端**：Python 3, FastAPI, Uvicorn, Requests
* **AI 核心**：Dify API, 火山引擎高级语音合成 (TTS) API

---

## 📂 项目结构

```text
├── main.py                 # FastAPI 后端核心主程序（含 Dify 及 火山 TTS 接口）
├── static/                 # 前端静态资源目录
│   ├── index.html          # 3D 场景渲染与掌机交互界面
│   ├── my_background.png   # (可选) 自定义上传的本地背景图
│   └── audio/              # 本地音频缓存文件夹（自动生成）
├── .gitignore              # Git 上传忽略配置文件
├── .env                    # (本地专享) 密钥与环境变量配置文件
└── requirements.txt        # 项目 Python 依赖库列表

```

---

## 🚀 本地快速启动

### 1. 克隆项目与安装依赖

```bash
git clone [https://github.com/你的用户名/你的仓库名.git](https://github.com/你的用户名/你的仓库名.git)
cd 你的仓库名
pip install -r requirements.txt

```

### 2. 配置环境变量

在项目根目录下新建 `.env` 文件，并填入你的私有密钥：

```env
DIFY_API_KEY=你的Dify应用密钥
DIFY_API_URL=你的Dify接口地址
VOLC_APPID=你的火山引擎AppID
VOLC_TOKEN=你的火山引擎BearerToken

```

### 3. 运行服务

```bash
python main.py

```

打开浏览器访问 `http://127.0.0.1:8000` 即可开始对战聊天！

---

## 🌐 线上部署规范 (以 Render 为例)

1. 将代码推送到 GitHub（`.env` 和 `static/audio/` 会被 `.gitignore` 自动忽略）。
2. 在 Render 平台新建一个 **Web Service** 并关联该 GitHub 仓库。
3. 在 Render 的 **Environment** 配置中，手动添加上述四个环境变量（`DIFY_API_KEY` 等）。
4. 本项目已完美兼容 `0.0.0.0` 动态端口绑定，启动后即可一键生成全网可访问的 HTTPS 线上链接。

---

## 📜 许可证

本项目基于 MIT 协议开源。仅供技术交流与个人娱乐使用，3D 模型等美术资产版权归原官方所有。

```

```
