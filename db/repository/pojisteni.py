from sqlmodel import Field
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel

from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.session import engine
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni


def create_pojisteni_admin(session: Session, pojisteni: VytvorPojisteni):

    pojisteni = Pojisteni.from_orm(pojisteni)
    session.add(pojisteni)
    session.commit()
    session.refresh(pojisteni)

    return pojisteni


def create_pojisteni_user(session: Session, pojisteni: VytvorPojisteni):

    pojisteni = Pojisteni.from_orm(pojisteni)
    session.add(pojisteni)
    session.commit()
    session.refresh(pojisteni)

    return pojisteni


def find_pojisteni(session: Session, pojisteni_id: int):

    pojisteni = session.get(Pojisteni, pojisteni_id)

    if not pojisteni:
        return 0

    return pojisteni


def update_pojisteni(session: Session, pojisteni_id: int, pojisteni: UpravPojisteni):

    existing_pojisteni = session.get(Pojisteni, pojisteni_id)

    if not existing_pojisteni:
        return 0

    pojisteni_data = pojisteni.dict(exclude_unset=True)

    for key, value in pojisteni_data.items():
        setattr(existing_pojisteni, key, value)

    session.add(existing_pojisteni)
    session.commit()
    session.refresh(existing_pojisteni)

    return existing_pojisteni


def delete_pojisteni(session: Session, pojisteni_id: int):

    pojisteni = session.get(Pojisteni, pojisteni_id)

    if not pojisteni:
        return 0

    session.delete(pojisteni)
    session.commit()

    return 1


def list_pojisteni(session):

    pojisteni = session.exec(select(Pojisteni)).all()

    return pojisteni
