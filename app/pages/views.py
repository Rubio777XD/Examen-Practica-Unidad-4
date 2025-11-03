"""Server-rendered page routes for the demo frontend."""

from flask import render_template

from . import pages_bp


@pages_bp.get("/")
def index():
    """Render the landing page."""
    return render_template("index.html", title="Inicio")


@pages_bp.get("/register")
def register():
    """Render the user registration form."""
    return render_template("register.html", title="Registrar usuario")


@pages_bp.get("/login")
def login():
    """Render the demo login page."""
    return render_template("login.html", title="Login demo")


@pages_bp.get("/users")
def users():
    """Render the users listing page."""
    return render_template("users.html", title="Usuarios")
