# Sistema Web Flask – CRUD con autenticación y muro

Aplicación Flask que implementa registro de usuarios, login real con verificación de contraseña y un muro de comentarios, todo con almacenamiento en memoria (RAM). No requiere base de datos ni archivos externos: al reiniciar el servidor, los datos vuelven a su estado inicial.

## Requisitos previos

- Python 3.11 o superior
- Entorno virtual recomendado (`python -m venv .venv`)

## Pasos de ejecución

1. Instala dependencias (solo la primera vez):

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt

   # Linux / macOS
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación (comandos requeridos por el examen):

   ```bash
   cd Examen-Practica-Unidad-4
   .\.venv\Scripts\activate       # Windows PowerShell
   # source .venv/bin/activate      # Linux / macOS
   flask run --port=5001
   ```

3. Abre <http://127.0.0.1:5001/> en tu navegador.

## Flujo funcional

1. **Registrar usuario:** completa el formulario en `/register`.
2. **Iniciar sesión:** ingresa tu correo y contraseña en `/login`. El usuario autenticado se guarda en `localStorage` como `auth_user`.
3. **Ver lista de usuarios:** navega a `/users` para consultar el registro actual (en memoria).
4. **Publicar en el muro:** visita `/muro` para leer y publicar comentarios. Si iniciaste sesión, se mostrará tu nombre como autor; de lo contrario, se publica como “Anónimo”.

## Muro de comentarios

- Endpoint público de lectura: `GET /api/wall/posts`.
- Publicación con validación: `POST /api/wall/posts` (máximo 500 caracteres). Incluye el encabezado `X-Author` para enviar el nombre del usuario autenticado.
- Los comentarios se ordenan del más reciente al más antiguo y se sellan con fecha/hora UTC.

## Ejecución de pruebas automatizadas

```bash
pytest -v
coverage run -m pytest && coverage report -m
```

Las pruebas utilizan `Flask.test_client()` y reinician el almacenamiento en memoria en cada caso de prueba.

## Funcionalidades destacadas

- Registro y autenticación con `werkzeug.security` para el hash de contraseñas.
- Navbar dinámico que alterna entre “Iniciar sesión” y “Cerrar sesión” según el estado en `localStorage`.
- Muro con AJAX (Fetch API) que se actualiza sin recargar la página y admite publicaciones anónimas o autenticadas.
- Suite de pruebas `pytest` que cubre autenticación, CRUD de usuarios, muro y páginas principales.
