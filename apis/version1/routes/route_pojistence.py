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
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from db.models.pojistenec import Pojistenec
from db.models.pojistenec import PojistenecOut
from db.repository.pojistenec import create_pojistenec
from db.repository.pojistenec import delete_pojistence
from db.repository.pojistenec import find_pojistenec
from db.repository.pojistenec import list_pojistence
from db.repository.pojistenec import update_pojistence
from db.session import get_session
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence


router = APIRouter(prefix="", tags=["pojistenci-api"])
templates = Jinja2Templates(directory="templates")


@router.post("/pojistenec/vytvorit/", response_model=PojistenecOut)
async def vytvorit_pojistence(
    *,
    pojistenec: VytvorPojistence,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vytvori pojistence"""

    if current_user and current_user.is_superuser:

        pojistenec = create_pojistenec(session, pojistenec)

        return pojistenec

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/pojistenec/{pojistenec_id}", response_model=ZobrazPojistence)
def get_pojistence(*, session: Session = Depends(get_session), pojistenec_id: int):
    """Nacte pojistence"""

    pojistenec = find_pojistenec(session, pojistenec_id)

    if not pojistenec:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojistenec s  id {pojistenec_id} neexistuje",
        )

    return pojistenec


@router.patch("/pojistenec/uprava/{pojistenec_id}", response_model=ZobrazPojistence)
async def upravit_pojistence(
    pojistenec_id: int,
    pojistenec: UpravPojistence,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uprava pojistence"""

    if current_user and current_user.is_superuser:

        message = update_pojistence(session, pojistenec_id, pojistenec)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojistenec s id {id} neexistuje",
            )

        return {"msg": "Successfully updated data."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.delete("/pojistenec/vymazat/{pojistenec_id}")
async def vymazat_pojistence(
    *,
    pojistenec_id: int,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vymaze pojistence dle id"""

    if current_user and current_user.is_superuser:

        message = delete_pojistence(session, pojistenec_id)

        response = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojistenec s id {pojistenec_id} nenalezen",
        )

        if not message:
            return response

        msg = f"Successfully deleted pojistenec : {pojistenec_id}."
        return {"msg": msg}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Nepovoleno - You are not permitted!!!",
    )


@router.get("/pojistenci/vse/", response_model=List[ZobrazPojistence])
def zobrazi_vsechny_pojistence(session: Session = Depends(get_session)):

    """Zobrazi vsechna pojisteni"""

    pojistenci = list_pojistence(session)

    return pojistenci
