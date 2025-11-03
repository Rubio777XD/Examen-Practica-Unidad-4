# Registro de Cambios

## CRUD en memoria corregido (actual)

- Se implementó `app/store.py` como fuente de verdad en memoria con creación,
  listado, actualización y borrado de usuarios, garantizando emails únicos.
- Se actualizaron los endpoints `/api/users` para usar el store, estandarizar
  respuestas JSON (incluyendo 409 para emails duplicados) y exponer `/api/health`.
- Se ajustaron los esquemas de Marshmallow y la fábrica `create_app` para limpiar
  el estado en pruebas y devolver errores consistentes.
- Se reescribieron los formularios y scripts de frontend (`register`, `/users`) para
  consumir la API con fetch, mostrar toasts claros y refrescar la tabla.
- Se actualizaron las pruebas de Pytest y la documentación (`README.md`) con
  instrucciones para ejecutar la app en el puerto 5001 y validar con cobertura.

## Refactor in-memory (anterior)

- Se eliminó por completo la dependencia de base de datos (SQLAlchemy,
  migraciones, modelos).
- Se añadió `app/store.py` con diccionarios en memoria para gestionar usuarios y
  reinicios en modo pruebas.
- Las rutas `/api/users` ahora operan sobre el almacenamiento en memoria,
  mantienen validaciones con Marshmallow y hash de contraseña.
- Se simplificó el `Makefile`, los requisitos (`requirements.txt`) y la
  configuración (`app/config.py`).
- Se actualizó la fábrica de aplicación (`create_app`) para aceptar
  `testing=True`, reiniciar el store y exponer `/api/_debug/reset` durante las
  pruebas.
- Se reemplazaron las pruebas por versiones Pytest que validan el CRUD y las
  páginas básicas.
- Se actualizó la documentación principal (`README.md`) con instrucciones de
  instalación/ejecución/pruebas para Windows y Linux/Mac.

## Historial previo

- Configuración inicial del CRUD con Flask, validaciones y pruebas base.
