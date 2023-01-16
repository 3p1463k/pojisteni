from sqlalchemy import select
from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.pojistenec import Pojistenec
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence


def vytvor_noveho_pojistence(pojistenec: VytvorPojistence, db: Session):

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
        is_superuser=False,
    )

    db.add(pojistenec)
    db.commit()
    db.refresh(pojistenec)

    return pojistenec


def najdi_pojistence_dle_emailu(email: str, db: Session):

    """Najde pojistence dle emailu"""

    pojistenec = db.query(Pojistenec).filter(Pojistenec.email == email).first()
    print(f"{pojistenec} PRINTED from repository pojistenec.py")

    return pojistenec


def uprav_pojistence_dle_id(id: int, pojistenec: UpravPojistence, db: Session):

    """Upravi pojistence dle id"""

    with db as session:

        statement = select(Pojistenec).where(Pojistenec.id == id)
        results = session.execute(statement)  #

        print(results)

        # db.commit()

        return 1


def vymaz_pojistence_dle_id(id: int, db: Session):

    """Vymaze pojistence"""

    existing_pojistenec = db.query(Pojistenec).filter(Pojistenec.id == id)

    if not existing_pojistenec.first():
        return 0

    existing_pojistenec.delete()
    db.commit()
    return 1


def najdi_pojistence(id: int, db: Session):

    """Vymaze pojistence"""

    existing_pojistenec = db.query(Pojistenec).get(id)

    print(f"ID je : { id}")
    print(existing_pojistenec)

    # if not existing_pojistenec.first():
    #   return 0

    return existing_pojistenec


def list_pojistence(db: Session):

    """TODO......."""

    pojistenci = db.query(Pojistenec).all()
    return pojistenci
