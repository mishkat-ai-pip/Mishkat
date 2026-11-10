from fastapi import Depends, HTTPException, status
from auth_handler import decode_token
from database import get_db
from models import User
from sqlalchemy.orm import Session

def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    """
    التحقق من الهوية (Authentication)
    إذا كان التوكن غير صحيح -> 401 Unauthorized
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authentication token missing"
        )
        
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found or inactive"
        )
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    """
    التحقق من الصلاحيات (Authorization)
    إذا كان المستخدم معروفاً ولكن ليس مسؤولاً -> 403 Forbidden
    """
    if current_user.role not in ["Super Admin", "Admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operation not permitted. Administrative privileges required."
        )
    return current_user
  
