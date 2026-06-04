
from flask import Flask, render_template, request, redirect, url_for, session
from database import get_connection

app = Flask(__name__)
app.secret_key = "prosperapp_secret"

#Pagina de inicio

@app.route("/")
def index():
    return redirect(url_for("login"))

#Login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id_usuario, nombre FROM USUARIO WHERE email=%s AND contraseña=%s",
            (email, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            session["id_usuario"] = user[0]
            session["nombre"] = user[1]
            return redirect(url_for("proyectos"))
        else:
            return render_template("login.html", error="Email o contraseña incorrectos")
    
    return render_template("login.html")

# Ver proyectos

@app.route("/proyectos")
def proyectos():
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id_proyecto, nombre, descripcion, estado FROM PROYECTO WHERE id_usuario=%s",
        (session["id_usuario"],)
    )
    mis_proyectos = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("proyectos.html", proyectos=mis_proyectos)

# Crear proyecto
@app.route("/proyectos/nuevo", methods=["GET", "POST"])
def nuevo_proyecto():
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        secciones = request.form.getlist("secciones")
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO PROYECTO (nombre, descripcion, estado, id_usuario) VALUES (%s, %s, 'activo', %s) RETURNING id_proyecto",
            (nombre, descripcion, session["id_usuario"])
        )
        id_proyecto = cur.fetchone()[0]
        
        for i, seccion in enumerate(secciones):
            cur.execute(
                "INSERT INTO SECCION (nombre, posicion, id_proyecto) VALUES (%s, %s, %s)",
                (seccion, i+1, id_proyecto)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for("proyectos"))
    
    return render_template("nuevo_proyecto.html")

# Ver tablero

@app.route("/proyectos/<int:id_proyecto>")
def tablero(id_proyecto):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT nombre FROM PROYECTO WHERE id_proyecto=%s", (id_proyecto,))
    proyecto = cur.fetchone()
    
    cur.execute(
        "SELECT id_seccion, nombre FROM SECCION WHERE id_proyecto=%s ORDER BY posicion",
        (id_proyecto,)
    )
    secciones = cur.fetchall()
    
    tablero = {}
    for seccion in secciones:
        cur.execute(
            "SELECT id_funcionalidad, titulo FROM FUNCIONALIDAD WHERE id_seccion=%s",
            (seccion[0],)
        )
        tablero[seccion] = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template("tablero.html", proyecto=proyecto, tablero=tablero, id_proyecto=id_proyecto)

# Cerrar sesion

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)