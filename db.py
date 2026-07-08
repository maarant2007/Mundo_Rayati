import sqlite3
import os

# Ruta del archivo de base de datos (se crea junto al proyecto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mundo_rayati.db")


def get_connection():
    """Abre y devuelve una nueva conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a las columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Crea todas las tablas si no existen todavía. Se llama al arrancar la app."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matriculas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno TEXT NOT NULL,
            edad INTEGER,
            nivel TEXT NOT NULL,
            apoderado TEXT NOT NULL,
            telefono TEXT NOT NULL,
            comentarios TEXT,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            creado_en TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            grado TEXT NOT NULL,
            edad INTEGER NOT NULL,
            apoderado TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS docentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT NOT NULL,
            nivel TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            motivo TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            creado_en TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    # Datos de ejemplo solo si las tablas están vacías (para que el dashboard no se vea vacío la primera vez)
    if cur.execute("SELECT COUNT(*) FROM matriculas").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO matriculas (alumno, edad, nivel, apoderado, telefono, comentarios, estado) VALUES (?,?,?,?,?,?,?)",
            [
                ("Ana García", 4, "Inicial – 4 años", "Rosa García", "+51 945373930", "", "Confirmado"),
                ("Luis Pérez", 7, "Primaria – 2° grado", "Carlos Pérez", "+51 912345678", "", "Pendiente"),
                ("Sofía Torres", 11, "Primaria – 5° grado", "María Torres", "+51 987654321", "", "En proceso"),
            ]
        )

    if cur.execute("SELECT COUNT(*) FROM alumnos").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO alumnos (nombre, grado, edad, apoderado, telefono) VALUES (?,?,?,?,?)",
            [
                ("Ana García", "Inicial – 4 años", 4, "Rosa García", "+51 945373930"),
                ("Luis Pérez", "Primaria – 2° grado", 7, "Carlos Pérez", "+51 912345678"),
                ("Sofía Torres", "Primaria – 5° grado", 11, "María Torres", "+51 987654321"),
                ("Diego Ramírez", "Primaria – 1° grado", 6, "Juan Ramírez", "+51 934567890"),
            ]
        )

    if cur.execute("SELECT COUNT(*) FROM docentes").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO docentes (nombre, especialidad, nivel, telefono) VALUES (?,?,?,?)",
            [
                ("Sra. Lucía Mendoza", "Comunicación", "Primaria", "+51 911111111"),
                ("Sr. Marcos Quispe", "Matemática", "Primaria", "+51 922222222"),
                ("Sra. Elena Vargas", "Inicial", "Inicial", "+51 933333333"),
            ]
        )

    if cur.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?,?,?,?)",
            [
                ("Comunicación – Nivel Inicial", "Libros", 35.00, 20),
                ("Matemática – Nivel Inicial", "Libros", 32.00, 15),
                ("Polo Colegio", "Uniforme", 28.00, 50),
                ("Buzo Completo", "Uniforme", 85.00, 30),
                ("Agenda Escolar", "Agenda", 20.00, 100),
            ]
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Base de datos creada/verificada en: {DB_PATH}")