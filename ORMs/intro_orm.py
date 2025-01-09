from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

engine = create_engine('mysql+mysqlconnector://root:password@localhost/intro_orm')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable = False)
    email: Mapped[str] = mapped_column(String(100))

Base.metadata.create_all(engine)

session = Session(engine)

# new_user = User(name="Dylan", email="dkatina@email.com")

# session.add(new_user)
# session.commit()

query = select(User)
users = session.execute(query).scalars().all()
print(users)