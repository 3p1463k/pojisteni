from sqlalchemy import select
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.pojistenec import Pojistenec
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence


def vytvor_admina(pojistenec: VytvorPojistence, db: Session):
    pojistenec = Pojistenec(
        jmeno=pojistenec.jmeno,
        prijmeni=pojistenec.prijmeni,
        ulice=pojistenec.ulice,
        mesto=pojistenec.mesto,
        psc=pojistenec.psc,
        telefon=pojistenec.telefon,
        email=pojistenec.email,
        hashed_password=Hasher.get_password_hash(pojistenec.password),
        is_active=True,
        is_superuser=True,
    )

    db.add(pojistenec)
    db.commit()
    db.refresh(pojistenec)

    return pojistenec
