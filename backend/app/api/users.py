from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, PasswordUpdate
from app.services.user_service import UserService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return success_response(UserResponse.model_validate(current_user).model_dump())


@router.put("/me/password")
def update_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        UserService.update_password(db, current_user.id, password_data)
        return success_response(message="密码修改成功")
    except ValueError as e:
        return error_response("WRONG_PASSWORD", str(e))
