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
from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.repository.druh_pojisteni import create_druh_pojisteni
from db.repository.druh_pojisteni import delete_druh_pojisteni
from db.repository.druh_pojisteni import find_druh_pojisteni
from db.repository.druh_pojisteni import list_druhy_pojisteni
from db.repository.druh_pojisteni import update_druh_pojisteni
from db.session import get_session
from schemas.druh_pojisteni import UpravDruhPojisteni
from schemas.druh_pojisteni import VytvorDruhPojisteni
from schemas.druh_pojisteni import ZobrazDruhPojisteni


router = APIRouter(prefix="", tags=["pojisteni-druh-api"])
templates = Jinja2Templates(directory="templates")


@router.post("/pojisteni/druh/vytvor/")
def vytvor_druh_pojisteni(
    *,
    session: Session = Depends(get_session),
    druh_pojisteni: VytvorDruhPojisteni,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vytvori druh pojisteni"""

    druh_pojisteni = create_druh_pojisteni(session, druh_pojisteni)

    return druh_pojisteni


@router.get("/pojisteni/druh/{druh_pojisteni_id}", response_model=ZobrazDruhPojisteni)
def get_druh_pojisteni(
    *, session: Session = Depends(get_session), druh_pojisteni_id: int
):
    """Nacte detail jednotliveho pojisteni"""

    druh_pojisteni = find_druh_pojisteni(session, druh_pojisteni_id)

    if not druh_pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s  id {druh_pojisteni_id} neexistuje",
        )

    return druh_pojisteni


@router.patch("/pojisteni/druh/uprava/{druh_pojisteni_id}")
def uprav_druh_pojisteni(
    druh_pojisteni_id: int,
    druh_pojisteni: UpravDruhPojisteni,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uprava pojisteni"""

    message = update_druh_pojisteni(session, druh_pojisteni_id, druh_pojisteni)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s id {druh_pojisteni_id} nenalezeno",
        )

    return {"msg": "Successfully updated data."}


@router.delete("/pojisteni/druh/vymazat/{druh_pojisteni_id}")
def vymaz_druh_pojisteni(
    *,
    session: Session = Depends(get_session),
    druh_pojisteni_id: int,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vymaze pojisteni z databaze podle id"""

    if current_user and current_user.is_superuser:

        message = delete_druh_pojisteni(session, druh_pojisteni_id)

        if not message:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojisteni s id {druh_pojisteni_id} nenalezeno",
            )

        return {"msg": "Successfully deleted."}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/pojisteni/druh/vse/", response_model=List[ZobrazDruhPojisteni])
def zobrazit_dostupna_pojisteni(session: Session = Depends(get_session)):

    """Zobrazi vsechny dostupne druhy pojisteni"""

    druh_pojisteni = list_druhy_pojisteni(session)

    return druh_pojisteni
