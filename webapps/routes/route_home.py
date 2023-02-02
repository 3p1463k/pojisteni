from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.dataclasses import dataclass


templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="", tags=["webapp"], include_in_schema=False)


@router.get("/")
async def home(request: Request):

    """Get request na zobrazeni domovske stranky"""

    context = {"request": request}
    return templates.TemplateResponse("general_pages/home1.html", context)
