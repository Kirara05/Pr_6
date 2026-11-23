from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from database.connections import get_session
from models.events import Event
from models.users import User

web_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@web_router.get("/")
async def home():
    return RedirectResponse(url="/ui/events", status_code=status.HTTP_302_FOUND)


# ================= КАТЕГОРИЯ: СОБЫТИЯ =================


@web_router.get("/ui/events")
async def ui_events_page(request: Request, session: Session = Depends(get_session)):
    events = session.exec(select(Event)).all()
    return templates.TemplateResponse(
        request=request, name="events.html", context={"events": events}
    )


@web_router.post("/ui/events/new")
async def ui_create_event(
    title: str = Form(...),
    location: str = Form(default=""),
    description: str = Form(default=""),
    tags: str = Form(default=""),
    image: str = Form(default=""),
    session: Session = Depends(get_session),
):
    new_event = Event(
        title=title, location=location, description=description, tags=tags, image=image
    )
    session.add(new_event)
    session.commit()
    return RedirectResponse(url="/ui/events", status_code=status.HTTP_303_SEE_OTHER)


@web_router.post("/ui/events/delete/{id}")
async def ui_delete_event(id: int, session: Session = Depends(get_session)):
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
    return RedirectResponse(url="/ui/events", status_code=status.HTTP_303_SEE_OTHER)


# ================= КАТЕГОРИЯ: ПОЛЬЗОВАТЕЛИ =================


@web_router.get("/ui/users")
async def ui_users_page(request: Request, session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        request=request, name="users.html", context={"users": users}
    )


@web_router.post("/ui/users/signup")
async def ui_signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    existing = session.exec(select(User).where(User.email == email)).first()
    message = None
    error = None

    if existing:
        error = "Пользователь с таким email уже существует"
    else:
        user = User(email=email, password=password)
        session.add(user)
        session.commit()
        message = "Пользователь успешно зарегистрирован"

    users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"users": users, "message": message, "error": error},
    )


@web_router.post("/ui/users/signin")
async def ui_signin(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.email == email)).first()
    message = None
    error = None

    if not user:
        error = "Пользователь с таким email не найден"
    elif user.password != password:
        error = "Неверный пароль"
    else:
        message = f"Успешный вход в систему: {user.email}"

    users = session.exec(select(User)).all()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"users": users, "message": message, "error": error},
    )
