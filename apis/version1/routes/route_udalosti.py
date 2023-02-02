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
from db.repository.udalost import create_udalost_admin
from db.repository.udalost import delete_udalost
from db.repository.udalost import find_udalost
from db.repository.udalost import list_udalosti
from db.repository.udalost import update_udalost
from db.session import get_session
from schemas.udalost import UpravUdalost
from schemas.udalost import VytvorUdalost
from schemas.udalost import ZobrazUdalost


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["udalosti-api"])


@router.post("/udalosti/vytvor/", response_model=ZobrazUdalost)
async def vytvorit_udalost(
    *,
    udalost: VytvorUdalost,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Admin muze vytvorit udalost a pridelit pojistenec_id"""

    if current_user and current_user.is_superuser:

        udalost = create_udalost_admin(session, udalost)

        return {"msg": "Udalost uspesne vytvorena."}

    raise HTTPException(
        status_code=403, detail="Unauthorized - Nepovoleno, nemate opravneni"
    )


@router.get("/udalosti/{udalost_id}")
async def udalost(*, session: Session = Depends(get_session), udalost_id: int):
    """Zobrazi udalost dle id"""
    pass

    udalost = find_udalost(session, udalost_id)

    if not udalost:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Udalost s  id {udalost_id} neexistuje",
        )

    return udalost


@router.patch("/udalosti/uprav/{udalost_id}")
async def upravit_udalost(
    udalost_id: int,
    udalost: UpravUdalost,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Upravi existujici udalost"""

    if current_user and current_user.is_superuser:

        message = update_udalost(session, udalost_id, udalost)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Udalost s id {udalost_id} nenalezena",
            )

        return {"msg": "Successfully updated data."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )


@router.delete("/udalosti/vymaz/")
async def vymazat_udalost(
    *,
    udalost_id: int,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vymaze udalost"""
    if current_user and current_user.is_superuser:

        message = delete_udalost(session, udalost_id)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Udalost s id {udalost_id} nenalezeno",
            )

        return {"msg": "Successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )


@router.get("/udalosti/vse/", response_model=List[ZobrazUdalost])
def zobrazit_udalosti(session: Session = Depends(get_session)):

    """Zobrazi vsechny udalosti"""

    udalosti = list_udalosti(session)

    return udalosti
