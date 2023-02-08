from sqlmodel import select
from sqlmodel import Session

from core.hashing import Hasher
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.session import engine
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence


def create_pojistenec(session: Session, pojistenec: VytvorPojistence):

    pojistenec_data = pojistenec.dict()
    hashed_password = Hasher.get_password_hash(pojistenec_data["password"])
    pojistenec_data["hashed_password"] = hashed_password
    del pojistenec_data["password"]

    pojistenec1 = Pojistenec()

    for key, value in pojistenec_data.items():
        setattr(pojistenec1, key, value)

    session.add(pojistenec1)
    session.commit()
    session.refresh(pojistenec1)

    return pojistenec


def find_pojistenec(session: Session, pojistenec_id: int):

    pojistenec = session.get(Pojistenec, pojistenec_id)

    if not pojistenec:
        return 0

    return pojistenec


def update_pojistence(
    session: Session, pojistenec_id: int, pojistenec: UpravPojistence
):

    existing_pojistenec = session.get(Pojistenec, pojistenec_id)

    if not existing_pojistenec:
        return 0

    pojistenec_data = pojistenec.dict(exclude_unset=True)

    for key, value in pojistenec_data.items():
        setattr(existing_pojistenec, key, value)

    session.add(existing_pojistenec)
    session.commit()
    session.refresh(existing_pojistenec)
    return existing_pojistenec


def delete_pojistence(session: Session, pojistenec_id: int):

    pojistenec = session.get(Pojistenec, pojistenec_id)

    if not pojistenec:
        return 0

    session.delete(pojistenec)
    session.commit()
    return 1


def list_pojistence(session):

    pojistenci = session.exec(select(Pojistenec)).all()

    return pojistenci
