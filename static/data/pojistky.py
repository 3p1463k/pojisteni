from schemas.pojisteni import VytvorPojisteni

list_pojistek = [
    VytvorPojisteni(
        nazev="Urazove Pojisteni", popis="Pojisteni proti urazu", cena=4500
    ),
    VytvorPojisteni(nazev="Cestovni Pojisteni", popis="Pojisteni na cesty", cena=1500),
    VytvorPojisteni(nazev="Havarijni Pojisteni", popis="Pojisteni pro auto", cena=7500),
    VytvorPojisteni(
        nazev="Duchodove Pojisteni", popis="Zakonne duchodove pojisteni", cena=3000
    ),
    VytvorPojisteni(
        nazev="Zdravotni Pojisteni", popis="Zakonne zdravotni pojisteni", cena=4500
    ),
]
