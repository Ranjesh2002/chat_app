from fastapi import FastAPI, Depends, HTTPException, WebSocket
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .chat import websocket_endpoint, get_db
from .database import SessionLocal, engine
from .models import Base
from . import models, schemas, auth, deps

# ✅ Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.username, "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin-only")
def read_admin_data(dep=Depends(deps.get_current_user_role("admin"))):
    return {"msg": "Hello, admin!"}

@app.get("/user-only")
def read_user_data(dep=Depends(deps.get_current_user_role("user"))):
    return {"msg": "Hello, user!"}


@app.websocket("/ws/{room_id}")
async def chat_ws(websocket: WebSocket, room_id: str, token: str, db: Session = Depends(get_db)):
    await websocket_endpoint(websocket, room_id, token, db)