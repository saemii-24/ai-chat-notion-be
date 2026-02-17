from fastapi import APIRouter, HTTPException, status
from app.auth.schemas import UserLogin, Token
from app.auth.service import authenticate_user, create_access_token

router = APIRouter()


@router.post("/login", response_model=Token)
async def user_login(payload: UserLogin):
    # 1. 유저 인증
    user = authenticate_user(payload.username, payload.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # 2. JWT 생성
    access_token = create_access_token(data={"sub": user["username"]})

    return {"access_token": access_token, "token_type": "bearer"}
