from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import hash_password, verify_password, create_token


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError("邮箱已被注册")
        
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise ValueError("用户名已被使用")
        
        hashed_password = hash_password(user_data.password)
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> tuple[str, User]:
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            raise ValueError("用户不存在")
        
        if not verify_password(login_data.password, user.password_hash):
            raise ValueError("密码错误")
        
        token = create_token({"user_id": user.id, "email": user.email})
        
        return token, user
