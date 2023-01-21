from schemas.druh_pojisteni import VytvorDruhPojisteni

list_pojistek = [
    VytvorDruhPojisteni(
        nazev="Urazove Pojisteni", popis="Pojisteni proti urazu", cena=4500
    ),
    VytvorDruhPojisteni(
        nazev="Cestovni Pojisteni", popis="Pojisteni na cesty", cena=1500
    ),
    VytvorDruhPojisteni(
        nazev="Havarijni Pojisteni", popis="Pojisteni pro auto", cena=7500
    ),
    VytvorDruhPojisteni(
        nazev="Duchodove Pojisteni", popis="Zakonne duchodove pojisteni", cena=3000
    ),
    VytvorDruhPojisteni(
        nazev="Zdravotni Pojisteni", popis="Zakonne zdravotni pojisteni", cena=4500
    ),
]
