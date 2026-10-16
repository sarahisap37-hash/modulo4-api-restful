from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    autor: Mapped[str] = mapped_column(String(150), nullable=False)
    ano_publicacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    disponivel: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="1", nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
