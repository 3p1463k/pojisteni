from sqlmodel import select
from sqlmodel import Session

from db.models.pojistenec import Pojistenec
from db.session import engine


def najdi_pojistence_dle_emailu(email: str, session: Session):

    """Funkce pro vyhledani uzivatele pro login"""

    with Session(engine) as session:
        # statement = select(Pojistenec).where(Pojistenec.email == email)
        # pojistenec = session.exec(statement)
        pojistenec1 = (
            session.query(Pojistenec).filter(Pojistenec.email == email).first()
        )

        return pojistenec1
