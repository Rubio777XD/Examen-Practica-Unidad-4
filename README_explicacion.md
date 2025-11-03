# Entendiendo el proyecto paso a paso

## 1. Introducción general
Imagina un pequeño portal escolar donde podemos registrar a los estudiantes, iniciar sesión y dejar mensajes en un muro público. Eso es exactamente lo que hace este sistema. Se creó para practicar cómo un backend (el servidor) y un frontend (las pantallas del navegador) se hablan entre sí mientras manejan usuarios, autenticación y publicaciones.

## 2. Estructura del proyecto
A grandes rasgos, el proyecto está dividido así:

- `app/`: contiene todo el código de la aplicación Flask.
  - `create_app.py`: arma la aplicación, registra las rutas y configura los errores.
  - `routes/`: aquí viven las rutas de la API (lo que responde en formato JSON).
  - `pages/` y `templates/`: definen las páginas HTML que ve el usuario.
  - `static/`: archivos estáticos como JavaScript y CSS para darle vida a las páginas.
  - `store.py`: actúa como una “mini base de datos” guardada en memoria.
  - `schemas.py` y `validators.py`: validan datos antes de guardarlos.
- `tests/`: pruebas automáticas que verifican que todo funcione.
- `README.md` y `README_REPORT.md`: documentos de referencia (uno explica instalación/uso y otro sirve como registro de cambios).

## 3. Backend (API)
El backend está hecho con **Flask**, un framework de Python pensado para construir APIs y páginas web ligeras.

Las rutas principales son:

- `POST /api/auth/login`: revisa el correo y la contraseña y responde con los datos del usuario cuando son correctos.
- `POST /api/users`: crea un usuario nuevo validando nombre, correo y contraseña.
- `GET /api/users`: lista todos los usuarios registrados hasta el momento.
- `GET /api/users/<id>`: devuelve los datos de un usuario específico.
- `PUT /api/users/<id>`: actualiza nombre, correo o contraseña de un usuario.
- `DELETE /api/users/<id>`: elimina un usuario.
- `GET /api/wall/posts`: entrega los mensajes publicados en el muro (del más reciente al más viejo).
- `POST /api/wall/posts`: agrega un mensaje nuevo al muro; si no dices quién eres, firma como “Anónimo”.

Todas estas rutas usan `store.py` para guardar la información en memoria y `schemas.py`/`validators.py` para asegurarse de que los datos tienen sentido.

## 4. Frontend (HTML/JS/CSS)
Las pantallas están hechas con plantillas HTML y un archivo JavaScript (`app/static/js/app.js`) que hace las peticiones a la API.

- **Página de inicio (`/`)**: presentación rápida y acceso al resto del sitio.
- **Registro (`/register`)**: formulario para crear usuarios; al enviar el formulario se llama a `POST /api/users` desde JavaScript.
- **Login (`/login`)**: formulario que se conecta con `POST /api/auth/login`. Si el login sale bien, guarda los datos en el `localStorage` del navegador para recordar quién eres.
- **Listado de usuarios (`/users`)**: muestra una tabla con la información que llega de `GET /api/users` y permite eliminar usuarios desde la misma vista.
- **Muro (`/muro`)**: carga mensajes desde `GET /api/wall/posts` y permite publicar nuevos con `POST /api/wall/posts`. Si entraste con tu cuenta, envía tu nombre en una cabecera llamada `X-Author`.

El CSS (`app/static/css/styles.css`) mantiene un estilo limpio y el JavaScript también maneja mensajes emergentes (toasts) para avisar si las acciones salieron bien o mal.

## 5. Base de datos
No hay una base de datos “real” (como MySQL o PostgreSQL). En su lugar usamos estructuras en memoria:

- **USERS**: diccionario donde la clave es el ID del usuario y el valor es su información (nombre, correo, fecha de creación y hash de la contraseña).
- **POSTS**: lista con los mensajes del muro. Cada mensaje guarda autor, contenido y fecha/hora en formato ISO.

Al reiniciar el servidor se reinicia todo, igual que cuando apagamos una consola de videojuegos sin guardar la partida.

## 6. Pruebas
Se usan dos estilos:

- **Pytest** (`tests/test_auth.py`, `tests/test_api_users.py`, `tests/test_wall.py`, etc.): simulan llamadas a la API y a las páginas para confirmar que respondan lo esperado (códigos 200, errores cuando deben, datos correctos, etc.).
- **Unittest** (`tests/test_validators_unittest.py`): prueba las funciones de validación de nombres, correos y contraseñas.

En conjunto revisan autenticación, CRUD de usuarios, muro de mensajes y que las plantillas HTML carguen bien.

## 7. Cómo ejecutar el proyecto
1. Crea y activa un entorno virtual (opcional pero recomendado).
2. Instala dependencias con `pip install -r requirements.txt`.
3. Arranca el servidor con `flask run --port=5001` (Flask usará la aplicación definida en `app/create_app.py`).
4. Abre `http://127.0.0.1:5001/` en el navegador y juega con las diferentes páginas.
5. Para correr las pruebas, ejecuta `pytest` (también puedes usar `coverage run -m pytest` para ver cobertura).

## 8. Resumen final (end-to-end)
El flujo completo se ve así:

1. Abres el sitio y navegas a la sección que necesites (registro, login, muro, etc.).
2. Cuando envías un formulario, el JavaScript manda la información a la API Flask.
3. La API valida los datos, los guarda en la memoria interna (`store.py`) y responde con JSON.
4. El JavaScript interpreta la respuesta: actualiza las tablas, muestra mensajes y, si aplica, guarda tus datos en `localStorage`.
5. Todo el proceso se repite cada vez que interactúas con el sistema, manteniendo sincronizados el frontend y el backend.

Así, aunque no haya una base de datos tradicional, backend, frontend y pruebas se combinan para demostrar cómo funcionaría un pequeño sistema de usuarios con autenticación y muro de comentarios.
