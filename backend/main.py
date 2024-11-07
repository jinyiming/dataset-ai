from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
from api.model_api import app as model_app
from config import Config

# 创建 Flask 应用
def create_flask_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    CORS(flask_app, resources={r"/api/*": {"origins": "*"}})
    flask_app.register_blueprint(api_bp, url_prefix='/api')
    return flask_app

# 创建 FastAPI 应用
app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 Flask 应用
flask_app = create_flask_app()
app.mount("/flask", WSGIMiddleware(flask_app))

# 包含 model_api 的路由
app.include_router(model_app, prefix="/model")

# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy"}