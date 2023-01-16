from sqlalchemy.orm import Session
from db.models.pojistenec import Pojistenec


def najdi_pojistence_dle_emailu(email: str, db: Session):

    """Funkce pro vyhledani uzivatele pro login"""

    pojistenec = db.query(Pojistenec).filter(Pojistenec.email == email).first()

    return pojistenec
