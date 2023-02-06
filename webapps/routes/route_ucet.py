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
from db.models.pojisteni import Pojisteni
from db.models.udalost import Udalost
from db.repository.pojistenec import find_pojistenec
from db.repository.pojisteni import find_pojisteni
from db.repository.pojisteni import list_pojisteni
from db.repository.udalost import find_udalost
from db.session import get_session
from schemas.pojistenec import ZobrazPojistence
from schemas.pojisteni import ZobrazPojisteni
from schemas.udalost import ZobrazUdalost


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["ucet-uzivatel"], include_in_schema=False)


@router.get("/uzivatel/")
async def pojistenci_ucet(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Prihlasime uzivatele a nacteme jeho pojisteni a udalosti"""

    moje_pojisteni = session.query(Pojisteni).filter(
        Pojisteni.pojistenec_id == current_user.id
    )

    moje_udalosti = session.query(Udalost).filter(
        Udalost.pojistenec_id == current_user.id
    )

    context = {
        "request": request,
        "msg": msg,
        "moje_udalosti": moje_udalosti,
        "moje_pojisteni": moje_pojisteni,
        "current_user": current_user,
    }

    return templates.TemplateResponse("ucet/uzivatel.html", context)


@router.get("/uzivatel/udalosti/")
async def ucet_udalosti(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uzivatel si muze zalozit udalost"""

    moje_udalosti = session.query(Udalost).filter(
        Udalost.pojistenec_id == current_user.id
    )

    context = {
        "request": request,
        "msg": msg,
        "moje_udalosti": moje_udalosti,
        "current_user": current_user,
    }

    return templates.TemplateResponse("ucet/udalosti.html", context)


@router.get("/uzivatel/pojisteni/")
async def ucet_pojisteni(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uzivatel muze zalozit pojisteni"""

    moje_pojisteni = session.query(Pojisteni).filter(
        Pojisteni.pojistenec_id == current_user.id
    )

    context = {
        "request": request,
        "msg": msg,
        "moje_pojisteni": moje_pojisteni,
        "current_user": current_user,
    }

    return templates.TemplateResponse("ucet/pojisteni.html", context)


@router.get("/uzivatel/pojisteni/{pojisteni_id}", response_model=ZobrazPojisteni)
def nacti_detail_pojisteni(
    request: Request,
    pojisteni_id: int,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte detail jednotliveho pojisteni"""

    pojisteni = find_pojisteni(session, pojisteni_id)

    context = {
        "request": request,
        "pojisteni": pojisteni,
        "current_user": current_user,
    }

    if not pojisteni:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pojisteni s  id {id} neexistuje",
        )

    return templates.TemplateResponse(
        "ucet/detail_pojisteni.html",
        context,
    )


@router.get("/uzivatel/udalosti/{udalost_id}", response_model=ZobrazUdalost)
def nacti_detail_pojisteni(
    request: Request,
    udalost_id: int,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte detail jednotliveho pojisteni"""

    udalosti = find_udalost(session, udalost_id)

    context = {
        "request": request,
        "udalosti": udalosti,
        "current_user": current_user,
    }

    if not udalosti:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Udalost s  id {udalost_id} neexistuje",
        )

    return templates.TemplateResponse(
        "ucet/detail_udalosti.html",
        context,
    )
