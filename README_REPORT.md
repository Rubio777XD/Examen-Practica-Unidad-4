# Reporte de Pruebas

## Información general

| Elemento | Detalle |
| --- | --- |
| Nombre del proyecto | Sistema de Registro de Usuarios |
| Alumno | *Autogenerado por IA* |
| Framework | Flask |
| Tecnologías utilizadas | Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, Email-Validator, Werkzeug, Pytest, Unittest, Coverage.py, Black, isort, Flake8, GitHub Actions |
| Objetivo de las pruebas | Validar el CRUD de usuarios, sus validaciones y manejo de errores |

### Alcance del sistema

- CRUD completo de usuarios con validaciones y hashing de contraseña.
- Listado con paginación y filtros básicos de página/per_page.
- Manejo uniforme de errores y respuestas JSON.
- Frontend mínimo servido por Flask con plantillas Jinja y Fetch API.

## Funciones / Rutas probadas

| Función/Endpoint | Propósito | Tipo de prueba | Resultado esperado |
| --- | --- | --- | --- |
| POST /api/users | Crear usuario | Positiva/Negativa | 201 / 400 / 409 |
| GET /api/users | Listar | Positiva | 200 + lista |
| GET /api/users/<id> | Detalle | Positiva/Negativa | 200 / 404 |
| PUT /api/users/<id> | Actualizar | Positiva/Negativa | 200 / 400 / 409 |
| DELETE /api/users/<id> | Borrar | Positiva/Negativa | 204 / 404 |
| Páginas HTML (/, /register, /login, /users) | Renderizar interfaz | Positiva | 200 + contenido base |

## Cobertura general

> **Nota:** La ejecución de pruebas sigue bloqueada en este entorno por restricciones de red (proxy 403 al descargar dependencias). Una vez instaladas las dependencias fijadas, se espera ≥ 90% de cobertura; la tabla se actualizará con los porcentajes reales.

| Categoría | Porcentaje |
| --- | --- |
| Funciones principales | N/D (pendiente) |
| Validaciones de entrada | N/D (pendiente) |
| Excepciones controladas | N/D (pendiente) |
| Rutas o vistas web | N/D (pendiente) |
| Cobertura total aprox. | N/D (pendiente) |

## Resultados de ejecución

### Antes de correcciones

```
$ make test
ImportError while loading conftest '/workspace/Examen-Practica-Unidad-4/tests/conftest.py'.
tests/conftest.py:6: in <module>
    from werkzeug.security import generate_password_hash
ModuleNotFoundError: No module named 'werkzeug'
```

### Después de correcciones

Se fijaron versiones compatibles (línea A) y se actualizó el Makefile, pero la instalación sigue fallando por el proxy del entorno:

```
$ make install
...
ERROR: Could not find a version that satisfies the requirement Flask==2.3.3 (from versions: none)
ERROR: No matching distribution found for Flask==2.3.3
```

El intento de verificar versiones y ejecutar pruebas refleja la ausencia de dependencias instaladas:

```
$ python -c "import flask, werkzeug; print(flask.__version__, werkzeug.__version__)
ModuleNotFoundError: No module named 'flask'

$ make test
ModuleNotFoundError: No module named 'werkzeug'

$ make cov
make: coverage: No such file or directory
```

### Resumen de coverage

No disponible por la limitación anterior.

## Análisis y correcciones

| Fallo | Causa raíz | Fix aplicado | Evidencia |
| --- | --- | --- | --- |
| `ModuleNotFoundError: No module named 'werkzeug'` | Dependencias sin instalar por bloqueo de proxy 403. | Se fijaron versiones compatibles (Flask 2.3.3/Werkzeug 2.3.7 y stack completo), se actualizó `requirements.txt`, Makefile y documentación para soportar instalación con proxy/offline. | Intentos documentados en la sección de resultados muestran el bloqueo remanente hasta contar con acceso a PyPI. |
| `make cov` sin comando coverage | La librería no se instaló por la misma restricción de red. | Cobertura configurada en `.coveragerc` y Makefile; pendiente de instalación exitosa para ejecutar. | Ver comandos fallidos anteriores. |

## Conclusión

El proyecto queda preparado con dependencias fijadas, scripts de automatización y documentación para instalar mediante proxy u offline. Una vez que se ejecute `make install` en un entorno con acceso a PyPI (o paquetes locales), se podrán correr `make test` y `make cov`, alcanzando la cobertura objetivo ≥ 90% sobre el CRUD y las páginas de soporte.

## Preguntas de reflexión

- **¿Qué aprendiste al probar tu sistema?** La combinación de pruebas API + smoke tests HTML permite validar tanto la lógica de negocio como la interfaz básica.
- **Errores encontrados que no habías visto:** El proxy corporativo bloquea la descarga de paquetes, resaltando la necesidad de documentar instalaciones alternativas.
- **Mejoras futuras para más calidad:** Ejecutar los flujos en un entorno con conectividad, agregar pruebas end-to-end en navegador y publicar reportes de cobertura como artefactos del CI.
- **Valor de las pruebas automatizadas:** Aseguran regresiones controladas en el CRUD, las validaciones y los templates al mantener una línea base reproducible.
