from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.dataclasses import dataclass

# from deta import Deta

# deta = Deta()

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="", tags=["udalosti-webapp"], include_in_schema=True)


@router.get("/udalosti/")
async def udalosti(request: Request):

    context = {"request": request}
    return templates.TemplateResponse("pojisteni/udalosti.html", context)
