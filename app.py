from flask import Flask, render_template, request, jsonify
from db import get_connection, init_db

app = Flask(__name__)

# Crea las tablas (si no existen) apenas arranca la aplicación
init_db()


# ============================================================
#  UTILIDAD DE VALIDACIÓN
# ============================================================
def validar_campos(data, campos_obligatorios):
    """
    Revisa que todos los campos obligatorios vengan en el JSON y no estén vacíos.
    Devuelve una lista con los nombres de los campos que faltan o están vacíos.
    """
    faltantes = []
    for campo in campos_obligatorios:
        valor = data.get(campo)
        if valor is None or (isinstance(valor, str) and valor.strip() == ""):
            faltantes.append(campo)
    return faltantes


# ============================================================
#  PÁGINAS
# ============================================================
@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ============================================================
#  API: MATRÍCULAS (usado por el dashboard admin)
# ============================================================
@app.route("/api/matriculas", methods=["GET"])
def get_matriculas():
    conn = get_connection()
    filas = conn.execute("SELECT * FROM matriculas ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas])


@app.route("/api/matriculas", methods=["POST"])
def crear_matricula():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["alumno", "nivel", "apoderado", "telefono", "estado"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO matriculas (alumno, edad, nivel, apoderado, telefono, comentarios, estado) VALUES (?,?,?,?,?,?,?)",
        (data["alumno"].strip(), data.get("edad") or None, data["nivel"], data["apoderado"].strip(),
         data["telefono"].strip(), data.get("comentarios", "").strip(), data["estado"])
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": nuevo_id}), 201


@app.route("/api/matriculas/<int:id>", methods=["PUT"])
def editar_matricula(id):
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["alumno", "nivel", "apoderado", "telefono", "estado"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "UPDATE matriculas SET alumno=?, edad=?, nivel=?, apoderado=?, telefono=?, comentarios=?, estado=? WHERE id=?",
        (data["alumno"].strip(), data.get("edad") or None, data["nivel"], data["apoderado"].strip(),
         data["telefono"].strip(), data.get("comentarios", "").strip(), data["estado"], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/matriculas/<int:id>", methods=["DELETE"])
def borrar_matricula(id):
    conn = get_connection()
    conn.execute("DELETE FROM matriculas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ============================================================
#  API: MATRÍCULA PÚBLICA (formulario de la página principal)
# ============================================================
@app.route("/api/matricula-publica", methods=["POST"])
def matricula_publica():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["alumno", "edad", "nivel", "apoderado", "telefono"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO matriculas (alumno, edad, nivel, apoderado, telefono, comentarios, estado) VALUES (?,?,?,?,?,?,?)",
        (data["alumno"].strip(), data["edad"], data["nivel"], data["apoderado"].strip(),
         data["telefono"].strip(), data.get("comentarios", "").strip(), "Pendiente")
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "mensaje": "¡Solicitud de matrícula recibida! Te contactaremos pronto."}), 201


# ============================================================
#  API: ALUMNOS
# ============================================================
@app.route("/api/alumnos", methods=["GET"])
def get_alumnos():
    conn = get_connection()
    filas = conn.execute("SELECT * FROM alumnos ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas])


@app.route("/api/alumnos", methods=["POST"])
def crear_alumno():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "grado", "edad", "apoderado", "telefono"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO alumnos (nombre, grado, edad, apoderado, telefono) VALUES (?,?,?,?,?)",
        (data["nombre"].strip(), data["grado"], data["edad"], data["apoderado"].strip(), data["telefono"].strip())
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": nuevo_id}), 201


@app.route("/api/alumnos/<int:id>", methods=["PUT"])
def editar_alumno(id):
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "grado", "edad", "apoderado", "telefono"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "UPDATE alumnos SET nombre=?, grado=?, edad=?, apoderado=?, telefono=? WHERE id=?",
        (data["nombre"].strip(), data["grado"], data["edad"], data["apoderado"].strip(), data["telefono"].strip(), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/alumnos/<int:id>", methods=["DELETE"])
def borrar_alumno(id):
    conn = get_connection()
    conn.execute("DELETE FROM alumnos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ============================================================
#  API: DOCENTES
# ============================================================
@app.route("/api/docentes", methods=["GET"])
def get_docentes():
    conn = get_connection()
    filas = conn.execute("SELECT * FROM docentes ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas])


@app.route("/api/docentes", methods=["POST"])
def crear_docente():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "especialidad", "nivel", "telefono"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO docentes (nombre, especialidad, nivel, telefono) VALUES (?,?,?,?)",
        (data["nombre"].strip(), data["especialidad"].strip(), data["nivel"], data["telefono"].strip())
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": nuevo_id}), 201


@app.route("/api/docentes/<int:id>", methods=["PUT"])
def editar_docente(id):
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "especialidad", "nivel", "telefono"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "UPDATE docentes SET nombre=?, especialidad=?, nivel=?, telefono=? WHERE id=?",
        (data["nombre"].strip(), data["especialidad"].strip(), data["nivel"], data["telefono"].strip(), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/docentes/<int:id>", methods=["DELETE"])
def borrar_docente(id):
    conn = get_connection()
    conn.execute("DELETE FROM docentes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ============================================================
#  API: PRODUCTOS (tienda escolar)
# ============================================================
@app.route("/api/productos", methods=["GET"])
def get_productos():
    conn = get_connection()
    filas = conn.execute("SELECT * FROM productos ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(f) for f in filas])


@app.route("/api/productos", methods=["POST"])
def crear_producto():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "categoria", "precio", "stock"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?,?,?,?)",
        (data["nombre"].strip(), data["categoria"], float(data["precio"]), int(data["stock"]))
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": nuevo_id}), 201


@app.route("/api/productos/<int:id>", methods=["PUT"])
def editar_producto(id):
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "categoria", "precio", "stock"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?",
        (data["nombre"].strip(), data["categoria"], float(data["precio"]), int(data["stock"]), id)
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.route("/api/productos/<int:id>", methods=["DELETE"])
def borrar_producto(id):
    conn = get_connection()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


# ============================================================
#  API: CONTACTO (formulario de la página principal)
# ============================================================
@app.route("/api/contacto", methods=["POST"])
def crear_contacto():
    data = request.get_json(force=True, silent=True) or {}
    faltantes = validar_campos(data, ["nombre", "telefono", "motivo", "mensaje"])
    if faltantes:
        return jsonify({"error": "Faltan campos obligatorios", "campos": faltantes}), 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO contactos (nombre, telefono, motivo, mensaje) VALUES (?,?,?,?)",
        (data["nombre"].strip(), data["telefono"].strip(), data["motivo"], data["mensaje"].strip())
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "mensaje": "¡Mensaje enviado! Te responderemos pronto."}), 201


if __name__ == "__main__":
    app.run(debug=True)