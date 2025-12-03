"""
app.py - Aplicación principal del Quiz Game
============================================

Este es el archivo principal que ejecuta la aplicación web Flask.
Es el "punto de entrada" del programa.

¿QUÉ ES FLASK?
--------------
Flask es un framework web para Python. Permite crear aplicaciones web
de forma sencilla. Los conceptos clave son:

1. RUTAS (@app.route): URLs que el usuario puede visitar
   - '/' -> Página principal
   - '/api/temas' -> Obtener lista de temas (JSON)
   - '/api/jugar' -> Iniciar partida (JSON)

2. TEMPLATES: Archivos HTML que Flask "rellena" con datos
   - render_template('index.html', datos=...) -> Devuelve HTML

3. JSON API: Endpoints que devuelven datos, no HTML
   - jsonify({'clave': 'valor'}) -> Devuelve JSON

4. SESIÓN: Almacena datos del usuario entre peticiones
   - session['usuario'] = 'Juan' -> Guarda dato
   - session.get('usuario') -> Recupera dato

ARQUITECTURA DE LA APLICACIÓN:
------------------------------
┌─────────────────────────────────────────────────────────────┐
│                    NAVEGADOR WEB                            │
│  (El usuario ve index.html con JavaScript)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (peticiones/respuestas)
┌──────────────────────────▼──────────────────────────────────┐
│                      app.py (Flask)                         │
│  - Recibe peticiones HTTP                                   │
│  - Procesa la lógica del juego                              │
│  - Devuelve HTML o JSON                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │ Importa funciones
┌──────────────────────────▼──────────────────────────────────┐
│  database.py          │           preguntas.py              │
│  - Conexión SQLite    │           - Banco de preguntas      │
│  - Crear tablas       │           - Cargar datos            │
└───────────────────────┴─────────────────────────────────────┘
                           │ SQL
┌──────────────────────────▼──────────────────────────────────┐
│                      quiz.db (SQLite)                       │
│  - Tabla temas                                              │
│  - Tabla preguntas                                          │
│  - Tabla estadisticas                                       │
└─────────────────────────────────────────────────────────────┘

CÓMO EJECUTAR:
--------------
    cd tarjetas
    uv run python app.py
    
    Luego abre: http://127.0.0.1:5000

Autor: Profesor de SAA
Fecha: 2025
"""

from flask import Flask, render_template, request, jsonify, session

# Importamos funciones de nuestros módulos
from database import get_db, init_db, tablas_vacias
from preguntas import cargar_todas_las_preguntas, mostrar_estadisticas

# =============================================================================
# CONFIGURACIÓN DE FLASK
# =============================================================================

# Crear la aplicación Flask
# __name__ le dice a Flask dónde buscar templates y archivos estáticos
app = Flask(__name__)

# Clave secreta para las sesiones (IMPORTANTE para seguridad)
# En producción, usa una clave aleatoria larga y mantenla secreta
# Esta clave se usa para firmar las cookies de sesión
app.secret_key = 'quiz_game_secret_key_2025'


# =============================================================================
# INICIALIZACIÓN
# =============================================================================

def inicializar_app():
    """
    Prepara la aplicación antes de recibir peticiones.
    
    ¿Qué hace?
    ----------
    1. Crea las tablas en la base de datos (si no existen)
    2. Si las tablas están vacías, carga las preguntas iniciales
    
    ¿Cuándo se ejecuta?
    -------------------
    Automáticamente al importar este módulo (ver línea al final).
    Es decir, cuando arranca el servidor Flask.
    
    Nota: Con debug=True, Flask reinicia el servidor cuando detecta
    cambios en el código. Por eso verás este mensaje dos veces al inicio.
    """
    # Paso 1: Asegurar que las tablas existen
    init_db()
    
    # Paso 2: Si no hay datos, cargarlos
    if tablas_vacias():
        print("📝 Cargando preguntas iniciales...")
        cargar_todas_las_preguntas()
        print("✅ Base de datos inicializada con preguntas")
        mostrar_estadisticas()
    else:
        print("✅ Base de datos ya inicializada")


# =============================================================================
# RUTAS WEB (devuelven HTML)
# =============================================================================

@app.route('/')
def index():
    """
    Página principal del quiz - Muestra el menú de temas.
    
    Decorador @app.route('/'):
    -------------------------
    Indica que esta función responde a peticiones GET a la URL raíz (/).
    Cuando alguien visita http://127.0.0.1:5000/, Flask ejecuta esta función.
    
    ¿Qué hace?
    ----------
    1. Conecta a la base de datos
    2. Obtiene la lista de temas disponibles
    3. Renderiza el template HTML pasándole los temas
    
    render_template():
    -----------------
    Busca 'index.html' en la carpeta 'templates/' y lo procesa.
    Las variables que pasamos (temas=temas) están disponibles en el HTML
    usando la sintaxis Jinja2: {{ temas }}, {% for tema in temas %}...
    
    Returns:
        str: HTML de la página principal
    """
    # Conectar a la base de datos
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtener todos los temas
    cursor.execute('SELECT * FROM temas')
    temas = cursor.fetchall()  # Lista de todos los temas
    
    # Cerrar conexión (buena práctica)
    conn.close()
    
    # Renderizar el template con los datos
    return render_template('index.html', temas=temas)


# =============================================================================
# API REST (devuelven JSON)
# =============================================================================
# Estas rutas son llamadas por JavaScript desde el navegador.
# Devuelven datos en formato JSON, no páginas HTML.

@app.route('/api/temas')
def obtener_temas():
    """
    API: Devuelve la lista de temas en formato JSON.
    
    URL: GET /api/temas
    
    ¿Para qué sirve?
    ----------------
    El JavaScript del frontend puede pedir esta información
    para mostrar los botones de temas dinámicamente.
    
    ¿Por qué convertimos a dict?
    ---------------------------
    cursor.fetchall() devuelve objetos Row de SQLite.
    jsonify() no sabe cómo convertirlos a JSON directamente.
    dict(row) convierte cada fila a un diccionario normal.
    
    Ejemplo de respuesta:
        [
            {"id": 1, "nombre": "NumPy", "descripcion": "...", "icono": "🔢"},
            {"id": 2, "nombre": "Pandas", "descripcion": "...", "icono": "🐼"}
        ]
    
    Returns:
        Response: JSON con la lista de temas
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM temas')
    
    # Convertir cada fila a diccionario para que jsonify funcione
    temas = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    # jsonify() convierte el diccionario a JSON y establece headers correctos
    return jsonify(temas)


@app.route('/api/jugar', methods=['POST'])
def iniciar_juego():
    """
    API: Inicia una nueva partida del quiz.
    
    URL: POST /api/jugar
    Body: {"tema": "NumPy"} o {"tema": "todos"}
    
    Decorador methods=['POST']:
    --------------------------
    Esta ruta solo acepta peticiones POST (no GET).
    POST se usa cuando enviamos datos al servidor.
    
    request.json:
    -------------
    Contiene los datos JSON enviados en el cuerpo de la petición.
    El frontend envía: {"tema": "NumPy"} para jugar solo NumPy.
    
    session (sesión):
    ----------------
    Flask guarda datos entre peticiones usando cookies firmadas.
    Guardamos las preguntas y el progreso del usuario aquí.
    Cada usuario tiene su propia sesión (no se mezclan).
    
    ORDER BY RANDOM() LIMIT 10:
    --------------------------
    Selecciona 10 preguntas aleatorias del tema elegido.
    Así cada partida es diferente.
    
    Ejemplo de respuesta:
        {
            "pregunta_num": 1,
            "total": 10,
            "pregunta": "¿Cuál es el alias...?",
            "opciones": {"a": "...", "b": "...", "c": "..."}
        }
    
    Returns:
        Response: JSON con la primera pregunta o error 404
    """
    # Obtener el tema del cuerpo de la petición
    datos = request.json
    tema = datos.get('tema', 'todos')  # Si no se especifica, juega con todos
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Seleccionar 10 preguntas aleatorias
    if tema == 'todos':
        # De todos los temas
        cursor.execute('SELECT * FROM preguntas ORDER BY RANDOM() LIMIT 10')
    else:
        # Solo del tema especificado (usamos JOIN para filtrar por nombre)
        cursor.execute('''
            SELECT p.* FROM preguntas p
            JOIN temas t ON p.tema_id = t.id
            WHERE t.nombre = ?
            ORDER BY RANDOM() LIMIT 10
        ''', (tema,))
    
    preguntas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Guardar estado del juego en la sesión del usuario
    session['preguntas'] = preguntas       # Lista de preguntas de esta partida
    session['tema'] = tema                  # Tema elegido
    session['pregunta_actual'] = 0          # Índice de la pregunta actual
    session['correctas'] = 0                # Contador de aciertos
    
    # Si hay preguntas, devolver la primera
    if preguntas:
        pregunta = preguntas[0]
        return jsonify({
            'pregunta_num': 1,                    # Número de pregunta (1 de 10)
            'total': len(preguntas),              # Total de preguntas
            'pregunta': pregunta['pregunta'],     # Texto de la pregunta
            'opciones': {                         # Las 3 opciones
                'a': pregunta['opcion_a'],
                'b': pregunta['opcion_b'],
                'c': pregunta['opcion_c']
            }
        })
    else:
        # No hay preguntas para ese tema
        return jsonify({'error': 'No hay preguntas disponibles'}), 404


@app.route('/api/responder', methods=['POST'])
def responder():
    """
    API: Procesa la respuesta del usuario a una pregunta.
    
    URL: POST /api/responder
    Body: {"respuesta": "b"}
    
    ¿Qué hace?
    ----------
    1. Recibe la respuesta del usuario ('a', 'b' o 'c')
    2. Compara con la respuesta correcta
    3. Actualiza el contador de aciertos
    4. Devuelve si es correcta + explicación
    5. Si hay más preguntas, incluye la siguiente
    6. Si era la última, guarda estadísticas y devuelve resultado final
    
    Flujo del juego:
    ---------------
    [Frontend] ─── POST /api/jugar ───────► [Backend] Devuelve pregunta 1
    [Frontend] ◄── pregunta 1 ─────────────
    [Frontend] ─── POST /api/responder ───► [Backend] Evalúa y devuelve pregunta 2
    [Frontend] ◄── resultado + pregunta 2 ─
    ...
    [Frontend] ─── POST /api/responder ───► [Backend] Evalúa pregunta 10
    [Frontend] ◄── resultado final ────────           y guarda estadísticas
    
    Ejemplo de respuesta (pregunta intermedia):
        {
            "correcta": true,
            "respuesta_correcta": "b",
            "explicacion": "np.sum() suma todos los elementos...",
            "correctas_acumuladas": 5,
            "siguiente": {
                "pregunta_num": 6,
                "total": 10,
                "pregunta": "...",
                "opciones": {...}
            }
        }
    
    Ejemplo de respuesta (última pregunta):
        {
            "correcta": false,
            "respuesta_correcta": "a",
            "explicacion": "...",
            "correctas_acumuladas": 7,
            "fin": {
                "correctas": 7,
                "total": 10,
                "porcentaje": 70.0
            }
        }
    
    Returns:
        Response: JSON con el resultado y siguiente pregunta (o fin)
    """
    # Obtener la respuesta enviada por el usuario
    datos = request.json
    respuesta_usuario = datos.get('respuesta')
    
    # Recuperar el estado del juego de la sesión
    preguntas = session.get('preguntas', [])
    idx = session.get('pregunta_actual', 0)  # Índice de la pregunta actual
    
    # Validación: ¿hay pregunta para responder?
    if idx >= len(preguntas):
        return jsonify({'error': 'No hay más preguntas'}), 400
    
    # Obtener la pregunta actual y verificar la respuesta
    pregunta_actual = preguntas[idx]
    es_correcta = respuesta_usuario == pregunta_actual['respuesta_correcta']
    
    # Si es correcta, incrementar contador
    if es_correcta:
        session['correctas'] = session.get('correctas', 0) + 1
    
    # Avanzar a la siguiente pregunta
    session['pregunta_actual'] = idx + 1
    
    # Preparar respuesta base
    resultado = {
        'correcta': es_correcta,                           # ¿Acertó?
        'respuesta_correcta': pregunta_actual['respuesta_correcta'],  # Cuál era
        'explicacion': pregunta_actual['explicacion'],     # Por qué
        'correctas_acumuladas': session['correctas']       # Aciertos totales
    }
    
    # ¿Hay más preguntas?
    if idx + 1 < len(preguntas):
        # Sí hay más: incluir la siguiente pregunta
        siguiente = preguntas[idx + 1]
        resultado['siguiente'] = {
            'pregunta_num': idx + 2,
            'total': len(preguntas),
            'pregunta': siguiente['pregunta'],
            'opciones': {
                'a': siguiente['opcion_a'],
                'b': siguiente['opcion_b'],
                'c': siguiente['opcion_c']
            }
        }
    else:
        # Era la última pregunta: fin del juego
        total = len(preguntas)
        correctas = session['correctas']
        porcentaje = (correctas / total) * 100 if total > 0 else 0
        
        # Guardar en la tabla de estadísticas para historial
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO estadisticas (tema, correctas, total, porcentaje)
            VALUES (?, ?, ?, ?)
        ''', (session.get('tema', 'todos'), correctas, total, porcentaje))
        conn.commit()
        conn.close()
        
        # Incluir resumen final
        resultado['fin'] = {
            'correctas': correctas,
            'total': total,
            'porcentaje': porcentaje
        }
    
    return jsonify(resultado)


@app.route('/api/estadisticas')
def obtener_estadisticas():
    """
    API: Devuelve el historial de las últimas partidas.
    
    URL: GET /api/estadisticas
    
    ¿Para qué sirve?
    ----------------
    Para mostrar un historial de partidas anteriores.
    Útil para ver el progreso del estudiante.
    
    ORDER BY fecha DESC LIMIT 10:
    ----------------------------
    Ordena por fecha descendente (más recientes primero)
    y limita a las 10 últimas partidas.
    
    Ejemplo de respuesta:
        [
            {"id": 5, "fecha": "2025-12-03 10:30:00", "tema": "NumPy", 
             "correctas": 8, "total": 10, "porcentaje": 80.0},
            {"id": 4, "fecha": "2025-12-03 10:15:00", "tema": "Pandas",
             "correctas": 6, "total": 10, "porcentaje": 60.0},
            ...
        ]
    
    Returns:
        Response: JSON con las últimas 10 partidas
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM estadisticas 
        ORDER BY fecha DESC 
        LIMIT 10
    ''')
    
    stats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(stats)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

# Esta línea se ejecuta cuando Python carga este módulo.
# Inicializa la base de datos y carga las preguntas si es necesario.
inicializar_app()

# El bloque if __name__ == '__main__' solo se ejecuta si ejecutas
# directamente este archivo: python app.py
# No se ejecuta si otro archivo hace: from app import app
if __name__ == '__main__':
    # app.run() arranca el servidor web de desarrollo de Flask
    # 
    # Parámetros:
    # - debug=True: 
    #   * Muestra errores detallados en el navegador
    #   * Reinicia automáticamente cuando cambias el código
    #   * ¡NUNCA uses debug=True en producción!
    #
    # - host='127.0.0.1': 
    #   * Solo accesible desde tu ordenador (localhost)
    #   * Usa '0.0.0.0' para que otros ordenadores de la red puedan acceder
    #
    # - port=5000: 
    #   * Puerto donde escucha el servidor
    #   * Accedes en http://127.0.0.1:5000
    #
    app.run(debug=True, host='127.0.0.1', port=5000)
