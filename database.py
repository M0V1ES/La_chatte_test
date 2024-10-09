from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column
from sqlalchemy import String, create_engine, select, inspect

engine = create_engine("sqlite:///database.db", echo=True)

class Base(DeclarativeBase):
	pass
#Создаем образ таблицы
class CinemaBase(Base):
	__tablename__ = "Films"
	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str] = mapped_column(String(100))
	description: Mapped[str] = mapped_column(String(500))
	raiting: Mapped[float]
	photo: Mapped[str]
#Создаем таблицу на компьютере
def create_db_and_tables() -> None:
	if not inspect(engine).has_table(table_name="films"):
		Base.metadata.create_all(engine)
#Получаем данные
def get_films():
	with Session(engine) as session:
		statement = select(CinemaBase)
		objects = session.scalars(statement).all()
		return objects

create_db_and_tables()