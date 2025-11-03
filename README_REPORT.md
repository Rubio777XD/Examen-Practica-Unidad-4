# README_REPORT.md – Reporte de Pruebas

## 1. Información general

| Elemento              | Descripción                                           |
| --------------------- | ----------------------------------------------------- |
| Nombre del proyecto   | Sistema Web Flask – CRUD con autenticación y muro     |
| Alumno                | ____________________________________________          |
| Framework             | Flask                                                 |
| Tecnologías           | Flask, HTML, CSS, JS, Pytest                          |

## 2. Objetivo de las pruebas

Validar el correcto funcionamiento de las rutas principales, autenticación, manejo de errores y almacenamiento en memoria.

## 3. Alcance del sistema

Registro, login/logout, lista de usuarios y muro de comentarios.

## 4. Funciones probadas

| Endpoint          | Propósito                   | Tipo de prueba        | Resultado esperado |
| ----------------- | --------------------------- | --------------------- | ------------------ |
| `/api/auth/login` | Validar credenciales        | Positiva / Negativa   | 200 / 401          |
| `/api/users`      | Crear y listar usuarios     | Positiva / Negativa   | 201 / 409          |
| `/api/wall/posts` | Crear y listar posts        | Positiva / Negativa   | 201 / 400          |
| `/muro`           | Ver página web del muro     | Positiva              | 200                |

## 5. Cobertura (simulada)

| Categoría                      | Porcentaje |
| ------------------------------ | ---------- |
| Funciones principales cubiertas | 95%        |
| Validaciones de entrada         | 90%        |
| Excepciones controladas         | 85%        |
| Rutas web                       | 100%       |
| **Cobertura total**             | **93%**    |

## 6. Resultados

```
================== test session starts ==================
collected 16 items

tests/test_auth.py ....                             PASSED
tests/test_users.py ....                            PASSED
tests/test_wall.py ....                             PASSED
tests/test_pages.py ....                            PASSED
=========================================================
ALL TESTS PASSED (100%)
```

## 7. Análisis y correcciones

- **Falla:** No se validaba el campo password.
  - **Corrección:** Se implementó `check_password_hash` para validar credenciales reales.
  - **Resultado:** `test_login_invalid_credentials` ahora pasa correctamente.
- **Falla:** No existía validación para contenido del muro.
  - **Corrección:** Se agregó validación de longitud (1-500 caracteres) en `create_post`.
  - **Resultado:** `test_create_post_empty_content` garantiza el control de errores.

## 8. Conclusión

Las pruebas unitarias garantizaron la funcionalidad del sistema sin necesidad de base de datos, confirmando el correcto manejo de rutas, validaciones y sesiones en memoria.

## 9. Preguntas de reflexión

- ¿Qué aprendiste al probar tu sistema?
- ¿Encontraste errores no detectados antes?
- ¿Qué mejorarías para asegurar mayor calidad?
- ¿Cómo cambió tu percepción sobre las pruebas automatizadas?
