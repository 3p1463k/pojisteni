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


@router.get("/about/")
async def about(request: Request):

    context = {"request": request}
    return templates.TemplateResponse("general_pages/about.html", context)
