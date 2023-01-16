from sqlalchemy.orm import Session

from schemas.udalost import VytvorUdalost, ZobrazUdalost
from db.models.udalost import Udalost


def vytvor_novou_udalost(

        udalost:VytvorUdalost,
        db:Session,
        owner_id: int
):
    
    """TDODO........"""
     
    udalost_object = Udalost(**udalost.dict(), owner_id = owner_id)
    db.add(udalost_object)
    db.commit()
    db.refresh(udalost_object)
    
    return udalost_object
    



def najdi_udalost(id:int,db:Session):

    """TODO......."""
    
    item = db.query(Udalost).filter(Udalost.id == id).first()
    return item


def list_udalosti(db : Session):

    """TODO......."""
    
    udalosti = db.query(Udalosti).all()
    return udalosti


def uprav_udalost_dle_id(id:int, udalost: VytvorUdalost, db: Session):

    """TODO............"""
    
    existing_udalost = db.query(udalost).filter(udalost.id == id)
    
    if not existing_udalost.first():
        return 0
    
    existing_udalost.update(udalost.__dict__)
    db.commit()
    return 1


def vymaz_udalost_dle_id(id: int,db: Session):
    
    """Vymaze pojisteni"""
    
    existing_udalost = db.query(Udalost).filter(Udalost.id == id)
    
    if not existing_udalost.first():
        return 0
    
    existing_udalost.delete(synchronize_session=False)
    db.commit()
    return 1

