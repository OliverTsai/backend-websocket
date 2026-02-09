#!/usr/bin/env python
"""
開發環境啟動腳本
"""
import os
import subprocess
import sys

def setup_environment():
    """設置開發環境變數"""
    # 檢查 .env 檔案是否存在，如果不存在則從範例檔案複製
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("Creating .env file from .env.example...")
            with open('.env.example', 'r') as example_file:
                with open('.env', 'w') as env_file:
                    env_file.write(example_file.read())
        else:
            print("Warning: .env.example file not found.")
            
    # 讀取 .env 檔案中的環境變數
    if os.path.exists('.env'):
        with open('.env', 'r') as env_file:
            for line in env_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def start_backend():
    """啟動後端服務"""
    print("Starting backend server...")
    try:
        # 使用 uvicorn 啟動 FastAPI 應用程式
        subprocess.run(
            [
                "uvicorn", 
                "backend.app.main:app", 
                "--reload", 
                "--host", "0.0.0.0", 
                "--port", os.environ.get("BACKEND_PORT", "8000")
            ],
            check=True
        )
    except KeyboardInterrupt:
        print("\nBackend server stopped.")
    except Exception as e:
        print(f"Error starting backend server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()
    start_backend()