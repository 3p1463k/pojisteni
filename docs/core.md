# Core


## Config

config.py

V configu mame tridu  Settings, kde nastavime potrebne udaje

```
class Settings:

    PROJECT_NAME: str = "POJISTENI-FASTAPI-SQLMODEL"
    PROJECT_VERSION: str = "1.0.0"
    # PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    TEST_USER_EMAIL = "test@example.com"

```
## Hashing

hashing.py

Funkci pro overeni a zasiforvani hesla muzete vyzkouset v prikazovem radku

Spuste python

```
python
```
```
>>> from core.hashing import Hasher
>>> Hasher.get_password_hash("AhojSvete")
'$2b$12$yAysWQB8WjKO56XZXsHX9ekxIVmJTc5DFEFUZCuEm4QMmXDz8HPO6'
```
```
>>> Hasher.verify_password("AhojSvete", "$2b$12$yAysWQB8WjKO56XZXsHX9ekxIVmJTc5DFEFUZCuEm4QMmXDz8HPO6")
True
```
```
>>> Hasher.verify_password("Ahoj", "$2b$12$yAysWQB8WjKO56XZXsHX9ekxIVmJTc5DFEFUZCuEm4QMmXDz8HPO6")
False
```

![Hasher](img/hash1.png){ loading=lazy }

## Security

security.py

Funkci generace tokenu muzete vyzkouset v prikazovem radku

Spuste python
```
python
```

```
>>> from core.security import create_access_token
>>> data = {"sub":"fake@email.com"}
>>> create_access_token(data)

output:

'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWtlQGVtYWlsLmNvbSIsImV4cCI6MTY3NTQzODE0NH0.qBDN_BNxIIE3sKDGf69hHP1pIa4s6_HKx1ky3b_LD1U'
```

![Hasher](img/token1.png){ loading=lazy }
