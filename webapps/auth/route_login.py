from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import login_for_access_token
from db.models.pojistenec import Pojistenec
from db.repository.login import najdi_pojistence_dle_emailu
from db.session import get_db
from webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["auth-webapp"], include_in_schema=False)


@router.get("/login/")
def user_login(request: Request):

    """Get request for login page"""

    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):

    """Nacteme formular pro prihlaseni"""

    form = LoginForm(request)
    await form.load_data()

    if await form.is_valid():

        try:
            email = str(form.username)
            pojistenec = db.query(Pojistenec).filter(Pojistenec.email == email).first()
            # pojistenec = najdi_pojistence_dle_emailu(email, db)
            # print(pojistenec.is_superuser)
            if pojistenec and pojistenec.is_superuser:

                form.__dict__.update(msg="Login Successful Vitej admine ")

                response = RedirectResponse(
                    "/admin/pojistenec/list?msg=Uspesne-prihlaseni",
                    status_code=status.HTTP_302_FOUND,
                )

                login_for_access_token(response=response, form_data=form, db=db)

                return response

            else:
                form.__dict__.update(msg="Login Successful Vitej uzivateli")

                response = RedirectResponse(
                    "/uzivatel?msg=Uspesne-prihlaseni",
                    status_code=status.HTTP_302_FOUND,
                )

                login_for_access_token(response=response, form_data=form, db=db)

                return response

        except HTTPException:

            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")

            return templates.TemplateResponse("auth/login.html", form.__dict__)

    return templates.TemplateResponse("auth/login.html", form.__dict__)
