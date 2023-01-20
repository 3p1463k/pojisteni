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
from db.repository.pojisteni import list_pojisteni
from db.repository.pojisteni import najdi_pojisteni
from db.repository.pojisteni import uprav_pojisteni_dle_id
from db.repository.pojisteni import vymaz_pojisteni_dle_id
from db.repository.pojisteni import vytvor_nove_pojisteni
from db.session import get_db
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni
from schemas.pojisteni import ZobrazPojisteni


pojisteni_router = APIRouter(prefix="", tags=["pojisteni-api"])
templates = Jinja2Templates(directory="templates")


@pojisteni_router.get("/pojisteni/{id}", response_model=ZobrazPojisteni)
def nacti_detail_pojisteni(id: int, db: Session = Depends(get_db)):

    """Nacte detail jednotliveho pojisteni"""

    pojisteni = najdi_pojisteni(id=id, db=db)

    if not pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s  id {id} neexistuje",
        )

    return pojisteni


@pojisteni_router.get("/pojisteni/vse/", response_model=List[ZobrazPojisteni])
def zobrazit_dostupna_pojisteni(db: Session = Depends(get_db)):

    """Zobrazi vsechna dostupna pojisteni"""

    pojisteni = list_pojisteni(db=db)

    return pojisteni


@pojisteni_router.post("/pojisteni/vytvor/", response_model=ZobrazPojisteni)
def vytvor_pojisteni(
    pojisteni: VytvorPojisteni,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vytvori nove pojisteni TODOn admin rights only"""
    # current_user_is_admin = db.is_superuser==True
    # if current_user_is_admin:
    #       do stuff
    print(current_user.id)

    pojisteni = vytvor_nove_pojisteni(
        pojisteni=pojisteni, db=db, owner_id=current_user.id
    )

    return pojisteni


@pojisteni_router.put("/pojisteni/uprava/{id}")
def uprav_pojisteni(
    id: int,
    pojisteni: UpravPojisteni,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Uprava pojisteni"""

    pojisteni1 = najdi_pojisteni(id=id, db=db)
    print(pojisteni.__dict__)

    if not pojisteni1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s id {id} nenalezeno",
        )

    message = uprav_pojisteni_dle_id(
        id=id,
        pojisteni=pojisteni,
        db=db,
        owner_id=current_user.id,
    )

    return {"msg": "Successfully updated data."}


@pojisteni_router.delete("/pojisteni/vymazat/{id}")
def vymaz_pojisteni(
    id: int,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vymaze pojisteni z databaze podle id"""

    message = vymaz_pojisteni_dle_id(id=id, db=db, owner_id=current_user.id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s id {id} nenalezeno",
        )

    #    print(current_user.id, current_user.is_superuser)

    if current_user and current_user.is_superuser:

        vymaz_pojisteni_dle_id(id=id, db=db, owner_id=current_user.id)

        return {"msg": "Successfully deleted."}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not permitted!!!!",
        )
