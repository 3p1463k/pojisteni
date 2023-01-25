from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import get_current_user_from_token
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.repository.druh_pojisteni import list_druh_pojisteni
from db.repository.druh_pojisteni import najdi_druh_pojisteni
from db.repository.druh_pojisteni import uprav_druh_pojisteni_dle_id
from db.repository.druh_pojisteni import vymaz_druh_pojisteni_dle_id
from db.repository.druh_pojisteni import vytvor_novy_druh_pojisteni
from db.session import get_db
from schemas.druh_pojisteni import UpravDruhPojisteni
from schemas.druh_pojisteni import VytvorDruhPojisteni
from schemas.druh_pojisteni import ZobrazDruhPojisteni


router = APIRouter(prefix="", tags=["pojisteni-druh-api"])
templates = Jinja2Templates(directory="templates")


@router.get("/pojisteni/druh/{id}", response_model=ZobrazDruhPojisteni)
def nacti_detail_druh_pojisteni(id: int, db: Session = Depends(get_db)):

    """Nacte detail jednotliveho pojisteni"""

    druh_pojisteni = najdi_druh_pojisteni(id=id, db=db)

    if not druh_pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s  id {id} neexistuje",
        )

    return druh_pojisteni


@router.get("/pojisteni/druh/vse/", response_model=List[ZobrazDruhPojisteni])
def zobrazit_dostupna_pojisteni(db: Session = Depends(get_db)):

    """Zobrazi vsechny dostupne druhy pojisteni"""

    druh_pojisteni = list_druh_pojisteni(db=db)

    return druh_pojisteni


@router.post("/pojisteni/druh/vytvor/", response_model=ZobrazDruhPojisteni)
def vytvor_druh_pojisteni(
    druh_pojisteni: VytvorDruhPojisteni,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vytvori druh pojisteni"""

    druh_pojisteni = vytvor_novy_druh_pojisteni(
        druh_pojisteni=druh_pojisteni,
        db=db,
    )

    return druh_pojisteni


@router.put("/pojisteni/druh/uprava/{id}")
def uprav_druh_pojisteni(
    id: int,
    druh_pojisteni: UpravDruhPojisteni,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uprava pojisteni"""

    druh_pojisteni1 = najdi_druh_pojisteni(id=id, db=db)
    print(druh_pojisteni.__dict__)

    if not druh_pojisteni1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s id {id} nenalezeno",
        )

    message = uprav_druh_pojisteni_dle_id(
        id=id, druh_pojisteni=druh_pojisteni, db=db, owner_id=current_user.id
    )

    return {"msg": "Successfully updated data."}


@router.delete("/pojisteni/druh/vymazat/{id}")
def vymaz_druh_pojisteni(
    id: int,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vymaze pojisteni z databaze podle id"""

    message = vymaz_druh_pojisteni_dle_id(id=id, db=db)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s id {id} nenalezeno",
        )

    if current_user and current_user.is_superuser:

        vymaz_druh_pojisteni_dle_id(id=id, db=db)

        return {"msg": "Successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )
