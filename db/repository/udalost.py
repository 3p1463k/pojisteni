from sqlalchemy.orm import Session

from db.models.udalost import Udalost
from schemas.udalost import VytvorUdalost
from schemas.udalost import ZobrazUdalost


def vytvor_novou_udalost(udalost: VytvorUdalost, db: Session, owner_id: int):

    """TDODO........"""
    udalost_object = Udalost(**udalost.dict(exclude={"owner_id"}), owner_id=owner_id)

    db.add(udalost_object)
    db.commit()
    db.refresh(udalost_object)

    return udalost_object


def najdi_udalost(id: int, db: Session):

    """TODO......."""

    item = db.query(Udalost).filter(Udalost.id == id).first()
    return item


def list_udalosti(db: Session) -> list[dict]:

    """TODO......."""

    udalosti = db.query(Udalost).all()
    return udalosti


def uprav_udalost_dle_id(id: int, udalost: VytvorUdalost, db: Session) -> bool:

    """Pouze admin muze upravit udalost"""

    existing_udalost = db.query(Udalost).filter(Udalost.id == id)

    if not existing_udalost.first():
        return 0

    """Nacteme json jako dictionary a vyfiltrujeme None"""
    payload = {k: v for k, v in udalost.__dict__.items() if v is not None}
    existing_udalost.update(payload)
    db.commit()
    return 1


def vymaz_udalost_dle_id(id: int, db: Session) -> bool:

    """Vymaze pojisteni"""

    existing_udalost = db.query(Udalost).filter(Udalost.id == id)

    if not existing_udalost.first():
        return 0

    existing_udalost.delete(synchronize_session=False)
    db.commit()
    return 1
