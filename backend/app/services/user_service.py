from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import PasswordUpdate
from app.utils.auth import hash_password, verify_password


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_password(db: Session, user_id: int, password_data: PasswordUpdate) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("用户不存在")
        
        if not verify_password(password_data.old_password, user.password_hash):
            raise ValueError("原密码错误")
        
        user.password_hash = hash_password(password_data.new_password)
        db.commit()
