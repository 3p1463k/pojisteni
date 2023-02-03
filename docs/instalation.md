# Instalace

## Instalace

### Vytvoreni virtualniho prostredi

Bash terminal

```
conda create --name pojisteni python=3.10.8
```

Alternativne
```
virtualenv -p <path-to-3.10.8> pojisteni
```

### Clone repo
```
git clone https://github.com/3p1463k/pojisteni.git
```

```
cd pojisteni
```
### Install dependencies

```
pip install -r requirements.txt
```

### Spusteni Aplikace
```
uvicorn main:app
```
![Start App](img/start1.png){ loading=lazy }

### Otevreme webovy prohllizec

Na adrese [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

![Start App](img/web1.png){ loading=lazy }
