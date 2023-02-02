from sqlmodel import Field
from sqlmodel import select
from sqlmodel import Session
from sqlmodel import SQLModel

from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.session import engine
from schemas.udalost import Udalost
from schemas.udalost import UpravUdalost
from schemas.udalost import VytvorUdalost


def create_udalost_admin(session: Session, udalost: VytvorUdalost):

    udalost = Udalost.from_orm(udalost)
    session.add(udalost)
    session.commit()
    session.refresh(udalost)

    return udalost


def create_udalost_user(session: Session, udalost: VytvorUdalost):

    udalost = Udalost.from_orm(udalost)
    session.add(udalost)
    session.commit()
    session.refresh(udalost)

    return udalost


def find_udalost(session: Session, udalost_id: int):

    udalost = session.get(Udalost, udalost_id)

    if not udalost:
        return 0

    return udalost


def update_udalost(session: Session, udalost_id: int, udalost: UpravUdalost):

    existing_udalost = session.get(Udalost, udalost_id)

    if not existing_udalost:
        return 0

    udalost_data = udalost.dict(exclude_unset=True)

    for key, value in udalost_data.items():
        setattr(existing_udalost, key, value)

    session.add(existing_udalost)
    session.commit()
    session.refresh(existing_udalost)

    return existing_udalost


def delete_udalost(session: Session, udalost_id: int):

    udalost = session.get(Udalost, udalost_id)

    if not udalost:
        return 0

    session.delete(udalost)
    session.commit()

    return 1


def list_udalosti(session: Session):

    udalosti = session.exec(select(Udalost)).all()

    return udalosti
