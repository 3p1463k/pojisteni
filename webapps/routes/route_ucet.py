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
from db.models.udalost import Udalost
from db.repository.pojistenec import najdi_pojistence
from db.session import get_db
from schemas.pojistenec import ZobrazPojistence


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["ucet-uzivatel"], include_in_schema=False)


@router.get("/uzivatel/")
async def pojistenci_ucet(
    request: Request,
    db: Session = Depends(get_db),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    moje_pojisteni = db.query(Pojisteni).filter(Pojisteni.owner_id == current_user.id)

    moje_udalosti = db.query(Udalost).filter(Udalost.owner_id == current_user.id)

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
    db: Session = Depends(get_db),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    moje_udalosti = db.query(Udalost).filter(Udalost.owner_id == current_user.id)

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
    db: Session = Depends(get_db),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    moje_pojisteni = db.query(Pojisteni).filter(Pojisteni.owner_id == current_user.id)

    context = {
        "request": request,
        "msg": msg,
        "moje_pojisteni": moje_pojisteni,
        "current_user": current_user,
    }

    return templates.TemplateResponse("ucet/pojisteni.html", context)
