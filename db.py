import pyodbc

# ============================
# COMPLETA ESTOS DATOS
# ============================
SERVER   = 'localhost'   # Instancia por defecto (MSSQLSERVER), sin sufijo
DATABASE = 'BD_Mundo_Rayati'
DRIVER   = 'ODBC Driver 18 for SQL Server'

# Autenticacion de Windows: usa tu usuario de Windows actual automaticamente,
# no necesita UID ni PWD.
CONN_STRING = (
    f'DRIVER={{{DRIVER}}};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'Trusted_Connection=yes;'
    f'TrustServerCertificate=yes;'
)


def get_connection():
    """Abre y devuelve una nueva conexion a la base de datos."""
    return pyodbc.connect(CONN_STRING)


# ============================
# PRUEBA RAPIDA DE CONEXION
# ============================
if __name__ == '__main__':
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT @@VERSION')
        version = cursor.fetchone()
        print('Conexion exitosa a SQL Server')
        print(version[0])
        conn.close()
    except Exception as e:
        print('Error al conectar:')
        print(e)