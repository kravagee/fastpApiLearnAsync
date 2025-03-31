from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)