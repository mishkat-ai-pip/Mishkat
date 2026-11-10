import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

# مفتاح سري لتشفير التوكنات - في الإنتاج يفضل وضعه في Environment Variable
SECRET_KEY = "MISHKAT_SECRET_2026_SECURE" 
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """تشفير كلمة المرور قبل تخزينها في قاعدة البيانات"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """التحقق من كلمة المرور المدخلة مقابل المشفرة"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """إنشاء توكن دخول صالح لمدة 24 ساعة"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    """فك تشفير التوكن للتحقق من هوية المستخدم"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None
  
