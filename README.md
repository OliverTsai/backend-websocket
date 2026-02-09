語言為python，框架FastAPI，會用python-socketio實現即時通訊

複製.env.example的資料並另存成.env，修改成自己的環境變數

安裝docker

重新建置指令：

docker-compose down

docker-compose build --no-cache backend

docker-compose up -d

docker-compose logs -f backend

測試API：http://localhost:8000/docs