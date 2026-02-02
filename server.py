import asyncio
import websockets
import json

# 伺服器設定
HOST = '127.0.0.1'
PORT = 5000

# 儲存所有連線的客戶端
connected_clients = set()
nicknames = {}

async def broadcast(message, sender=None):
    """廣播訊息給所有客戶端"""
    if connected_clients:  # 確保有連線的客戶端
        tasks = []
        for client in connected_clients:
            if client != sender:  # 不發送給自己
                try:
                    tasks.append(asyncio.create_task(client.send(message)))
                except:
                    pass
        if tasks:
            await asyncio.gather(*tasks)

async def handle_client(websocket):
    """處理單一客戶端的連線"""
    try:
        # 請求暱稱
        await websocket.send(json.dumps({"type": "request_nickname"}))
        response = await websocket.recv()
        data = json.loads(response)  # 修正：使用 json.loads 而不是 json.parse
        
        if data["type"] == "set_nickname":
            nickname = data["nickname"]
            nicknames[websocket] = nickname
            connected_clients.add(websocket)
            
            print(f"[+] 新使用者連線: {nickname}")
            
            # 通知所有人新使用者加入
            join_message = json.dumps({
                "type": "user_joined",
                "nickname": nickname,
                "message": f"📥 {nickname} 加入了聊天室！"
            })
            await broadcast(join_message)
            
            # 通知使用者連線成功
            await websocket.send(json.dumps({
                "type": "connected",
                "message": "✅ 成功連線到聊天室！"
            }))
            
            # 持續接收訊息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data["type"] == "chat_message":
                        chat_message = data["message"]
                        nickname = nicknames[websocket]
                        formatted_msg = f"💬 {nickname}: {chat_message}"
                        print(formatted_msg)
                        
                        # 廣播訊息給其他人
                        broadcast_message = json.dumps({
                            "type": "chat_message",
                            "nickname": nickname,
                            "message": chat_message
                        })
                        await broadcast(broadcast_message, websocket)
                        
                        # 發送給自己，但標記為自己發送的訊息
                        self_message = json.dumps({
                            "type": "self_message",
                            "nickname": nickname,
                            "message": chat_message
                        })
                        await websocket.send(self_message)
                except json.JSONDecodeError:
                    continue
                
    except websockets.ConnectionClosed:
        pass
    finally:
        # 清理斷線的客戶端
        if websocket in connected_clients:
            nickname = nicknames[websocket]
            connected_clients.remove(websocket)
            del nicknames[websocket]
            
            leave_message = json.dumps({
                "type": "user_left",
                "nickname": nickname,
                "message": f"📤 {nickname} 離開了聊天室"
            })
            await broadcast(leave_message)
            print(f"[-] {nickname} 已斷線")

async def main():
    """啟動WebSocket伺服器"""
    print(f"🟢 WebSocket聊天室伺服器啟動中... 監聽 {HOST}:{PORT}")
    # 修正：移除 path 參數
    async with websockets.serve(handle_client, HOST, PORT):
        await asyncio.Future()  # 持續運行

if __name__ == "__main__":
    asyncio.run(main())