from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import ExpiredSignatureError
from jose import jwt
from jose import JWTError
from sqlmodel import Session

from apis.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.login import najdi_pojistence_dle_emailu
from db.session import get_session
from schemas.tokens import Token


login_router = APIRouter(prefix="", tags=["login-api"])
templates = Jinja2Templates(directory="templates")


def authenticate_user(email: str, password: str, session: Session):

    """Overime zda uzivatel exisuje"""

    user = najdi_pojistence_dle_emailu(email, session)

    if not user:
        return False

    if not Hasher.verify_password(password, user.hashed_password):
        return False

    return user


@login_router.post("/login/token/", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    user = authenticate_user(form_data.username, form_data.password, session)

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )  # set HttpOnly cookie in response

    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token/")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
):

    """Najdi uzivatele podle tokenu"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials - Nelze Overit",
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except ExpiredSignatureError:

        raise HTTPException(
            status_code=403, detail="Prihlaseni vyprselo - token has been expired"
        )

    except JWTError as e:
        print(f"JWTError \n {e}")
        raise credentials_exception

    user = najdi_pojistence_dle_emailu(email=username, session=session)

    if user is None:
        raise credentials_exception

    return user
