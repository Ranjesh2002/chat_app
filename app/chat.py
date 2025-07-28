from fastapi import WebSocket, WebSocketDisconnect, Depends
from jose import jwt, JWTError
from .auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Message

connections = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

async def websocket_endpoint(websocket: WebSocket, room_id: str, token: str, db: Session):
    await websocket.accept()

    username = await get_current_user(token)
    if not username:
        await websocket.close(code=1008)
        return

    # Add user to room connections
    if room_id not in connections:
        connections[room_id] = []
    connections[room_id].append(websocket)

    # Send last 10 messages
    messages = db.query(Message).filter(Message.room_id == room_id).order_by(Message.timestamp.desc()).limit(10).all()
    for msg in reversed(messages):
        await websocket.send_json({
            "username": msg.username,
            "content": msg.content,
            "timestamp": str(msg.timestamp)
        })

    try:
        while True:
            data = await websocket.receive_json()
            content = data["content"]

            # Save to DB
            message = Message(room_id=room_id, username=username, content=content)
            db.add(message)
            db.commit()

            # Broadcast
            for conn in connections[room_id]:
                await conn.send_json({
                    "username": username,
                    "content": content,
                })
    except WebSocketDisconnect:
        connections[room_id].remove(websocket)
