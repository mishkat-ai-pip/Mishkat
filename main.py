from fastapi import FastAPI, Depends
from database import Base, engine, get_db
from models import User
from sqlalchemy.orm import Session
from dependencies import get_current_user, require_admin
import logging

# إعداد السجلات لرؤية الأخطاء بوضوح في Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إنشاء الجداول في قاعدة البيانات فور تشغيل السيرفر
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating tables: {e}")

app = FastAPI(title="MISHKAT Platform")

@app.get("/")
def home():
    return {"status": "MISHKAT is now running on Render!", "message": "System Online"}

@app.get("/api/v1/auth/me")
def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role}

@app.get("/api/v1/admin/test", dependencies=[Depends(require_admin)])
def admin_test():
    return {"message": "Admin Access Verified on Render"}
    
