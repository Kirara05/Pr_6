from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database.connections import get_session
from models.users import User, NewUser, UserSignIn

user_router = APIRouter(tags=["User"])


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_user_up(data: NewUser, session: Session = Depends(get_session)) -> dict:
    user_exist = session.exec(select(User).where(User.email == data.email)).first()
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    user = User(email=data.email, password=data.password)
    session.add(user)
    session.commit()
    return {"message": "Пользователь успешно зарегистрирован"}


@user_router.post("/signin")
async def sign_user_in(
    user: UserSignIn, session: Session = Depends(get_session)
) -> dict:
    user_exist = session.exec(select(User).where(User.email == user.email)).first()
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
