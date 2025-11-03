# Proyecto – CRUD de Usuarios (almacenamiento en memoria)

Aplicación Flask con API REST y páginas HTML para gestionar usuarios utilizando
almacenamiento 100% en memoria (sin base de datos). Al reiniciar el servidor, los
registros se reinician.

## Requisitos

- Python 3.11+
- (Windows) PowerShell
- (Linux/Mac) bash

## Ejecutar la aplicación

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "app/create_app.py"
flask run --port 5001
```

### Linux/Mac

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app/create_app.py
flask run --port 5001
```

Luego abre <http://127.0.0.1:5001/> para acceder a las páginas (`/`, `/register`,
`/login`, `/users`) y a la API (`/api/users`, `/api/users/<id>`, `/api/health`).

## Pruebas

```bash
pytest -q
coverage run -m pytest && coverage report -m
```

## Características clave

- CRUD de usuarios completamente en memoria con validación y manejo de errores
  consistentes.
- Endpoints REST listos para pruebas automáticas (`/api/health` para smoke tests).
- Frontend ligero con formularios que consumen la API y muestran mensajes claros.
