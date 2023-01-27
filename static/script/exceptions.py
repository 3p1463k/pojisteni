from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def not_found_error(request: Request, exc: HTTPException):

    context = {"detail": str(exc.detail), "request": request}

    return templates.TemplateResponse("errors/404.html", context, status_code=404)


async def internal_error(request: Request, exc: HTTPException):

    context = {"request": request}

    return templates.TemplateResponse("errors/500.html", context, status_code=500)


async def expired_token_error(request: Request, exc: HTTPException):

    context = {"detail": str(exc.detail), "request": request}

    return templates.TemplateResponse("errors/403.html", context, status_code=403)


async def unauthorized_error(request: Request, exc: HTTPException):

    context = {"detail": str(exc.detail), "request": request}

    return templates.TemplateResponse("errors/401.html", context, status_code=401)


async def unprocessable_entity_error(request: Request, exc: HTTPException):

    context = {"detail": str(exc.detail), "request": request}

    return templates.TemplateResponse("errors/422.html", context, status_code=422)


exception_handlers = {
    404: not_found_error,
    500: internal_error,
    403: expired_token_error,
    401: unauthorized_error,
    422: unprocessable_entity_error,
}
