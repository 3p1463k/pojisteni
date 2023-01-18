from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import login_for_access_token
from db.repository.pojistenec import vytvor_noveho_pojistence
from db.session import get_db
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence
from webapps.auth.forms import RegistraceForm


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
    tags=["webapp"],
    include_in_schema=False,
)


@router.get("/registr/")
async def registrace(request: Request):

    """GET request na zobrazeni formulare registrace"""

    context = {"request": request}

    return templates.TemplateResponse("general_pages/registrace.html", context)


@router.post("/registr/")
async def registrace(request: Request, db: Session = Depends(get_db)):

    """POST request na ulozeni formulare registrace"""

    form = RegistraceForm(request)
    await form.load_data()

    if await form.is_valid():

        pojistenec = VytvorPojistence(
            jmeno=form.jmeno,
            prijmeni=form.prijmeni,
            ulice=form.ulice,
            mesto=form.mesto,
            psc=form.psc,
            telefon=form.telefon,
            email=form.email,
            password=form.password,
        )

        try:

            pojistenec = vytvor_noveho_pojistence(pojistenec=pojistenec, db=db)

            return responses.RedirectResponse(
                "/uzivatel?msg=Registrace-byla-uspesna",
                status_code=status.HTTP_302_FOUND,
            )

        except IntegrityError:

            form.__dict__.get("errors").append("Duplicate username or email")

            return templates.TemplateResponse(
                "general_pages/registrace.html", form.__dict__
            )

    return templates.TemplateResponse("general_pages/registrace.html", form.__dict__)
