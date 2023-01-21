from sqlalchemy.orm import Session

from db.models.druh_pojisteni import DruhPojisteni
from schemas.druh_pojisteni import UpravDruhPojisteni
from schemas.druh_pojisteni import VytvorDruhPojisteni
from schemas.druh_pojisteni import ZobrazDruhPojisteni


def vytvor_novy_druh_pojisteni(
    druh_pojisteni: VytvorDruhPojisteni,
    db: Session,
    # owner_id: int
):

    """Vytvori novy druh pojisteni"""

    druh_pojisteni_object = DruhPojisteni(**druh_pojisteni.dict())
    db.add(druh_pojisteni_object)
    db.commit()
    db.refresh(druh_pojisteni_object)

    return druh_pojisteni_object


def najdi_druh_pojisteni(id: int, db: Session):

    """TODO......."""

    item = db.query(DruhPojisteni).filter(DruhPojisteni.id == id).first()
    return item


def list_druh_pojisteni(db: Session):

    """TODO......."""

    druh_pojisteni = db.query(DruhPojisteni).all()
    return druh_pojisteni


def zaloz_novy_druh_pojisteni(
    id: int, druh_pojisteni: UpravDruhPojisteni, db: Session, owner_id
):

    """Upravit pojisteni podle id"""

    existing_pojisteni = db.query(DruhPojisteni).filter(DruhPojisteni.id == id)

    if not existing_pojisteni:
        return 0

    """Nacteme json jako dictionary a vyfiltrujeme None"""
    payload = {k: v for k, v in pojisteni.__dict__.items() if v is not None}
    print(payload)

    existing_pojisteni.update(payload)
    db.commit()
    return 1


def uprav_druh_pojisteni_dle_id(
    id: int, druh_pojisteni: UpravDruhPojisteni, db: Session, owner_id
):

    """Upravit pojisteni podle id"""

    existing_pojisteni = db.query(DruhPojisteni).filter(DruhPojisteni.id == id)

    if not existing_pojisteni:
        return 0

    """Nacteme json jako dictionary a vyfiltrujeme None"""
    print(f"PRINTED FROM pojisteni.py {druh_pojisteni.__dict__}")

    payload = {k: v for k, v in druh_pojisteni.__dict__.items() if v is not None}
    # print(payload)

    existing_pojisteni.update(payload)
    db.commit()
    return 1


def vymaz_druh_pojisteni_dle_id(id: int, db: Session, owner_id: int):

    """Vymaze pojisteni"""

    existing_pojisteni = db.query(DruhPojisteni).filter(DruhPojisteni.id == id)

    if not existing_pojisteni:
        return 0

    existing_pojisteni.delete(synchronize_session=False)
    db.commit()
    return 1
