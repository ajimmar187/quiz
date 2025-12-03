# 🎯 Quiz Master - NumPy & Pandas

Un juego de preguntas y respuestas sobre NumPy y Pandas construido con Flask y SQLite.

## Características

✅ **Temas disponibles:** NumPy, Pandas, o todos mezclados
✅ **10 preguntas por ronda** seleccionadas aleatoriamente
✅ **3 opciones de respuesta** por pregunta
✅ **Explicaciones** después de cada respuesta
✅ **Puntuación final** con mensaje personalizado
✅ **Base de datos SQLite** para almacenar preguntas (fácil de ampliar)
✅ **Estadísticas** de partidas jugadas
✅ **Interfaz moderna** con animaciones

## 📥 Descargar el proyecto

### Opción 1: Con Git
```bash
git clone https://github.com/ajimmar187/quiz.git
cd quiz
```

### Opción 2: Descargar como ZIP
1. Ve a https://github.com/ajimmar187/quiz
2. Haz clic en el botón **Code** (verde)
3. Selecciona **Download ZIP**
4. Descomprime el archivo en tu equipo
5. Abre una terminal y navega a la carpeta del proyecto:
```bash
cd quiz
```

## 🔨 Construcción del proyecto

Instala las dependencias usando `uv`:

```bash
uv sync
```

Este comando instalará todas las dependencias definidas en `pyproject.toml`.

## ▶️ Ejecutar la aplicación

### Iniciar el servidor
```bash
uv run python app.py
```

Verás un mensaje similar a:
```
 * Running on http://127.0.0.1:5000
```

### Abrir en el navegador
Una vez que el servidor esté en ejecución, abre tu navegador y ve a:
```
http://127.0.0.1:5000
```

### Parar el servidor
Presiona **Ctrl + C** en la terminal donde está ejecutándose la aplicación.

Esto detendrá el servidor Flask inmediatamente.

## Estructura de archivos

```
quiz/
├── app.py              # Aplicación Flask principal
├── database.py         # Configuración y gestión de base de datos
├── preguntas.py        # Datos de preguntas
├── quiz.db             # Base de datos SQLite (se crea automáticamente)
├── pyproject.toml      # Dependencias del proyecto
├── README.md           # Este archivo
├── .gitignore          # Archivos a ignorar en Git
├── templates/
│   └── index.html      # Interfaz del juego
└── __pycache__/        # Archivos compilados de Python (no versionar)
```

## Base de datos

La aplicación usa SQLite con 3 tablas:

### Tabla `temas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| nombre | TEXT | Nombre del tema (NumPy, Pandas) |
| descripcion | TEXT | Descripción corta |
| icono | TEXT | Emoji del tema |

### Tabla `preguntas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| tema_id | INTEGER | FK a temas |
| pregunta | TEXT | Texto de la pregunta |
| opcion_a | TEXT | Primera opción |
| opcion_b | TEXT | Segunda opción |
| opcion_c | TEXT | Tercera opción |
| respuesta_correcta | TEXT | 'a', 'b' o 'c' |
| explicacion | TEXT | Explicación de la respuesta |

### Tabla `estadisticas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único |
| fecha | TIMESTAMP | Fecha y hora |
| tema | TEXT | Tema jugado |
| correctas | INTEGER | Respuestas correctas |
| total | INTEGER | Total de preguntas |
| porcentaje | REAL | Porcentaje de acierto |

## Agregar más preguntas

Puedes agregar preguntas directamente a la base de datos:

```python
import sqlite3

conn = sqlite3.connect('tarjetas/quiz.db')
cursor = conn.cursor()

# Obtener ID del tema
cursor.execute('SELECT id FROM temas WHERE nombre = "NumPy"')
tema_id = cursor.fetchone()[0]

# Insertar pregunta
cursor.execute('''
    INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, respuesta_correcta, explicacion)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (tema_id, '¿Tu pregunta?', 'Opción A', 'Opción B', 'Opción C', 'b', 'Explicación'))

conn.commit()
conn.close()
```

## Agregar nuevos temas

```python
import sqlite3

conn = sqlite3.connect('tarjetas/quiz.db')
cursor = conn.cursor()

cursor.execute('''
    INSERT INTO temas (nombre, descripcion, icono)
    VALUES (?, ?, ?)
''', ('SQL', 'Bases de datos relacionales', '🗃️'))

conn.commit()
conn.close()
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página principal |
| GET | `/api/temas` | Lista de temas |
| POST | `/api/jugar` | Iniciar partida |
| POST | `/api/responder` | Enviar respuesta |
| GET | `/api/estadisticas` | Historial de partidas |

## Tecnologías

- **Backend:** Flask (Python)
- **Base de datos:** SQLite
- **Frontend:** HTML, CSS, JavaScript vanilla
- **Estilos:** CSS moderno con gradientes y animaciones

---

¡Buena suerte con el quiz! 🍀
