from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.dataclasses import dataclass
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import get_current_user_from_token
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.repository.pojistenec import list_pojistence
from db.repository.pojistenec import najdi_pojistence
from db.repository.pojistenec import uprav_pojistence_dle_id
from db.repository.pojistenec import vymaz_pojistence_dle_id
from db.repository.pojistenec import vytvor_noveho_pojistence
from db.session import get_db
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence


pojistenci_router = APIRouter(prefix="", tags=["pojistenci-api"])
templates = Jinja2Templates(directory="templates")


@pojistenci_router.get("/pojistenci/{id}", response_model=ZobrazPojistence)
def nacti_pojistence(id: int, db: Session = Depends(get_db)):

    """Nacte detail jednotliveho pojisteni"""

    pojistenec = najdi_pojistence(id=id, db=db)

    if not pojistenec:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojistenec s  id {id} neexistuje",
        )

    return pojistenec


@pojistenci_router.get("/pojistenci/vse/", response_model=List[ZobrazPojistence])
def zobrazit_pojistence(db: Session = Depends(get_db)):

    """Zobrazi vsechna dostupna pojisteni"""

    pojistenci = list_pojistence(db=db)

    return pojistenci


@pojistenci_router.post("/pojistenci/vytvorit/", response_model=ZobrazPojistence)
async def vytvorit_pojistence(
    pojistenec: VytvorPojistence,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vytvori noveho pojistence"""

    pojistenec = vytvor_noveho_pojistence(pojistenec=pojistenec, db=db)

    return pojistenec


@pojistenci_router.put("/pojistenci/uprava/{id}")
async def upravit_pojistence(
    id: int,
    pojistenec: UpravPojistence,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Uprava pojistence"""

    pojistenec_existuje = najdi_pojistence(id=id, db=db)

    if not pojistenec_existuje:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojistenec s id {id} neexistuje",
        )

    message = uprav_pojistence_dle_id(
        id=id,
        pojistenec=pojistenec,
        db=db,
    )

    if message:
        return {"msg": "Successfully updated data."}

    return {"msg": "Can't be a 0"}


@pojistenci_router.delete("/pojistenci/vymazat/{id}")
async def vymazat_pojistence(
    id: int,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vymaze pojistence dle id"""

    message = vymaz_pojistence_dle_id(id=id, db=db)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojistenec s id {id} nenalezen",
        )

    #    if current_user.is_superuser:
    if current_user.id:

        vymaz_pojistence_dle_id(id=id, db=db)

        return {"msg": "Successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )
