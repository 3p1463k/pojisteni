from sqlalchemy.orm import Session

from db.models.pojisteni import Pojisteni
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni
from schemas.pojisteni import ZobrazPojisteni


def vytvor_nove_pojisteni(pojisteni: VytvorPojisteni, db: Session, owner_id: int):

    """TDODO........"""

    pojisteni_object = Pojisteni(**pojisteni.dict(), owner_id=owner_id)
    db.add(pojisteni_object)
    db.commit()
    db.refresh(pojisteni_object)

    return pojisteni_object


def najdi_pojisteni(id: int, db: Session):

    """TODO......."""

    item = db.query(Pojisteni).filter(Pojisteni.id == id).first()
    return item


def list_pojisteni(db: Session):

    """TODO......."""

    pojisteni = db.query(Pojisteni).all()
    return pojisteni


def zaloz_nove_pojisteni(id: int, pojisteni: UpravPojisteni, db: Session, owner_id):

    """Upravit pojisteni podle id"""

    existing_pojisteni = db.query(Pojisteni).filter(Pojisteni.id == id)

    if not existing_pojisteni:
        return 0

    """Nacteme json jako dictionary a vyfiltrujeme None"""
    payload = {k: v for k, v in pojisteni.__dict__.items() if v is not None}
    print(payload)

    existing_pojisteni.update(payload)
    db.commit()
    return 1


def uprav_pojisteni_dle_id(id: int, pojisteni: UpravPojisteni, db: Session, owner_id):

    """Upravit pojisteni podle id"""

    existing_pojisteni = db.query(Pojisteni).filter(Pojisteni.id == id)

    if not existing_pojisteni:
        return 0

    """Nacteme json jako dictionary a vyfiltrujeme None"""
    payload = {k: v for k, v in pojisteni.__dict__.items() if v is not None}
    print(payload)

    existing_pojisteni.update(payload)
    db.commit()
    return 1


def vymaz_pojisteni_dle_id(id: int, db: Session, owner_id):

    """Vymaze pojisteni"""

    existing_pojisteni = db.query(Pojisteni).filter(Pojisteni.id == id)

    if not existing_pojisteni:
        return 0

    existing_pojisteni.delete(synchronize_session=False)
    db.commit()
    return 1
