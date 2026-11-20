from fastapi import APIRouter, HTTPException, status
from database.connection import Database
from models.users import User, NewUser, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_user_up(data: NewUser) -> dict:
    user_exist = await User.find_one(User.email == data.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    user = User(email=data.email, password=data.password)
    await user_database.save(user)
    return {"message": "Пользователь успешно зарегистрирован"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь с таким email не найден",
        )
    if user_exist.password == user.password:
        return {"message": "Успешный вход в систему"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные учетные данные"
    )
