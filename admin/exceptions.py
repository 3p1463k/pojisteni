from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/404.html", {"request": request}, status_code=404
    )


async def internal_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/500.html", {"request": request}, status_code=500
    )


exception_handlers = {404: not_found_error, 500: internal_error}
