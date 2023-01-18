from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import login_for_access_token
from db.session import get_db
from webapps.auth.forms import LoginForm


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["auth-webapp"], include_in_schema=False)


@router.get("/logout/")
def user_logout(request: Request):

    """TODO............"""

    return templates.TemplateResponse("auth/logout.html", {"request": request})


@router.post("/logout/")
async def logout(request: Request, response: Response):

    """Odhlasi s uctu vymazanim cookie"""
    response.delete_cookie("bearer")

    print(response.status_code)
    # return {"status":"success"}

    context = {"request": request}

    return templates.TemplateResponse("auth/login5.html", context)
