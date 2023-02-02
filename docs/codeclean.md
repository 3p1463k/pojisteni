# Code cleaning


## Pre-commit

Pro dokumentaci visit [pre-commit.com](https://pre-commit.com/)

Pro kontrolu kodu jsem pouzil:

    black
    reorder_python_imports

### Pre-commit kofigurace

```
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.3.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
    -   id: black
-   repo: https://github.com/asottile/reorder_python_imports
    rev: v2.3.6
    hooks:
    -   id: reorder-python-imports
```
