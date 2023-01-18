from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import get_current_user_from_token
from db.models.pojistenec import Pojistenec
from db.session import get_db
from webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["auth-webapp"], include_in_schema=False)


@router.get("/logout/")
def user_logout(
    request: Request,
    current_user: Pojistenec = Depends(get_current_user_from_token),
):

    """TODO............"""

    context = {"request": request, "current_user": current_user}

    return templates.TemplateResponse("auth/logout.html", context)


@router.post("/logout/")
async def logout(request: Request, response: Response):

    """Odhlasi s uctu vymazanim cookie"""
    response.delete_cookie("bearer")

    print(response.status_code)
    # return {"status":"success"}

    context = {"request": request}

    return templates.TemplateResponse("auth/login.html", context)
