# Sistema de Registro de Usuarios

Proyecto base en Flask 3.11 que implementa un CRUD de usuarios con SQLite y SQLAlchemy. Incluye un frontend mínimo con plantillas Jinja y JavaScript para interactuar con los endpoints REST, junto con pruebas automatizadas, cobertura y CI.

## Arquitectura

```
[Navegador]
     |
     v
[Flask Pages (Jinja) + Fetch] --> [Flask API] --(SQLAlchemy)--> [SQLite app.db]
```

## Matriz de versiones (línea A)

| Componente | Versión fijada |
| --- | --- |
| Flask | 2.3.3 |
| Werkzeug | 2.3.7 |
| Jinja2 | 3.1.3 |
| itsdangerous | 2.1.2 |
| click | 8.1.7 |
| Flask-SQLAlchemy | 3.1.1 |
| Flask-Migrate | 4.0.5 |
| Flask-Marshmallow | 0.15.0 |
| marshmallow | 3.21.1 |
| email-validator | 2.1.1 |
| SQLAlchemy | 2.0.30 |
| pytest | 8.2.2 |
| pytest-cov | 5.0.0 |
| coverage | 7.5.1 |
| flake8 | 7.0.0 |
| black | 24.4.2 |
| isort | 5.13.2 |

## Stack principal

- Python 3.11
- Flask con Blueprints (API y páginas)
- SQLite/SQLAlchemy + Flask-Migrate
- Marshmallow para validaciones de entrada/salida
- Werkzeug para hashing de contraseñas
- Pytest y unittest para pruebas automatizadas
- Coverage.py para cobertura de código
- Black, isort y Flake8 para estilo y linting
- GitHub Actions para CI

## Requisitos previos

- Python 3.11
- `make`

Se recomienda crear un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .\.venv\Scripts\activate
```

## Instalación

```bash
make install
```

### Instalación con proxy u offline

```bash
pip install --no-cache-dir --proxy=http://USUARIO:PASS@HOST:PUERTO -r requirements.txt
```

```bash
pip download -r requirements.txt -d wheels
pip install --no-index --find-links=./wheels -r requirements.txt
```

## Ejecución en desarrollo

Inicializa las tablas (si usas migraciones):

```bash
flask --app app/create_app.py db upgrade
```

Inicia el servidor:

```bash
make run
```

La API queda disponible en `http://127.0.0.1:5000/api/users` y las páginas en la raíz (`/`, `/register`, `/login`, `/users`).

## Comandos principales

```bash
make install  # Instala dependencias fijadas
make run      # Ejecuta la app en modo debug
make test     # Ejecuta pytest (API + smoke tests de páginas)
make cov      # Ejecuta pytest con coverage y genera htmlcov/
make fmt      # Aplica black + isort
make lint     # Ejecuta flake8
make clean    # Elimina artefactos temporales
```

## Interfaz web y endpoints principales

La interfaz incorpora el tema “galaxy/neón futurista” y utiliza Fetch API para comunicarse con los endpoints REST existentes.

- `/` página de inicio con hero y CTA hacia el listado.
- `/register` formulario que consume `POST /api/users` mediante `fetch`.
- `/login` flujo de "login demo" que almacena el usuario en `localStorage` tras consultar la API.
- `/users` tabla que lista usuarios y permite eliminarlos vía `DELETE /api/users/<id>`.

### Crear usuario (API)

```bash
curl -X POST http://127.0.0.1:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com", "password": "secret123"}'
```

Respuesta 201:

```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

### Listar usuarios (API)

```bash
curl http://127.0.0.1:5000/api/users?page=1&per_page=10
```

### Ver detalle (API)

```bash
curl http://127.0.0.1:5000/api/users/1
```

### Actualizar usuario (API)

```bash
curl -X PUT http://127.0.0.1:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Updated", "password": "newsecret123"}'
```

### Eliminar usuario (API)

```bash
curl -X DELETE http://127.0.0.1:5000/api/users/1
```

## Pruebas y cobertura

```bash
make test
make cov  # Genera htmlcov/index.html con reporte detallado
```

La meta de cobertura es ≥ 90%. Los resultados concretos se documentan en `README_REPORT.md`.

## Estilo y calidad

```bash
make fmt
make lint
```

## Troubleshooting

- **ModuleNotFoundError: werkzeug**: reinstala dependencias con `pip install --no-cache-dir -r requirements.txt` para asegurar las versiones fijadas de Flask/Werkzeug.
- **Fallo al descargar dependencias**: utiliza el modo proxy u offline descrito arriba.

## Integración continua

El workflow GitHub Actions (`.github/workflows/ci.yml`) instala dependencias con soporte para variables de proxy, ejecuta `make lint`, `make test` y `make cov` en Python 3.11.

## Limitaciones actuales

- No existe autenticación ni autorización avanzada.
- No se expone documentación OpenAPI.
- El “login” es solo de demostración en el navegador (localStorage).

## Mejoras futuras sugeridas

- Agregar autenticación básica o basada en tokens.
- Publicar documentación interactiva (Swagger/OpenAPI).
- Añadir rate limiting y registro de auditoría.
- Implementar pre-commit hooks con formateadores y linters.

Para seguimiento de cambios y reporte del examen consulta `README_REPORT.md`.
