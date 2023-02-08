from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from db.models.pojistenec import Pojistenec
from db.repository.pojistenec import delete_pojistence
from db.repository.pojistenec import find_pojistenec
from db.repository.pojistenec import list_pojistence
from db.repository.pojistenec import update_pojistence
from db.repository.pojisteni import find_pojisteni
from db.repository.pojisteni import list_pojisteni
from db.repository.udalost import find_udalost
from db.repository.udalost import list_udalosti
from db.session import get_session
from schemas.pojistenec import UpravPojistence
from schemas.pojistenec import VytvorPojistence
from schemas.pojistenec import ZobrazPojistence
from schemas.pojisteni import ZobrazPojisteni
from schemas.udalost import ZobrazUdalost
from webapps.auth.forms import LoginForm
from webapps.auth.forms import RegistraceForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["auth-admin"], include_in_schema=False)


@router.get("/administrator/")
def admin_prihlaseni(request: Request):

    """GET request pro prihlaseni admina"""

    return templates.TemplateResponse("auth/admin.html", {"request": request})


@router.post("/administrator/")
async def prihlas_admina(request: Request, session: Session = Depends(get_session)):

    """TODO................"""

    form = LoginForm(request)
    await form.load_data()

    print(f"{form.username} PRINTED from route_login.py")

    if await form.is_valid():

        try:
            email = str(form.username)

            pojistenec = (
                session.query(Pojistenec).filter(Pojistenec.email == email).first()
            )
            # pojistenec = najdi_pojistence_dle_emailu(email, db)

            print(pojistenec.is_superuser)

            if pojistenec and pojistenec.is_superuser:

                form.__dict__.update(msg="Login Successful Vitej admine ")

                response = RedirectResponse(
                    "/administrator/ucet?msg=Uspesne-prihlaseni",
                    status_code=status.HTTP_302_FOUND,
                )

                login_for_access_token(
                    session=session, response=response, form_data=form
                )

                return response

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"You are not permitted!!!!",
            )

            # return templates.TemplateResponse("auth/admin.html", form.__dict__)

        except HTTPException:

            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")

            return templates.TemplateResponse("auth/admin.html", form.__dict__)

    return templates.TemplateResponse("auth/admin.html", form.__dict__)


@router.get("/administrator/ucet/")
def admin_ucet(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """TODO............"""

    if current_user.is_superuser:

        context = {
            "request": request,
            "current_user": current_user,
            "msg": msg,
        }

        return templates.TemplateResponse("auth/adminhome.html", context)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/pojistenci/")
def admin_get_pojistenci(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte pojistence"""

    if current_user.is_superuser:

        pojistenci = list_pojistence(session)

        pojistenci1 = [x.__dict__ for x in pojistenci]

        def without_keys(d, keys):
            return {k: v for k, v in d.items() if k not in keys}

        keys1 = ["_sa_instance_state", "hashed_password", "is_superuser"]

        pojistenci2 = [without_keys(x, keys1) for x in pojistenci1]

        if not pojistenci2:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojistenec s  id neexistuje",
            )

        context = {
            "pojistenci": pojistenci2,
            "request": request,
            "current_user": current_user,
            "msg": msg,
        }

        return templates.TemplateResponse(
            "administrator/admin_pojisteneci.html", context
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/pojisteni/", response_model=ZobrazPojisteni)
def admin_get_pojisteni(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte pojistence"""

    if current_user.is_superuser:

        pojisteni = list_pojisteni(session)

        pojisteni1 = [x.__dict__ for x in pojisteni]

        def without_keys(d, keys):
            return {k: v for k, v in d.items() if k not in keys}

        keys1 = ["_sa_instance_state"]

        pojisteni2 = [without_keys(x, keys1) for x in pojisteni1]

        if not pojisteni:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Zadne pojisteni neexistuje",
            )

        context = {
            "pojisteni": pojisteni,
            "pojisteni2": pojisteni2,
            "request": request,
            "current_user": current_user,
        }

        return templates.TemplateResponse("administrator/admin_pojisteni.html", context)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get(
    "/administrator/pojistenec/{pojistenec_id}", response_model=ZobrazPojistence
)
def admin_get_pojistence(
    pojistenec_id: int,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte pojistence"""

    if current_user.is_superuser:

        pojistenec = find_pojistenec(session, pojistenec_id)

        if not pojistenec:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojistenec s  id {pojistenec_id} neexistuje",
            )

        context = {
            "pojistenec": pojistenec,
            "request": request,
            "current_user": current_user,
        }

        return templates.TemplateResponse(
            "administrator/pojistenec_detail.html", context
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/pojistenec/vymazat/{pojistenec_id}")
def admin_vymazat_pojistence(
    pojistenec_id: int,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vymaze pojistence"""

    if current_user.is_superuser:

        pojistenec = delete_pojistence(session, pojistenec_id)

        if not pojistenec:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojistenec s  id {pojistenec_id} neexistuje",
            )

        response = RedirectResponse(
            "/administrator/pojistenci?msg=Pojistenec-uspesne-vymazan",
            status_code=status.HTTP_302_FOUND,
        )

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/pojistenec/upravit/{pojistenec_id}")
def admin_update_pojistence(
    pojistenec_id: int,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Vymaze pojistence"""

    if current_user.is_superuser:

        pojistenec = find_pojistenec(session, pojistenec_id)

        if not pojistenec:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojistenec s  id {pojistenec_id} neexistuje",
            )

        context = {
            "pojistenec": pojistenec,
            "request": request,
            "current_user": current_user,
        }

        return templates.TemplateResponse(
            "administrator/pojistenec_upravit.html", context
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.post("/administrator/pojistenec/upravit/{pojistenec_id}")
async def admin_uprav_pojistence(
    pojistenec_id,
    pojistenec: UpravPojistence,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Uprava pojistence"""

    # pojistenec = find_pojistenec(session, pojistenec_id)
    if current_user.is_superuser:

        form = RegistraceForm(request)
        await form.load_data()

        pojistenec1 = UpravPojistence(
            jmeno=form.jmeno,
            prijmeni=form.prijmeni,
            ulice=form.ulice,
            mesto=form.mesto,
            psc=form.psc,
            telefon=form.telefon,
            email=form.email,
            password=form.password,
        )

        pojistenec2 = update_pojistence(session, pojistenec_id, pojistenec1)

        response = responses.RedirectResponse(
            "/administrator/pojistenci?msg=Pojistenec-uspesne-Upraven",
            status_code=status.HTTP_302_FOUND,
        )

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/pojisteni/{pojisteni_id}", response_model=ZobrazPojisteni)
def admin_get_pojisteni(
    pojisteni_id: int,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte detail jednotliveho pojisteni"""

    if current_user.is_superuser:

        pojisteni = find_pojisteni(session, pojisteni_id)

        if not pojisteni:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pojisteni s  id {pojisteni_id} neexistuje",
            )

        context = {
            "pojisteni": pojisteni,
            "request": request,
            "current_user": current_user,
        }

        return templates.TemplateResponse(
            "administrator/pojisteni_detail.html", context
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/udalosti/", response_model=ZobrazUdalost)
def admin_get_udalosti(
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte udalosti"""

    if current_user.is_superuser:

        udalosti = list_udalosti(session)
        udalosti2 = [x.__dict__ for x in udalosti]

        def without_keys(d, keys):
            return {k: v for k, v in d.items() if k not in keys}

        keys1 = ["_sa_instance_state"]

        udalosti2 = [without_keys(x, keys1) for x in udalosti2]

        if not udalosti:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Udalost  neexistuje",
            )

        context = {
            "udalosti": udalosti,
            "udalosti2": udalosti2,
            "request": request,
            "current_user": current_user,
        }

        return templates.TemplateResponse("administrator/admin_udalosti.html", context)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )


@router.get("/administrator/udalost/{udalost_id}", response_model=ZobrazUdalost)
def admin_get_udalost(
    udalost_id: int,
    request: Request,
    session: Session = Depends(get_session),
    msg: str = None,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):
    """Nacte detail udalosti"""

    if current_user.is_superuser:

        udalost = find_udalost(session, udalost_id)

        if not udalost:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Udalost s  id {udalost_id} neexistuje",
            )

        context = {"udalost": udalost, "request": request, "current_user": current_user}

        return templates.TemplateResponse("administrator/udalost_detail.html", context)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"You are not permitted!!!!",
    )
