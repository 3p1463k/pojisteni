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
from db.models.udalost import Udalost
from db.repository.udalost import list_udalosti
from db.repository.udalost import najdi_udalost
from db.repository.udalost import uprav_udalost_dle_id
from db.repository.udalost import vymaz_udalost_dle_id
from db.repository.udalost import vytvor_novou_udalost
from db.session import get_db
from schemas.udalost import UpravUdalost
from schemas.udalost import VytvorUdalost
from schemas.udalost import ZobrazUdalost


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["udalosti-api"])


@router.get("/udalosti/{id}")
async def udalost(
    id: int,
    db: Session = Depends(get_db),
):
    """Zobrazi udalost dle id"""

    udalost = najdi_udalost(id=id, db=db)

    if not udalost:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Udalost s  id {id} neexistuje",
        )

    return udalost


@router.get("/udalosti/vse/", response_model=List[ZobrazUdalost])
def zobrazit_udalosti(db: Session = Depends(get_db)):

    """Zobrazi vsechny udalosti"""

    udalosti = list_udalosti(db=db)

    return udalosti


@router.post("/udalosti/vytvor/", response_model=ZobrazUdalost)
async def vytvorit_udalost(
    udalost: VytvorUdalost,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vytvori novou udalost"""

    udalost = vytvor_novou_udalost(udalost=udalost, db=db, owner_id=current_user.id)

    return udalost


@router.put("/udalosti/uprav/{id}")
async def upravit_udalost(
    id: int,
    udalost: UpravUdalost,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Upravi existujici udalost"""

    if current_user and current_user.is_superuser:

        message = uprav_udalost_dle_id(
            id=id,
            udalost=udalost,
            db=db,
        )

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Udalost s id {id} nenalezena",
            )

        return {"msg": "Successfully updated data."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )

    udalost = vytvor_novou_udalost(udalost=udalost, db=db)

    return udalost


@router.delete("/udalosti/vymaz/")
async def vymazat_udalost(
    id: int,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vymaze udalost"""

    print(current_user.id, current_user.is_superuser)

    if current_user and current_user.is_superuser:

        message = vymaz_udalost_dle_id(id=id, db=db)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojisteni s id {id} nenalezeno",
            )

        return {"msg": "Successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )
