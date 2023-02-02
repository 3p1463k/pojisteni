from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.repository.pojisteni import (
    create_pojisteni_admin,
)  # , najdi_vse_pojisteni_pojistence
from db.repository.pojisteni import delete_pojisteni
from db.repository.pojisteni import find_pojisteni
from db.repository.pojisteni import list_pojisteni
from db.repository.pojisteni import update_pojisteni
from db.session import get_session
from schemas.pojistenec import VytvorPojistence
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni
from schemas.pojisteni import ZobrazPojisteni

#


router = APIRouter(prefix="", tags=["pojisteni-api"])
templates = Jinja2Templates(directory="templates")


@router.post("/pojisteni/vytvor/")
def vytvor_pojisteni(
    *,
    session: Session = Depends(get_session),
    pojisteni: VytvorPojisteni,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vytvori nove pojisteni TODOn admin rights only"""

    if current_user and current_user.is_superuser:

        pojisteni = create_pojisteni_admin(session, pojisteni)

        return {"msg": "Pojisteni uspesne vytvoreno."}

    raise HTTPException(
        status_code=403, detail="Unauthorized - Nepovoleno, nemate opravneni"
    )


@router.get("/pojisteni/{pojisteni_id}", response_model=ZobrazPojisteni)
def get_pojisteni(*, session: Session = Depends(get_session), pojisteni_id: int):
    """Nacte detail jednotliveho pojisteni"""

    pojisteni = find_pojisteni(session, pojisteni_id)

    if not pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s  id {pojisteni_id} neexistuje",
        )

    return pojisteni


@router.patch("/pojisteni/uprava/{pojisteni_id}")
def uprav_pojisteni(
    pojisteni_id: int,
    pojisteni: UpravPojisteni,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uprava pojisteni"""

    if current_user and current_user.is_superuser:

        message = update_pojisteni(session, pojisteni_id, pojisteni=pojisteni)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojisteni s id {pojisteni_id} nenalezeno",
            )

        return {"msg": "Successfully updated data."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not permitted!!!!"
    )


@router.delete("/pojisteni/vymazat/{pojisteni_id}")
def delete_pojisteni_admin(
    *,
    pojisteni_id: int,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """Vymaze pojisteni z databaze podle id"""

    if current_user and current_user.is_superuser:

        message = delete_pojisteni(session, pojisteni_id)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojisteni s id {id} nenalezeno",
            )

        msg = f"Successfully deleted data - pojisteni id: {pojisteni_id}."
        return {"msg": msg}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/pojisteni/vse/", response_model=List[ZobrazPojisteni])
def zobrazit_vsechns_pojisteni(session: Session = Depends(get_session)):

    """Zobrazi vsechna pojisteni"""

    pojisteni = list_pojisteni(session=session)

    if not pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zadna pojisteni nenalezena",
        )

    return pojisteni


# @pojisteni_router.get("/pojisteni/pojistenec/vse/", response_model=List[ZobrazPojisteni])
# def zobraz_pojisteni_pojistence(pojistenec_id:int, db: Session = Depends(get_db)):
#
#     """Zobrazi vsechna dostupna pojisteni pojistence"""
#
#     pojisteni = najdi_vse_pojisteni_pojistence(pojistenec_id, db=db)
#
#     return pojisteni
