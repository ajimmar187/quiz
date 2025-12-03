"""
database.py - Módulo de gestión de la base de datos SQLite
==========================================================

Este módulo se encarga de toda la interacción con la base de datos SQLite.
Contiene funciones para:
  - Conectarse a la base de datos
  - Crear las tablas necesarias
  - Verificar si hay datos cargados
  - Operaciones auxiliares de consulta

CONCEPTOS CLAVE:
----------------
- SQLite: Base de datos ligera que guarda todo en un solo archivo (.db)
- Cursor: Objeto que permite ejecutar consultas SQL y recorrer resultados
- Connection: Objeto que representa la conexión a la base de datos
- row_factory: Permite acceder a las columnas por nombre (como diccionario)

PATRÓN DE USO TÍPICO:
--------------------
    conn = get_db()           # 1. Abrir conexión
    cursor = conn.cursor()    # 2. Crear cursor
    cursor.execute(sql)       # 3. Ejecutar SQL
    resultados = cursor.fetchall()  # 4. Obtener resultados
    conn.commit()             # 5. Guardar cambios (si hay INSERT/UPDATE/DELETE)
    conn.close()              # 6. Cerrar conexión (¡importante!)

Autor: Profesor de SAA
Fecha: 2025
"""

import sqlite3
from pathlib import Path

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Ruta de la base de datos - se guarda en la misma carpeta que este archivo
# Path(__file__) -> ruta de este archivo (database.py)
# .parent -> carpeta que contiene este archivo (tarjetas/)
# / "quiz.db" -> añade el nombre del archivo de base de datos
DB_PATH = Path(__file__).parent / "quiz.db"


# =============================================================================
# FUNCIONES DE CONEXIÓN
# =============================================================================

def get_db():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    
    ¿Qué hace?
    ----------
    1. Abre (o crea si no existe) el archivo quiz.db
    2. Configura row_factory para poder acceder a columnas por nombre
    
    ¿Por qué row_factory = sqlite3.Row?
    -----------------------------------
    Sin row_factory:  resultado[0], resultado[1], resultado[2]...
    Con row_factory:  resultado['nombre'], resultado['edad']...
    
    Mucho más legible y menos propenso a errores.
    
    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos
    
    Ejemplo de uso:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM temas')
        for fila in cursor.fetchall():
            print(fila['nombre'])  # Acceso por nombre de columna
        conn.close()
    """
    # sqlite3.connect() abre el archivo. Si no existe, lo crea.
    conn = sqlite3.connect(DB_PATH)
    
    # row_factory permite acceder a las columnas por nombre
    # Ejemplo: fila['nombre'] en lugar de fila[0]
    conn.row_factory = sqlite3.Row
    
    return conn


# =============================================================================
# FUNCIONES DE INICIALIZACIÓN
# =============================================================================

def init_db():
    """
    Inicializa la base de datos creando todas las tablas necesarias.
    
    ¿Qué hace?
    ----------
    Crea 3 tablas si no existen:
    
    1. TEMAS: Categorías de preguntas (NumPy, Pandas, etc.)
       - id: Identificador único (se genera automáticamente)
       - nombre: Nombre del tema (único, no puede repetirse)
       - descripcion: Texto descriptivo del tema
       - icono: Emoji para mostrar en la interfaz
    
    2. PREGUNTAS: Banco de preguntas del quiz
       - id: Identificador único
       - tema_id: Relación con la tabla temas (FK = Foreign Key)
       - pregunta: El texto de la pregunta
       - opcion_a, opcion_b, opcion_c: Las 3 opciones de respuesta
       - respuesta_correcta: 'a', 'b' o 'c'
       - explicacion: Texto que explica la respuesta correcta
    
    3. ESTADÍSTICAS: Historial de partidas jugadas
       - id: Identificador único
       - fecha: Cuándo se jugó (se pone automáticamente)
       - tema: Qué tema se jugó
       - correctas: Número de aciertos
       - total: Número total de preguntas
       - porcentaje: Porcentaje de aciertos
    
    Nota sobre CREATE TABLE IF NOT EXISTS:
    --------------------------------------
    Esta sintaxis evita errores si la tabla ya existe.
    Es seguro ejecutar esta función múltiples veces.
    
    Nota sobre FOREIGN KEY:
    ----------------------
    tema_id en 'preguntas' referencia a id en 'temas'.
    Esto asegura integridad: no puedes tener una pregunta
    con un tema_id que no existe en la tabla temas.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # -------------------------------------------------------------------------
    # Tabla de TEMAS (categorías de preguntas)
    # -------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            icono TEXT DEFAULT '📚'
        )
    ''')
    # PRIMARY KEY AUTOINCREMENT: SQLite genera el ID automáticamente (1, 2, 3...)
    # NOT NULL: El campo es obligatorio
    # UNIQUE: No puede haber dos temas con el mismo nombre
    # DEFAULT: Valor por defecto si no se especifica
    
    # -------------------------------------------------------------------------
    # Tabla de PREGUNTAS
    # -------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema_id INTEGER NOT NULL,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL CHECK(respuesta_correcta IN ('a', 'b', 'c')),
            explicacion TEXT,
            FOREIGN KEY (tema_id) REFERENCES temas(id)
        )
    ''')
    # CHECK: Restricción que valida que respuesta_correcta solo sea 'a', 'b' o 'c'
    # FOREIGN KEY: Crea una relación con la tabla temas
    
    # -------------------------------------------------------------------------
    # Tabla de ESTADÍSTICAS (historial de partidas)
    # -------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estadisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tema TEXT,
            correctas INTEGER,
            total INTEGER,
            porcentaje REAL
        )
    ''')
    # TIMESTAMP: Tipo de dato para fechas y horas
    # CURRENT_TIMESTAMP: Se rellena automáticamente con la fecha/hora actual
    # REAL: Número decimal (para el porcentaje)
    
    # Guardar los cambios en la base de datos
    conn.commit()
    
    # Cerrar la conexión (libera recursos)
    conn.close()


# =============================================================================
# FUNCIONES DE VERIFICACIÓN
# =============================================================================

def tablas_vacias():
    """
    Comprueba si las tablas de temas y preguntas están vacías.
    
    ¿Para qué sirve?
    ----------------
    Para saber si necesitamos cargar las preguntas iniciales.
    Si ya hay datos, no los volvemos a cargar (evitamos duplicados).
    
    Returns:
        bool: True si alguna tabla está vacía, False si ambas tienen datos
    
    Ejemplo:
        if tablas_vacias():
            cargar_preguntas_iniciales()
        else:
            print("Ya hay preguntas cargadas")
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Contar registros en la tabla temas
    # COUNT(*) devuelve el número de filas
    cursor.execute('SELECT COUNT(*) FROM temas')
    temas_count = cursor.fetchone()[0]  # fetchone() devuelve una tupla, [0] es el primer elemento
    
    # Contar registros en la tabla preguntas
    cursor.execute('SELECT COUNT(*) FROM preguntas')
    preguntas_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Si alguna está vacía (count == 0), devolvemos True
    return temas_count == 0 or preguntas_count == 0


# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def obtener_id_tema(nombre):
    """
    Obtiene el ID de un tema dado su nombre.
    
    ¿Para qué sirve?
    ----------------
    Cuando insertamos preguntas, necesitamos el ID del tema,
    no su nombre. Esta función hace esa conversión.
    
    Args:
        nombre (str): Nombre del tema (ej: "NumPy", "Pandas")
    
    Returns:
        int o None: ID del tema si existe, None si no se encuentra
    
    Ejemplo:
        numpy_id = obtener_id_tema("NumPy")  # Devuelve 1 (por ejemplo)
        pandas_id = obtener_id_tema("Pandas")  # Devuelve 2
        inexistente = obtener_id_tema("Java")  # Devuelve None
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # El ? es un placeholder - SQLite lo reemplaza por el valor de forma segura
    # Esto previene ataques de SQL Injection
    cursor.execute('SELECT id FROM temas WHERE nombre = ?', (nombre,))
    
    resultado = cursor.fetchone()  # Devuelve una fila o None si no hay resultados
    conn.close()
    
    # Si encontró resultado, devuelve el ID; si no, devuelve None
    return resultado[0] if resultado else None


def contar_preguntas():
    """
    Cuenta el total de preguntas agrupadas por tema.
    
    ¿Para qué sirve?
    ----------------
    Para mostrar estadísticas: "NumPy: 45 preguntas, Pandas: 50 preguntas"
    
    Returns:
        dict: Diccionario con formato {'NombreTema': cantidad, ...}
    
    Ejemplo de retorno:
        {'NumPy': 45, 'Pandas': 50}
    
    Nota sobre LEFT JOIN:
    --------------------
    Usamos LEFT JOIN para incluir temas aunque no tengan preguntas.
    Con JOIN normal, un tema sin preguntas no aparecería.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Esta consulta:
    # 1. Une las tablas temas y preguntas
    # 2. Cuenta cuántas preguntas hay por cada tema
    # 3. GROUP BY agrupa los resultados por tema
    cursor.execute('''
        SELECT t.nombre, COUNT(p.id) as total
        FROM temas t
        LEFT JOIN preguntas p ON t.id = p.tema_id
        GROUP BY t.id
    ''')
    
    # Convertimos los resultados a un diccionario
    # dict comprehension: {clave: valor for fila in resultados}
    resultado = {row['nombre']: row['total'] for row in cursor.fetchall()}
    conn.close()
    
    return resultado
