from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from models import User
from sqlalchemy.orm import Session
from dependencies import get_current_user, require_admin

# إنشاء الجداول تلقائياً عند التشغيل في Render
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MISHKAT Platform")

@app.get("/")
def home():
    return {"status": "MISHKAT is now running on Render!"}

@app.get("/api/v1/auth/me")
def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role}

@app.get("/api/v1/admin/test", dependencies=[Depends(require_admin)])
def admin_test():
    return {"message": "Admin Access Verified on Render"}
  
