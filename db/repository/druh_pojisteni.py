from sqlmodel import Field
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel

from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.session import engine
from schemas.druh_pojisteni import UpravDruhPojisteni
from schemas.druh_pojisteni import VytvorDruhPojisteni


def create_druh_pojisteni(session: Session, druh_pojisteni: VytvorDruhPojisteni):

    druh_pojisteni = DruhPojisteni.from_orm(druh_pojisteni)
    print(druh_pojisteni)
    session.add(druh_pojisteni)
    session.commit()
    session.refresh(druh_pojisteni)

    return druh_pojisteni


def find_druh_pojisteni(session: Session, druh_pojisteni_id: int):

    druh_pojisteni = session.get(DruhPojisteni, druh_pojisteni_id)

    if not druh_pojisteni:
        return 0

    return druh_pojisteni


def update_druh_pojisteni(
    session: Session, druh_pojisteni_id: int, druh_pojisteni: UpravDruhPojisteni
):

    existing_druh_pojisteni = session.get(DruhPojisteni, druh_pojisteni_id)

    if not existing_druh_pojisteni:
        return 0

    druh_pojisteni_data = druh_pojisteni.dict(exclude_unset=True)

    for key, value in druh_pojisteni_data.items():
        setattr(existing_druh_pojisteni, key, value)

    session.add(existing_druh_pojisteni)
    session.commit()
    session.refresh(existing_druh_pojisteni)
    return existing_druh_pojisteni


def delete_druh_pojisteni(session: Session, druh_pojisteni_id: int):

    druh_pojisteni = session.get(DruhPojisteni, druh_pojisteni_id)

    if not druh_pojisteni:
        return 0

    session.delete(druh_pojisteni)
    session.commit()
    return {"ok": True}


def list_druhy_pojisteni(session):

    druhy_pojisteni = session.exec(select(DruhPojisteni)).all()

    return druhy_pojisteni
