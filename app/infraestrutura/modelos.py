from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infraestrutura.db import Base


class LugarORM(Base):
    __tablename__ = "lugar"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20))
    bairro: Mapped[str] = mapped_column(String(60), index=True)
    como_e: Mapped[str] = mapped_column(Text, default="")

    avisos: Mapped[list["AvisoORM"]] = relationship(
        back_populates="lugar", cascade="all, delete-orphan")
    relatos: Mapped[list["RelatoORM"]] = relationship(
        back_populates="lugar", cascade="all, delete-orphan")


class AvisoORM(Base):
    __tablename__ = "aviso"

    id: Mapped[int] = mapped_column(primary_key=True)
    lugar_id: Mapped[int] = mapped_column(ForeignKey("lugar.id"), index=True)
    recurso: Mapped[str] = mapped_column(String(20))
    descricao: Mapped[str] = mapped_column(String(200))
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    valido_ate: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    lugar: Mapped[LugarORM] = relationship(back_populates="avisos")


class RelatoORM(Base):
    __tablename__ = "relato"

    id: Mapped[int] = mapped_column(primary_key=True)
    lugar_id: Mapped[int] = mapped_column(ForeignKey("lugar.id"), index=True)
    data_visita: Mapped[date] = mapped_column(Date)
    turno: Mapped[str] = mapped_column(String(10))
    necessidade: Mapped[str] = mapped_column(String(20))
    deu_certo: Mapped[bool]
    comentario: Mapped[str] = mapped_column(Text, default="")

    lugar: Mapped[LugarORM] = relationship(back_populates="relatos")