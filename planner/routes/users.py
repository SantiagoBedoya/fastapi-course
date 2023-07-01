from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])

users = {}

@user_router.post("/signup")
async def sign_new_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user with suplied email exists",
        )
    
    users[data.email] = data
    return {"message": "user successfully registered"}

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn)-> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exists"
        )
    
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="wrong credentials passed"
        )
    
    return {
        "message": "user signed in successfully"
    }