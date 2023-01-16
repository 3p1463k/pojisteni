from fastapi import APIRouter, HTTPException, Request, Form, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.dataclasses import dataclass
from datetime import datetime


templates = Jinja2Templates(directory="templates")

router = APIRouter(

    prefix="",
    tags=["home-webapp"],
    include_in_schema=False
)


@router.get("/")
async def home(request: Request):

    """Get request na zobrazeni domovske stranky"""

    context = {"request": request}
    return templates.TemplateResponse("general_pages/homepage.html", context)
