from sqlmodel import SQLModel, Session, create_engine
from models.events import Event

# Название файла базы данных
database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"

# Для SQLite отключаем проверку потоков
connect_args = {"check_same_thread": False}
engine_url = create_engine(
    database_connection_string, echo=True, connect_args=connect_args
)


# Функция создания таблиц при старте
def conn():
    SQLModel.metadata.create_all(engine_url)


# Генератор сессий для маршрутов
def get_session():
    with Session(engine_url) as session:
        yield session
