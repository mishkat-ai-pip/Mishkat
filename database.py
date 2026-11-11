import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# جلب رابط قاعدة البيانات من متغيرات البيئة (Render) أو استخدام الرابط المحلي كاحتياط
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# تصحيح الرابط إذا كان يبدأ بـ postgres:// ليصبح postgresql:// ليتوافق مع SQLAlchemy
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# في حال عدم وجود متغير بيئة (مثلاً في Termux)، نضع الرابط المحلي الافتراضي
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://u0_a301@localhost/mishkat"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise e

# Dependency لإدارة جلسات قاعدة البيانات في FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
