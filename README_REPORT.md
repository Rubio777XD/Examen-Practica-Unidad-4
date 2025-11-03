# Registro de Cambios

## Refactor in-memory (actual)

- Se eliminó por completo la dependencia de base de datos (SQLAlchemy, migraciones, modelos).
- Se añadió `app/store.py` con diccionarios en memoria para gestionar usuarios y reinicios en modo pruebas.
- Las rutas `/api/users` ahora operan sobre el almacenamiento en memoria, mantienen validaciones con Marshmallow y hash de contraseña.
- Se simplificó el `Makefile`, los requisitos (`requirements.txt`) y la configuración (`app/config.py`).
- Se actualizó la fábrica de aplicación (`create_app`) para aceptar `testing=True`, reiniciar el store y exponer `/api/_debug/reset` durante las pruebas.
- Se reemplazaron las pruebas por versiones Pytest que validan el CRUD y las páginas básicas.
- Se actualizó la documentación principal (`README.md`) con instrucciones de instalación/ejecución/pruebas para Windows y Linux/Mac.

## Historial previo

- Configuración inicial del CRUD con Flask, validaciones y pruebas base.
