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
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from db.models.pojistenec import Pojistenec
from db.models.udalost import Udalost
from db.repository.udalost import create_udalost_user
from db.session import get_session
from schemas.udalost import VytvorUdalost
from webapps.auth.forms import UdalostForm


templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="", tags=["udalost-zalozit-webapp"], include_in_schema=False)


@router.get("/udalost/zalozit/")
async def zaloz_udalost(
    request: Request,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uzivatel si muze zalozit udalost"""

    context = {"request": request, "current_user": current_user}

    return templates.TemplateResponse("ucet/zaloz_udalost.html", context)


@router.post("/udalost/zalozit/")
async def zalozit_udalost(
    request: Request,
    session: Session = Depends(get_session),
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacteme novou udalost a ulozime do databaze"""

    form = UdalostForm(request)
    await form.load_data()

    if await form.is_valid():

        udalost = VytvorUdalost(
            nazev=form.nazev,
            popis=form.popis,
            skoda=form.skoda,
            pojistenec_id=current_user.id,
        )

        try:
            udalost = create_udalost_user(session, udalost)

            return responses.RedirectResponse(
                "/uzivatel?msg=Udalost-uspesne-zalozena",
                status_code=status.HTTP_302_FOUND,
            )

        except IntegrityError:

            form.__dict__.get("errors").append("Duplicate username or email")

            return templates.TemplateResponse("ucet/zaloz_udalost.html", form.__dict__)

    return templates.TemplateResponse("pojisteni/zaloz_udalost.html", form.__dict__)
