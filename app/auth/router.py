from fastapi import APIRouter, HTTPException, status
from app.auth.schemas import UserLogin, Token
from app.auth.service import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()


@router.post("/login", response_model=Token)
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
