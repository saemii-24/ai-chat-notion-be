from fastapi import APIRouter, HTTPException, status
from app.auth.schemas import UserLogin, Token, UserCreate
from app.auth.service import authenticate_user, create_access_token, hash_password
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.auth.models import User

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    try:
        hashed = hash_password(user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    new_user = User(
        username=user_data.username,
        password=hashed,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "username": new_user.username}


@router.post("/login", response_model=Token)
async def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    로그인 엔드포인트
    1. 사용자 입력 받기 (평문 비밀번호)
    2. DB에서 해시값 가져오기
    3. verify()로 비교 (평문 vs 해시값)
    """
    # 🔐 authenticate_user 내부에서 verify_password() 실행됨
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
