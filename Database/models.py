from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import BigInteger, String, Boolean

class Base(DeclarativeBase):
    __table_args__ = {"schema": "public"}

class Presentation(Base):
    __tablename__ = "presentation"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    author: Mapped[str]
    description: Mapped[str| None] = mapped_column(default=None)
    file: Mapped[str] = mapped_column(String(30))
    hidden: Mapped[bool] = mapped_column(default=False)
    preview_image: Mapped[str | None] = mapped_column(String(40), default=None)