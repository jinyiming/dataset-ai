import os
import sys
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 