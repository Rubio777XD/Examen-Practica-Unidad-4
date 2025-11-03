# Proyecto – CRUD de Usuarios (almacenamiento en memoria)

Aplicación Flask con API y páginas HTML para gestionar usuarios utilizando almacenamiento en memoria
(lista/dicts en Python). No existe base de datos: cada vez que se reinicia el servidor los datos se
reinician.

## Requisitos

- Python 3.11+
- (Windows) PowerShell
- (Linux/Mac) bash

## Instalación

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/Mac

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la app

```powershell
# Windows
$env:FLASK_APP = "app/create_app.py"
flask run --port 5001
```

```bash
# Linux/Mac
export FLASK_APP=app/create_app.py
flask run --port 5001
```

Abre: <http://127.0.0.1:5001/>

- Páginas: `/`, `/register`, `/login`, `/users`
- API: `/api/users`, `/api/users/<id>`

## Pruebas y cobertura

```powershell
# Windows (con el entorno virtual activo)
pytest -q
coverage run -m pytest
coverage report -m
coverage html  # ver htmlcov/index.html
```

```bash
# Linux/Mac
pytest -q
coverage run -m pytest
coverage report -m
coverage html
```

## Notas

- Almacenamiento 100% en memoria, sin persistencia ni migraciones.
- Los usuarios se guardan con `password_hash`; la contraseña nunca aparece en respuestas.
- Existe un endpoint opcional `/api/_debug/reset` disponible únicamente en modo de pruebas para
  limpiar el estado entre tests.
