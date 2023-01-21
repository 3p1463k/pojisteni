from fastapi import Request
from fastapi import Response
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import Session

from apis.version1.routes.route_login import get_current_user_from_token
from apis.version1.routes.route_login import login_for_access_token
from core.config import settings
from db.models.pojistenec import Pojistenec
from db.session import SessionLocal
from webapps.auth.forms import LoginForm


class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:

        """Zkontrolujeme zda uzivatel existuje"""

        form = await request.form()
        username, password = form["username"], form["password"]

        class MyForm:
            def __init__(self, username, password):

                self.username = username
                self.password = password

        myform = MyForm(username, password)

        with SessionLocal() as session:
            pojistenec = (
                session.query(Pojistenec).filter(Pojistenec.email == username).first()
            )

        if pojistenec and pojistenec.is_superuser:

            # print(f"{pojistenec} is ADMIN")
            response = Response()

            res = login_for_access_token(
                response=response, form_data=myform, db=SessionLocal()
            )

            # print(res["access_token"])

            request.session.update({"token": res["access_token"]})

            return True

        print(f"{pojistenec} NOK")

        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:

        """Overime token"""
        token = request.session.get("token")

        if not token:
            return False

        else:
            user = get_current_user_from_token(token, db=SessionLocal())
            if user and user.is_superuser:

                print(token)
                return True
