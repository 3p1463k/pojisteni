from sqladmin import Admin
from sqladmin import ModelView

from db.models.druh_pojisteni import DruhPojisteni
from db.models.pojistenec import Pojistenec
from db.models.pojisteni import Pojisteni
from db.models.udalost import Udalost


class PojistenecAdmin(ModelView, model=Pojistenec):

    icon = "fa-solid fa-user"
    page_size = 25

    column_list = [
        Pojistenec.id,
        Pojistenec.jmeno,
        Pojistenec.prijmeni,
        # Pojistenec.fullname,
        Pojistenec.ulice,
        Pojistenec.mesto,
        Pojistenec.psc,
        Pojistenec.telefon,
        Pojistenec.email,
        # Pojistenec.hashed_password,
        Pojistenec.is_active,
        Pojistenec.is_superuser,
    ]

    column_searchable_list = [
        Pojistenec.prijmeni,
        Pojistenec.email,
    ]


class PojisteniAdmin(ModelView, model=Pojisteni):

    page_size = 25
    icon = "fa-solid fa-house-crack"

    column_list = [
        Pojisteni.id,
        Pojisteni.nazev,
        Pojisteni.popis,
        Pojisteni.cena,
        Pojisteni.pojistenec_id,
        Pojisteni.datum_zalozeni,
    ]

    column_searchable_list = [
        Pojisteni.nazev,
        Pojisteni.datum_zalozeni,
    ]


class UdalostAdmin(ModelView, model=Udalost):

    page_size = 25
    icon = "fa-solid fa-car"

    column_list = [
        Udalost.id,
        Udalost.nazev,
        Udalost.popis,
        Udalost.skoda,
        Udalost.pojistenec_id,
        Udalost.datum_zalozeni,
    ]


class DruhPojisteniAdmin(ModelView, model=DruhPojisteni):

    page_size = 25
    icon = "fa-solid fa-pen"

    column_list = [
        Pojisteni.id,
        Pojisteni.nazev,
        Pojisteni.popis,
        Pojisteni.cena,
    ]


#
# class DruhPojisteniAdmin(ModelView, model=DruhPojisteni):
#
#     page_size = 25
#
#     column_list = [
#
#         Pojisteni.id,
#         Pojisteni.nazev,
#         Pojisteni.popis,
#         Pojisteni.cena,
#     ]
#
#
