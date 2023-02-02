from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.repository.pojisteni import create_pojisteni_user
from db.repository.pojisteni import delete_pojisteni
from db.repository.pojisteni import find_pojisteni
from db.repository.pojisteni import list_pojisteni
from db.repository.pojisteni import update_pojisteni
from db.session import get_session
from schemas.pojisteni import UpravPojisteni
from schemas.pojisteni import VytvorPojisteni
from schemas.pojisteni import ZobrazPojisteni
from webapps.auth.forms import PojisteniForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["zalozit-webapp"], include_in_schema=False)


@router.get("/pojisteni/zalozit/")
async def zaloz_pojisteni(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uzivatel si muze zalozit pojisteni"""

    seznam_pojistek = session.query(DruhPojisteni).all()

    context = {
        "request": request,
        "current_user": current_user,
        "seznam_pojistek": seznam_pojistek,
    }

    return templates.TemplateResponse("ucet/zaloz_pojisteni.html", context)


@router.post("/pojisteni/zalozit/")
async def zalozit_pojisteni(
    request: Request,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacti druh zvoleneho pojisteni z formulare"""

    form = PojisteniForm(request)
    await form.load_data()

    if await form.is_valid():

        """Zkontroluj jestli pojisteni jiz neexistuje"""

        if (
            session.query(Pojisteni)
            .filter(Pojisteni.pojistenec_id == current_user.id)
            .filter(Pojisteni.nazev == form.nazev)
            .first()
        ):

            form.__dict__.update(msg="Pojisteni-jiz-existuje")

            return RedirectResponse(
                url="/uzivatel?msg=Pojisteni-jiz-existuje",
                status_code=status.HTTP_303_SEE_OTHER,
            )

        else:
            druh_pojisteni = (
                session.query(DruhPojisteni)
                .filter(DruhPojisteni.nazev == form.nazev)
                .first()
            )

            pojisteni = VytvorPojisteni(
                nazev=druh_pojisteni.nazev,
                popis=druh_pojisteni.popis,
                cena=druh_pojisteni.cena,
                pojistenec_id=current_user.id,
            )

            pojisteni = create_pojisteni_user(session, pojisteni)

            form.__dict__.update(msg="Pojisteni uspesne zalozeno")

            return RedirectResponse(
                "/uzivatel?msg=Pojisteni-uspesne-zalozeno",
                status_code=status.HTTP_302_FOUND,
            )

    return RedirectResponse(
        "/pojisteni/zalozit/?msg=Vyberte-pojisteni",
        status_code=status.HTTP_302_FOUND,
    )
