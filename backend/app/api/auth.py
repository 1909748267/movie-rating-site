from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(db, user_data)
        return success_response({"user_id": user.id}, "注册成功")
    except ValueError as e:
        error_code = "DUPLICATE_EMAIL" if "邮箱" in str(e) else "DUPLICATE_USERNAME"
        return error_response(error_code, str(e))


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        token, user = AuthService.login_user(db, login_data)
        return success_response({
            "token": token,
            "user": UserResponse.model_validate(user).model_dump()
        }, "登录成功")
    except ValueError as e:
        error_code = "WRONG_PASSWORD" if "密码" in str(e) else "USER_NOT_FOUND"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(error_code, str(e))
        )


@router.post("/logout")
def logout():
    return success_response(message="登出成功")
