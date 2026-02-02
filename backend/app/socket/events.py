from app.socket.manager import sio
from app.services.message import MessageService
from app.services.auth import verify_token
from app.database.session import AsyncSessionLocal

# 儲存連線用戶: {sid: user_id}
connected_users: dict[str, str] = {}


@sio.event
async def connect(sid, environ, auth):
    """用戶連線時驗證 JWT"""
    try:
        token = auth.get("token") if auth else None
        if not token:
            raise ConnectionRefusedError("Missing token")
        
        user_id = verify_token(token)
        connected_users[sid] = user_id
        print(f"User {user_id} connected with sid {sid}")
        return True
    except Exception as e:
        print(f"Connection refused: {e}")
        raise ConnectionRefusedError("Authentication failed")


@sio.event
async def disconnect(sid):
    """用戶斷線"""
    user_id = connected_users.pop(sid, None)
    print(f"User {user_id} disconnected")


@sio.event
async def join_room(sid, data):
    """加入聊天室"""
    room_id = data.get("room_id")
    user_id = connected_users.get(sid)
    
    if room_id and user_id:
        sio.enter_room(sid, room_id)
        await sio.emit("user_joined", {"user_id": user_id}, room=room_id, skip_sid=sid)
        print(f"User {user_id} joined room {room_id}")


@sio.event
async def leave_room(sid, data):
    """離開聊天室"""
    room_id = data.get("room_id")
    user_id = connected_users.get(sid)
    
    if room_id:
        sio.leave_room(sid, room_id)
        await sio.emit("user_left", {"user_id": user_id}, room=room_id)


@sio.event
async def send_message(sid, data):
    """發送訊息並儲存到資料庫"""
    user_id = connected_users.get(sid)
    room_id = data.get("room_id")
    content = data.get("content")
    
    if not all([user_id, room_id, content]):
        return {"error": "Missing required fields"}
    
    # 儲存訊息到資料庫
    async with AsyncSessionLocal() as session:
        message = await MessageService.create_message(
            session=session,
            sender_id=user_id,
            room_id=room_id,
            content=content
        )
    
    # 廣播訊息給房間內所有人
    await sio.emit("new_message", {
        "id": message.id,
        "content": message.content,
        "sender_id": message.sender_id,
        "room_id": message.room_id,
        "created_at": message.created_at.isoformat()
    }, room=room_id)


@sio.event
async def typing(sid, data):
    """顯示正在輸入狀態"""
    user_id = connected_users.get(sid)
    room_id = data.get("room_id")
    
    if room_id:
        await sio.emit("user_typing", {"user_id": user_id}, room=room_id, skip_sid=sid)
