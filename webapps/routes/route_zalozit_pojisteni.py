from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.repository.pojisteni import list_pojisteni
from db.repository.pojisteni import najdi_pojisteni
from db.repository.pojisteni import uprav_pojisteni_dle_id
from db.repository.pojisteni import vymaz_pojisteni_dle_id
from db.repository.pojisteni import vytvor_nove_pojisteni
from db.repository.pojisteni import zaloz_nove_pojisteni
from db.session import get_db
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni
from schemas.pojisteni import ZobrazPojisteni
from webapps.auth.forms import PojisteniForm

# from deta import Deta

# deta = Deta()

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="", tags=["zalozit-webapp"], include_in_schema=False)


@router.get("/pojisteni/zalozit/")
async def zaloz_pojisteni(
    request: Request,
    db: Session = Depends(get_db),
    msg: str = None,
    error: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    seznam_pojistek = db.query(DruhPojisteni).all()

    context = {
        "request": request,
        "current_user": current_user,
        "seznam_pojistek": seznam_pojistek,
    }

    return templates.TemplateResponse("ucet/zaloz_pojisteni.html", context)


@router.post("/pojisteni/zalozit/")
async def zalozit_pojisteni(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacti druh zvoleneho pojisteni z formulare"""

    form = PojisteniForm(request)
    await form.load_data()

    if await form.is_valid():

        # return "VALID FORM"
        """Zkontroluj jestli pojistwni jiz neexistuje"""

        if (
            db.query(Pojisteni)
            .filter(Pojisteni.owner_id == current_user.id)
            .filter(Pojisteni.nazev == form.nazev)
            .first()
        ):

            # form.__dict__.get("errors").append("Toto jiz mate zalozeno")
            form.__dict__.update(msg="Pojisteni-jiz-existuje")

            response = responses.RedirectResponse(
                url="/uzivatel?msg=Pojisteni-jiz-existuje",
                status_code=status.HTTP_303_SEE_OTHER,
            )

            return response

        else:
            druh_pojisteni = (
                db.query(DruhPojisteni)
                .filter(DruhPojisteni.nazev == form.nazev)
                .first()
            )

            pojisteni = VytvorPojisteni(
                nazev=druh_pojisteni.nazev,
                popis=druh_pojisteni.popis,
                cena=druh_pojisteni.cena,
            )

            pojisteni = vytvor_nove_pojisteni(
                pojisteni=pojisteni, db=db, owner_id=current_user.id
            )

            form.__dict__.update(msg="Pojisteni uspesne zalozeno")

            return responses.RedirectResponse(
                "/uzivatel?msg=Pojisteni-uspesne-zalozeno",
                status_code=status.HTTP_302_FOUND,
            )

    # print(form.__dict__["errors"])
    # return "NOK"

    return responses.RedirectResponse(
        "/pojisteni/zalozit/?msg=Vyberte-pojisteni",
        status_code=status.HTTP_302_FOUND,
    )
