# =============================================
# ProsperApp - Aplicación principal
# =============================================
from flask import Flask, render_template, request, redirect, url_for, session
from database import get_connection

app = Flask(__name__)
app.secret_key = "prosperapp_secret"

# -------------------------
# Ruta 1: Página de inicio
# -------------------------
@app.route("/")
def index():
    return redirect(url_for("login"))

# -------------------------
# Ruta 2: Login
# -------------------------
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

# -------------------------
# Ruta 3: Ver proyectos
# -------------------------
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

# -------------------------
# Ruta 4: Crear proyecto
# -------------------------
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

# -------------------------
# Ruta 5: Eliminar proyecto
# -------------------------
# -------------------------
# Ruta 5: Eliminar proyecto
# -------------------------
@app.route("/proyectos/<int:id_proyecto>/eliminar", methods=["POST"])
def eliminar_proyecto(id_proyecto):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    conn = get_connection()
    cur = conn.cursor()

    # Primero obtenemos las secciones del proyecto
    cur.execute("SELECT id_seccion FROM SECCION WHERE id_proyecto=%s", (id_proyecto,))
    secciones = cur.fetchall()

    for seccion in secciones:
        # Obtenemos las funcionalidades de cada seccion
        cur.execute("SELECT id_funcionalidad FROM FUNCIONALIDAD WHERE id_seccion=%s", (seccion[0],))
        funcionalidades = cur.fetchall()

        for func in funcionalidades:
            # Eliminamos subtareas de cada funcionalidad
            cur.execute("DELETE FROM SUBTAREA WHERE id_funcionalidad=%s", (func[0],))

        # Eliminamos funcionalidades de la seccion
        cur.execute("DELETE FROM FUNCIONALIDAD WHERE id_seccion=%s", (seccion[0],))

    # Eliminamos las secciones del proyecto
    cur.execute("DELETE FROM SECCION WHERE id_proyecto=%s", (id_proyecto,))

    # Finalmente eliminamos el proyecto
    cur.execute("DELETE FROM PROYECTO WHERE id_proyecto=%s AND id_usuario=%s",
                (id_proyecto, session["id_usuario"]))

    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("proyectos"))

# -------------------------
# Ruta 6: Ver tablero
# -------------------------
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

# -------------------------
# Ruta 7: Agregar funcionalidad
# -------------------------
@app.route("/seccion/<int:id_seccion>/funcionalidad/nueva", methods=["POST"])
def nueva_funcionalidad(id_seccion):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    titulo = request.form["titulo"]
    historia = request.form["historia"]
    notas = request.form["notas"]
    id_proyecto = request.form["id_proyecto"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO FUNCIONALIDAD (titulo, historia_usuario, notas_diseño, id_seccion) VALUES (%s, %s, %s, %s)",
        (titulo, historia, notas, id_seccion)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("tablero", id_proyecto=id_proyecto))

# -------------------------
# Ruta 8: Eliminar funcionalidad
# -------------------------
# -------------------------
# Ruta 8: Eliminar funcionalidad
# -------------------------
@app.route("/funcionalidad/<int:id_funcionalidad>/eliminar", methods=["POST"])
def eliminar_funcionalidad(id_funcionalidad):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    id_proyecto = request.form["id_proyecto"]
    
    conn = get_connection()
    cur = conn.cursor()

    # Primero eliminamos las subtareas de la funcionalidad
    cur.execute("DELETE FROM SUBTAREA WHERE id_funcionalidad=%s", (id_funcionalidad,))

    # Luego eliminamos la funcionalidad
    cur.execute("DELETE FROM FUNCIONALIDAD WHERE id_funcionalidad=%s", (id_funcionalidad,))

    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("tablero", id_proyecto=id_proyecto))

# -------------------------
# Ruta 9: Ver funcionalidad y subtareas
# -------------------------
@app.route("/funcionalidad/<int:id_funcionalidad>")
def ver_funcionalidad(id_funcionalidad):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT id_funcionalidad, titulo, historia_usuario, notas_diseño, fragmento_codigo, decision_tecnica, id_seccion FROM FUNCIONALIDAD WHERE id_funcionalidad=%s",
        (id_funcionalidad,)
    )
    funcionalidad = cur.fetchone()
    
    cur.execute(
        "SELECT id_subtarea, descripcion, completada FROM SUBTAREA WHERE id_funcionalidad=%s",
        (id_funcionalidad,)
    )
    subtareas = cur.fetchall()
    
    cur.execute(
        "SELECT id_proyecto FROM SECCION WHERE id_seccion=%s",
        (funcionalidad[6],)
    )
    id_proyecto = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return render_template("funcionalidad.html", funcionalidad=funcionalidad, subtareas=subtareas, id_proyecto=id_proyecto)

# -------------------------
# Ruta 10: Agregar subtarea
# -------------------------
@app.route("/funcionalidad/<int:id_funcionalidad>/subtarea/nueva", methods=["POST"])
def nueva_subtarea(id_funcionalidad):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    descripcion = request.form["descripcion"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO SUBTAREA (descripcion, completada, id_funcionalidad) VALUES (%s, FALSE, %s)",
        (descripcion, id_funcionalidad)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("ver_funcionalidad", id_funcionalidad=id_funcionalidad))

# -------------------------
# Ruta 11: Completar subtarea
# -------------------------
@app.route("/subtarea/<int:id_subtarea>/completar", methods=["POST"])
def completar_subtarea(id_subtarea):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    id_funcionalidad = request.form["id_funcionalidad"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE SUBTAREA SET completada = NOT completada WHERE id_subtarea=%s",
        (id_subtarea,)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("ver_funcionalidad", id_funcionalidad=id_funcionalidad))

# -------------------------
# Ruta 12: Eliminar subtarea
# -------------------------
@app.route("/subtarea/<int:id_subtarea>/eliminar", methods=["POST"])
def eliminar_subtarea(id_subtarea):
    if "id_usuario" not in session:
        return redirect(url_for("login"))
    
    id_funcionalidad = request.form["id_funcionalidad"]
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM SUBTAREA WHERE id_subtarea=%s", (id_subtarea,))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for("ver_funcionalidad", id_funcionalidad=id_funcionalidad))

# -------------------------
# Ruta 13: Cerrar sesión
# -------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)