import os
import uuid

from typing import Optional

from sqlalchemy import select, Column, Integer, String
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase): ...


class Auth(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(64), unique=True)
    access_token = Column(String(32))


def _create_table(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def add_auth_for_entity(engine: Engine, entity_name: str) -> str:
    _create_table(engine=engine)

    access_token = uuid.uuid4().hex
    with Session(engine) as session:
        session.add(Auth(entity_name=entity_name, access_token=access_token))
        session.commit()

    return access_token


def get_auth_from_entity(engine: Engine, entity_name: str) -> Optional[str]:
    with Session(engine) as session:
        stmt = select(Auth.access_token).where(Auth.entity_name == entity_name)
        access_token = session.scalar(stmt)

    return access_token


def get_entity_from_auth(engine: Engine, access_token: str) -> Optional[str]:
    with Session(engine) as session:
        stmt = select(Auth.entity_name).where(Auth.access_token == access_token)
        entity_name = session.scalar(stmt)

    return entity_name
