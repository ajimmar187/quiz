"""
preguntas.py - Módulo de preguntas del Quiz
============================================

Este módulo contiene todas las preguntas del quiz organizadas por tema
y la lógica para cargarlas en la base de datos.

ESTRUCTURA DEL MÓDULO:
---------------------
1. TEMAS: Lista de categorías disponibles
2. get_preguntas_numpy(): Devuelve todas las preguntas de NumPy
3. get_preguntas_pandas(): Devuelve todas las preguntas de Pandas
4. cargar_todas_las_preguntas(): Inserta todo en la base de datos
5. mostrar_estadisticas(): Muestra un resumen de preguntas cargadas

FORMATO DE CADA PREGUNTA:
------------------------
Cada pregunta es una tupla con 7 elementos:
(tema_id, pregunta, opcion_a, opcion_b, opcion_c, respuesta_correcta, explicacion)

Ejemplo:
    (1, '¿Qué función suma elementos?', 'np.add()', 'np.sum()', 'np.plus()', 'b', 'np.sum() suma todos.')

CÓMO AÑADIR MÁS PREGUNTAS:
-------------------------
1. Localiza la función get_preguntas_TEMA() correspondiente
2. Añade una nueva tupla a la lista con el formato indicado
3. Asegúrate de que respuesta_correcta sea 'a', 'b' o 'c'
4. Elimina el archivo quiz.db para regenerar la base de datos
5. Ejecuta la aplicación de nuevo

Autor: Profesor de SAA
Fecha: 2025
"""

from database import get_db


# =============================================================================
# DEFINICIÓN DE TEMAS
# =============================================================================

# Lista de temas disponibles en el quiz
# Cada tema es una tupla: (nombre, descripcion, icono_emoji)
# Puedes añadir más temas aquí, por ejemplo:
#   ('SQL', 'Consultas a bases de datos', '🗄️'),
#   ('Matplotlib', 'Visualización de datos', '📈'),
TEMAS = [
    ('NumPy', 'Computación numérica con arrays', '🔢'),
    ('Pandas', 'Análisis y manipulación de datos', '🐼'),
]


# =============================================================================
# PREGUNTAS DE NUMPY
# =============================================================================

def get_preguntas_numpy(tema_id):
    """
    Devuelve todas las preguntas del tema NumPy.
    
    ¿Por qué recibe tema_id como parámetro?
    ---------------------------------------
    Porque necesitamos asociar cada pregunta con su tema en la base de datos.
    El tema_id es el identificador único del tema "NumPy" en la tabla temas.
    
    Args:
        tema_id (int): ID del tema NumPy en la base de datos
    
    Returns:
        list: Lista de tuplas, cada una con formato:
              (tema_id, pregunta, opcion_a, opcion_b, opcion_c, 
               respuesta_correcta, explicacion)
    
    Tipos de preguntas incluidas:
    ----------------------------
    1. Conceptuales básicas: Qué es, cómo funciona, cuál es el alias...
    2. Prácticas "¿Qué usarías para...?": Orientadas a resolver problemas
    
    Para añadir una pregunta nueva, copia este formato:
        (tema_id, 
         '¿Tu pregunta aquí?',           # La pregunta
         'Opción A',                      # Primera opción
         'Opción B',                      # Segunda opción  
         'Opción C',                      # Tercera opción
         'b',                             # Letra correcta: 'a', 'b' o 'c'
         'Explicación de por qué es correcta.'  # Feedback educativo
        ),
    """
    return [
        # Preguntas conceptuales básicas
        (tema_id, '¿Cuál es el alias estándar para importar NumPy?', 'import numpy as num', 'import numpy as np', 'import numpy as npy', 'b', 'Por convención universal, NumPy se importa como np.'),
        (tema_id, '¿Qué función crea un array de ceros?', 'np.zeros()', 'np.empty()', 'np.null()', 'a', 'np.zeros() crea un array lleno de ceros.'),
        (tema_id, '¿Qué atributo devuelve las dimensiones de un array?', '.size', '.shape', '.dim', 'b', '.shape devuelve una tupla con las dimensiones del array.'),
        (tema_id, '¿Qué tipo de dato representa números decimales en NumPy?', 'int64', 'float64', 'decimal64', 'b', 'float64 es el tipo estándar para números decimales.'),
        (tema_id, '¿Cuál es la principal ventaja de los arrays sobre las listas?', 'Son más fáciles de crear', 'Son más rápidos para operaciones numéricas', 'Pueden almacenar diferentes tipos de datos', 'b', 'NumPy está optimizado para operaciones numéricas vectorizadas.'),
        (tema_id, '¿Qué función genera números equiespaciados en un intervalo?', 'np.arange()', 'np.linspace()', 'np.space()', 'b', 'np.linspace() genera n números equiespaciados entre dos valores.'),
        (tema_id, '¿Qué significa que un array sea "homogéneo"?', 'Que tiene una sola dimensión', 'Que todos sus elementos son del mismo tipo', 'Que tiene el mismo número de filas y columnas', 'b', 'Los arrays NumPy son homogéneos: todos los elementos tienen el mismo tipo.'),
        (tema_id, '¿Qué atributo indica el número de dimensiones?', '.ndim', '.dims', '.dimensions', 'a', '.ndim devuelve el número de dimensiones del array.'),
        (tema_id, '¿Qué operación es "vectorizada"?', 'Un bucle for que recorre el array', 'Una operación que se aplica a todos los elementos a la vez', 'Una operación que crea vectores', 'b', 'Las operaciones vectorizadas se aplican a todos los elementos simultáneamente.'),
        (tema_id, '¿Cómo se accede al último elemento de un array?', 'array[last]', 'array[-1]', 'array[end]', 'b', 'El índice -1 accede al último elemento.'),
        (tema_id, '¿Qué función calcula la media de un array?', 'np.mean()', 'np.average()', 'Ambas son correctas', 'c', 'Tanto np.mean() como np.average() calculan la media.'),
        (tema_id, '¿Qué hace np.reshape()?', 'Elimina elementos del array', 'Cambia la forma del array sin modificar los datos', 'Ordena los elementos', 'b', 'reshape() reorganiza los elementos en una nueva forma.'),
        (tema_id, '¿Qué es el "broadcasting" en NumPy?', 'Transmitir datos por red', 'Operar arrays de diferentes tamaños automáticamente', 'Copiar un array', 'b', 'Broadcasting permite operaciones entre arrays de diferentes tamaños.'),
        (tema_id, '¿Qué función crea una matriz identidad?', 'np.eye()', 'np.identity()', 'Ambas son correctas', 'c', 'Tanto np.eye() como np.identity() crean matrices identidad.'),
        (tema_id, '¿Cómo se obtiene un subconjunto de un array?', 'Con slicing: array[inicio:fin]', 'Con la función subset()', 'Con el método .get()', 'a', 'El slicing permite obtener porciones del array.'),
        (tema_id, '¿Qué hace np.where()?', 'Busca la ubicación de un valor', 'Aplica condiciones para seleccionar valores', 'Ambas son correctas', 'c', 'np.where() puede buscar índices o aplicar lógica condicional.'),
        (tema_id, '¿Qué tipo de almacenamiento usa NumPy?', 'No contiguo con punteros', 'Contiguo en memoria', 'En disco', 'b', 'NumPy almacena datos de forma contigua para mayor eficiencia.'),
        (tema_id, '¿Qué hace np.concatenate()?', 'Une arrays a lo largo de un eje', 'Multiplica arrays', 'Divide un array', 'a', 'concatenate() une múltiples arrays.'),
        (tema_id, '¿Para qué sirve np.random.seed()?', 'Generar números verdaderamente aleatorios', 'Hacer que los números aleatorios sean reproducibles', 'Inicializar un array', 'b', 'seed() permite reproducir la misma secuencia de números aleatorios.'),
        (tema_id, '¿Qué devuelve array.T?', 'El tamaño del array', 'La transpuesta del array', 'El tipo de datos', 'b', '.T es un atajo para la transpuesta del array.'),
        
        # Preguntas prácticas: "¿Qué usarías para...?"
        (tema_id, '¿Qué función usarías para crear un array con valores del 0 al 99?', 'np.range(100)', 'np.arange(100)', 'np.array(100)', 'b', 'np.arange(100) genera [0, 1, 2, ..., 99].'),
        (tema_id, '¿Qué función usarías para calcular la suma de todos los elementos?', 'np.sum()', 'np.add()', 'np.total()', 'a', 'np.sum(array) suma todos los elementos.'),
        (tema_id, '¿Qué función usarías para encontrar el valor máximo de un array?', 'np.maximum()', 'np.max()', 'np.highest()', 'b', 'np.max() o array.max() devuelve el valor máximo.'),
        (tema_id, '¿Qué función usarías para calcular la desviación estándar?', 'np.std()', 'np.deviation()', 'np.stdev()', 'a', 'np.std() calcula la desviación estándar.'),
        (tema_id, '¿Qué función usarías para generar 5 números aleatorios entre 0 y 1?', 'np.random.rand(5)', 'np.random(5)', 'np.rand(5)', 'a', 'np.random.rand(5) genera 5 números aleatorios uniformes.'),
        (tema_id, '¿Qué función usarías para redondear decimales a enteros?', 'np.round()', 'np.int()', 'np.floor()', 'a', 'np.round() redondea al entero más cercano.'),
        (tema_id, '¿Qué función usarías para obtener los índices que ordenarían el array?', 'np.sort()', 'np.argsort()', 'np.sortidx()', 'b', 'np.argsort() devuelve los índices que ordenarían el array.'),
        (tema_id, '¿Qué función usarías para convertir un array 2D en 1D?', 'np.flat()', 'np.flatten() o np.ravel()', 'np.convert()', 'b', 'flatten() y ravel() convierten a 1D. flatten() devuelve copia, ravel() puede ser vista.'),
        (tema_id, '¿Qué función usarías para multiplicar matrices (producto matricial)?', 'np.multiply()', 'np.dot() o @', 'np.prod()', 'b', 'np.dot(A, B) o A @ B realizan multiplicación matricial.'),
        (tema_id, '¿Qué función usarías para contar cuántos elementos cumplen una condición?', 'np.count()', 'np.sum(condicion)', 'np.filter()', 'b', 'np.sum(array > 5) cuenta True como 1.'),
        (tema_id, '¿Qué función usarías para obtener valores únicos de un array?', 'np.unique()', 'np.distinct()', 'np.different()', 'a', 'np.unique() devuelve los valores únicos ordenados.'),
        (tema_id, '¿Qué función usarías para apilar arrays verticalmente?', 'np.vstack()', 'np.vertical()', 'np.stack_v()', 'a', 'np.vstack() apila arrays uno encima del otro.'),
        (tema_id, '¿Qué función usarías para apilar arrays horizontalmente?', 'np.hstack()', 'np.horizontal()', 'np.stack_h()', 'a', 'np.hstack() une arrays lado a lado.'),
        (tema_id, '¿Qué función usarías para calcular la raíz cuadrada de cada elemento?', 'np.sqrt()', 'np.root()', 'np.square_root()', 'a', 'np.sqrt(array) calcula la raíz cuadrada elemento a elemento.'),
        (tema_id, '¿Qué función usarías para elevar cada elemento al cuadrado?', 'np.square()', 'np.pow2()', 'np.cuadrado()', 'a', 'np.square() o array**2 eleva al cuadrado.'),
        (tema_id, '¿Qué función usarías para guardar un array en un archivo?', 'np.save()', 'np.write()', 'np.export()', 'a', 'np.save("archivo.npy", array) guarda en formato binario.'),
        (tema_id, '¿Qué función usarías para cargar un array desde un archivo .npy?', 'np.load()', 'np.read()', 'np.import()', 'a', 'np.load("archivo.npy") carga el array.'),
        (tema_id, '¿Qué función usarías para crear un array de 10 elementos todos con valor 7?', 'np.full(10, 7)', 'np.fill(10, 7)', 'np.repeat(7, 10)', 'a', 'np.full(10, 7) crea [7, 7, 7, 7, 7, 7, 7, 7, 7, 7].'),
        (tema_id, '¿Qué función usarías para obtener el índice del valor máximo?', 'np.argmax()', 'np.maxindex()', 'np.idxmax()', 'a', 'np.argmax() devuelve el índice del máximo.'),
        (tema_id, '¿Qué función usarías para dividir un array en partes iguales?', 'np.split()', 'np.divide()', 'np.partition()', 'a', 'np.split(array, n) divide en n partes.'),
        (tema_id, '¿Qué función usarías para reemplazar valores según una condición?', 'np.replace()', 'np.where(condicion, si_true, si_false)', 'np.switch()', 'b', 'np.where() permite reemplazar valores condicionalmente.'),
        (tema_id, '¿Qué función usarías para calcular el producto de todos los elementos?', 'np.prod()', 'np.multiply_all()', 'np.product()', 'a', 'np.prod() multiplica todos los elementos.'),
        (tema_id, '¿Qué función usarías para calcular la suma acumulada?', 'np.cumsum()', 'np.sumcum()', 'np.running_sum()', 'a', 'np.cumsum() devuelve [a, a+b, a+b+c, ...].'),
        (tema_id, '¿Qué función usarías para generar números aleatorios con distribución normal?', 'np.random.randn()', 'np.random.normal()', 'Ambas son correctas', 'c', 'randn() y normal() generan números con distribución gaussiana.'),
        (tema_id, '¿Qué función usarías para repetir un array varias veces?', 'np.tile()', 'np.repeat()', 'Ambas, pero funcionan diferente', 'c', 'tile() repite el array completo, repeat() repite cada elemento.'),
    ]


# =============================================================================
# PREGUNTAS DE PANDAS
# =============================================================================

def get_preguntas_pandas(tema_id):
    """
    Devuelve todas las preguntas del tema Pandas.
    
    Organización de las preguntas:
    -----------------------------
    - Primero las conceptuales (qué hace, cómo se llama, etc.)
    - Después las prácticas (¿qué usarías para...?)
    
    Consejos para crear buenas preguntas:
    ------------------------------------
    1. Las opciones incorrectas deben ser plausibles
       Mal:  'pd.read_csv()', 'asdfgh()', 'xyz()'
       Bien: 'pd.read_csv()', 'pd.load_csv()', 'pd.open_csv()'
    
    2. La explicación debe ser educativa, no solo "es la correcta"
       Mal:  'La respuesta correcta es b'
       Bien: 'pd.read_csv() lee archivos CSV y los convierte en DataFrame'
    
    3. Incluye casos donde "ambas son correctas" si aplica
       Esto enseña que a veces hay múltiples formas válidas
    
    Args:
        tema_id (int): ID del tema Pandas en la base de datos
    
    Returns:
        list: Lista de tuplas con las preguntas
    """
    return [
        # Preguntas conceptuales básicas
        (tema_id, '¿Cuál es el alias estándar para importar Pandas?', 'import pandas as pan', 'import pandas as pd', 'import pandas as pnd', 'b', 'Por convención universal, Pandas se importa como pd.'),
        (tema_id, '¿Cuáles son las dos estructuras principales de Pandas?', 'Array y Matrix', 'Series y DataFrame', 'List y Dict', 'b', 'Series (1D) y DataFrame (2D) son las estructuras fundamentales.'),
        (tema_id, '¿Qué método muestra las primeras filas de un DataFrame?', '.first()', '.head()', '.top()', 'b', '.head() muestra las primeras n filas (por defecto 5).'),
        (tema_id, '¿Cómo se selecciona una columna de un DataFrame?', 'df.columna o df["columna"]', 'df.get("columna")', 'df.select("columna")', 'a', 'Se puede usar notación de punto o corchetes.'),
        (tema_id, '¿Qué método se usa para leer un archivo CSV?', 'pd.open_csv()', 'pd.read_csv()', 'pd.load_csv()', 'b', 'pd.read_csv() lee archivos CSV y los convierte en DataFrame.'),
        (tema_id, '¿Qué hace el método .dropna()?', 'Elimina columnas', 'Elimina filas con valores nulos', 'Elimina duplicados', 'b', '.dropna() elimina filas (o columnas) con valores faltantes.'),
        (tema_id, '¿Qué hace el método .fillna(valor)?', 'Filtra valores', 'Rellena valores nulos con el valor especificado', 'Busca valores', 'b', '.fillna() reemplaza NaN con el valor indicado.'),
        (tema_id, '¿Qué método agrupa datos por una columna?', '.group()', '.groupby()', '.aggregate()', 'b', '.groupby() agrupa datos para aplicar funciones de agregación.'),
        (tema_id, '¿Qué hace df.loc[]?', 'Selección por posición numérica', 'Selección por etiquetas', 'Localiza valores nulos', 'b', '.loc[] selecciona por etiquetas de índice y columnas.'),
        (tema_id, '¿Qué hace df.iloc[]?', 'Selección por etiquetas', 'Selección por posición numérica', 'Selección de índices', 'b', '.iloc[] selecciona por posición numérica (enteros).'),
        (tema_id, '¿Qué método combina DataFrames como un JOIN de SQL?', 'pd.join()', 'pd.merge()', 'pd.combine()', 'b', 'pd.merge() combina DataFrames basándose en columnas comunes.'),
        (tema_id, '¿Qué método apila DataFrames verticalmente?', 'pd.stack()', 'pd.concat()', 'pd.append()', 'b', 'pd.concat() puede concatenar DataFrames vertical u horizontalmente.'),
        (tema_id, '¿Qué método proporciona estadísticas descriptivas?', '.stats()', '.describe()', '.summary()', 'b', '.describe() genera estadísticas como media, std, min, max.'),
        (tema_id, '¿Qué es un valor NaN en Pandas?', 'Un número negativo', 'Un valor faltante o nulo', 'Un valor infinito', 'b', 'NaN (Not a Number) representa valores faltantes.'),
        (tema_id, '¿Qué hace el método .info()?', 'Muestra información del sistema', 'Muestra información sobre el DataFrame (tipos, nulos)', 'Muestra los primeros datos', 'b', '.info() muestra tipos de datos, memoria y valores no nulos.'),
        (tema_id, '¿Qué hace pivot_table()?', 'Rota el DataFrame 90 grados', 'Crea tablas dinámicas con agregación', 'Ordena las columnas', 'b', 'pivot_table() reorganiza datos y aplica funciones de agregación.'),
        (tema_id, '¿Qué hace el método .melt()?', 'Derrite el DataFrame', 'Convierte formato ancho a largo', 'Elimina columnas', 'b', '.melt() transforma columnas en filas (ancho a largo).'),
        (tema_id, '¿Qué hace df.sort_values()?', 'Ordena por índice', 'Ordena por valores de una columna', 'Ordena alfabéticamente las columnas', 'b', '.sort_values() ordena el DataFrame por una o más columnas.'),
        (tema_id, '¿Qué parámetro hace cambios directos en el DataFrame?', 'direct=True', 'inplace=True', 'modify=True', 'b', 'inplace=True modifica el DataFrame original.'),
        (tema_id, '¿Qué método cuenta valores únicos de una columna?', '.unique_count()', '.value_counts()', '.count_values()', 'b', '.value_counts() cuenta la frecuencia de cada valor único.'),
        
        # Preguntas prácticas: "¿Qué usarías para...?"
        (tema_id, '¿Qué función usarías para leer un archivo Excel?', 'pd.read_excel()', 'pd.load_excel()', 'pd.open_excel()', 'a', 'pd.read_excel() lee archivos .xlsx y .xls.'),
        (tema_id, '¿Qué método usarías para guardar un DataFrame a CSV?', 'df.save_csv()', 'df.to_csv()', 'df.write_csv()', 'b', 'df.to_csv("archivo.csv") guarda el DataFrame.'),
        (tema_id, '¿Qué método usarías para eliminar filas duplicadas?', 'df.remove_duplicates()', 'df.drop_duplicates()', 'df.delete_duplicates()', 'b', 'drop_duplicates() elimina filas repetidas.'),
        (tema_id, '¿Qué método usarías para renombrar columnas?', 'df.rename(columns={"old": "new"})', 'df.change_columns()', 'df.columns_rename()', 'a', 'rename(columns=dict) cambia nombres de columnas.'),
        (tema_id, '¿Qué método usarías para filtrar filas donde edad > 30?', 'df.filter(edad > 30)', 'df[df["edad"] > 30]', 'df.select(edad > 30)', 'b', 'df[condicion] filtra filas que cumplen la condición.'),
        (tema_id, '¿Qué método usarías para contar valores nulos por columna?', 'df.count_null()', 'df.isnull().sum()', 'df.null_count()', 'b', 'isnull().sum() cuenta NaN en cada columna.'),
        (tema_id, '¿Qué método usarías para obtener las últimas 3 filas?', 'df.last(3)', 'df.tail(3)', 'df.bottom(3)', 'b', 'df.tail(n) devuelve las últimas n filas.'),
        (tema_id, '¿Qué método usarías para cambiar el índice del DataFrame?', 'df.change_index()', 'df.set_index()', 'df.index_set()', 'b', 'set_index("columna") usa esa columna como índice.'),
        (tema_id, '¿Qué método usarías para resetear el índice a números?', 'df.reset_index()', 'df.index_reset()', 'df.default_index()', 'a', 'reset_index() vuelve a índice numérico 0, 1, 2...'),
        (tema_id, '¿Qué método usarías para ordenar por múltiples columnas?', 'df.sort(["a", "b"])', 'df.sort_values(by=["a", "b"])', 'df.order_by(["a", "b"])', 'b', 'sort_values(by=lista) ordena por varias columnas.'),
        (tema_id, '¿Qué método usarías para aplicar una función a cada elemento?', 'df.apply()', 'df.map()', 'Ambas, pero con diferencias', 'c', 'apply() para columnas/filas, map() para Series elemento a elemento.'),
        (tema_id, '¿Qué método usarías para calcular la correlación entre columnas?', 'df.correlation()', 'df.corr()', 'df.correlate()', 'b', 'df.corr() calcula la matriz de correlación.'),
        (tema_id, '¿Qué método usarías para agrupar y calcular la media por grupo?', 'df.groupby("col").mean()', 'df.group("col").average()', 'df.aggregate("col").mean()', 'a', 'groupby().mean() calcula la media de cada grupo.'),
        (tema_id, '¿Qué método usarías para combinar dos DataFrames por índice?', 'df1.merge(df2)', 'df1.join(df2)', 'Ambas pueden funcionar', 'c', 'join() usa el índice, merge() usa columnas (por defecto).'),
        (tema_id, '¿Qué método usarías para seleccionar filas 10 a 20?', 'df[10:20]', 'df.iloc[10:20]', 'Ambas funcionan igual', 'c', 'Tanto df[10:20] como iloc[10:20] seleccionan por posición.'),
        (tema_id, '¿Qué método usarías para obtener solo las columnas numéricas?', 'df.numeric_columns()', 'df.select_dtypes(include="number")', 'df.numbers()', 'b', 'select_dtypes() filtra columnas por tipo de dato.'),
        (tema_id, '¿Qué método usarías para crear una columna nueva calculada?', 'df.new_column("c", valor)', 'df["c"] = valor', 'df.add_column("c", valor)', 'b', 'df["nueva_col"] = expresion crea la columna.'),
        (tema_id, '¿Qué método usarías para eliminar una columna?', 'df.drop("col", axis=1)', 'df.remove("col")', 'df.delete_column("col")', 'a', 'drop(columna, axis=1) elimina la columna.'),
        (tema_id, '¿Qué método usarías para ver los tipos de datos de cada columna?', 'df.types()', 'df.dtypes', 'df.column_types()', 'b', 'df.dtypes muestra el tipo de cada columna.'),
        (tema_id, '¿Qué método usarías para rellenar nulos con la media de la columna?', 'df.fillna(df.mean())', 'df.replace_null(mean)', 'df.fill_mean()', 'a', 'fillna(df.mean()) rellena NaN con la media.'),
        (tema_id, '¿Qué método usarías para filtrar filas donde el nombre contiene "Ana"?', 'df[df["nombre"].contains("Ana")]', 'df[df["nombre"].str.contains("Ana")]', 'df.filter(nombre="Ana")', 'b', 'str.contains() busca patrones en strings.'),
        (tema_id, '¿Qué método usarías para convertir una columna a tipo fecha?', 'df["col"].to_date()', 'pd.to_datetime(df["col"])', 'df["col"].as_date()', 'b', 'pd.to_datetime() convierte strings a fechas.'),
        (tema_id, '¿Qué método usarías para extraer el año de una columna fecha?', 'df["fecha"].year', 'df["fecha"].dt.year', 'df["fecha"].get_year()', 'b', '.dt.year extrae el año de columnas datetime.'),
        (tema_id, '¿Qué método usarías para hacer un left join entre DataFrames?', 'pd.merge(df1, df2, how="left")', 'df1.left_join(df2)', 'pd.join_left(df1, df2)', 'a', 'merge() con how="left" hace left join.'),
        (tema_id, '¿Qué método usarías para obtener una muestra aleatoria de 100 filas?', 'df.random(100)', 'df.sample(100)', 'df.take_random(100)', 'b', 'df.sample(n) devuelve n filas aleatorias.'),
        (tema_id, '¿Qué método usarías para transponer un DataFrame?', 'df.transpose()', 'df.T', 'Ambas son correctas', 'c', 'df.T y df.transpose() intercambian filas y columnas.'),
        (tema_id, '¿Qué método usarías para ver cuánta memoria usa el DataFrame?', 'df.memory()', 'df.info(memory_usage="deep")', 'df.size_mb()', 'b', 'info() con memory_usage muestra uso de memoria detallado.'),
        (tema_id, '¿Qué método usarías para obtener el número de filas y columnas?', 'df.size()', 'df.shape', 'df.dimensions()', 'b', 'df.shape devuelve (filas, columnas).'),
        (tema_id, '¿Qué método usarías para convertir columnas en filas (unpivot)?', 'df.unpivot()', 'df.melt()', 'df.stack_columns()', 'b', 'melt() transforma de formato ancho a largo.'),
        (tema_id, '¿Qué método usarías para crear dummies de una columna categórica?', 'pd.get_dummies()', 'df.create_dummies()', 'df.one_hot_encode()', 'a', 'pd.get_dummies() crea variables dummy (one-hot encoding).'),
    ]


# =============================================================================
# FUNCIÓN PRINCIPAL DE CARGA
# =============================================================================

def cargar_todas_las_preguntas():
    """
    Carga todos los temas y preguntas en la base de datos SQLite.
    
    ¿Cuándo se ejecuta?
    -------------------
    Solo cuando las tablas están vacías (primera ejecución o después
    de eliminar quiz.db). Esto evita duplicar las preguntas.
    
    ¿Qué hace paso a paso?
    ----------------------
    1. Verifica si ya hay preguntas (si hay, no hace nada)
    2. Inserta los temas (NumPy, Pandas) en la tabla 'temas'
    3. Obtiene los IDs generados para cada tema
    4. Genera todas las preguntas con esos IDs
    5. Inserta todas las preguntas en la tabla 'preguntas'
    
    Returns:
        bool: True si se cargaron datos, False si ya existían
    
    Nota sobre executemany():
    ------------------------
    En lugar de hacer un INSERT por cada pregunta (lento),
    executemany() inserta todas de una vez (mucho más rápido).
    
    Ejemplo de INSERT individual (LENTO - NO USAR):
        for pregunta in preguntas:
            cursor.execute('INSERT INTO...', pregunta)
    
    Con executemany (RÁPIDO - USAMOS ESTO):
        cursor.executemany('INSERT INTO...', preguntas)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # -------------------------------------------------------------------------
    # PASO 1: Verificar si ya hay preguntas
    # -------------------------------------------------------------------------
    cursor.execute('SELECT COUNT(*) FROM preguntas')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False  # Ya hay datos, no hacemos nada
    
    # -------------------------------------------------------------------------
    # PASO 2: Insertar los temas
    # -------------------------------------------------------------------------
    # INSERT OR IGNORE: Si el tema ya existe (por nombre UNIQUE), lo ignora
    cursor.executemany(
        'INSERT OR IGNORE INTO temas (nombre, descripcion, icono) VALUES (?, ?, ?)', 
        TEMAS
    )
    conn.commit()  # Guardamos para que se generen los IDs
    
    # -------------------------------------------------------------------------
    # PASO 3: Obtener los IDs de los temas insertados
    # -------------------------------------------------------------------------
    # Necesitamos los IDs para asociar las preguntas a cada tema
    cursor.execute('SELECT id FROM temas WHERE nombre = "NumPy"')
    numpy_id = cursor.fetchone()[0]
    
    cursor.execute('SELECT id FROM temas WHERE nombre = "Pandas"')
    pandas_id = cursor.fetchone()[0]
    
    # -------------------------------------------------------------------------
    # PASO 4: Recopilar todas las preguntas
    # -------------------------------------------------------------------------
    # Concatenamos las listas de preguntas de cada tema
    todas_las_preguntas = (
        get_preguntas_numpy(numpy_id) + 
        get_preguntas_pandas(pandas_id)
    )
    
    # -------------------------------------------------------------------------
    # PASO 5: Insertar todas las preguntas de una vez
    # -------------------------------------------------------------------------
    cursor.executemany('''
        INSERT INTO preguntas (tema_id, pregunta, opcion_a, opcion_b, opcion_c, respuesta_correcta, explicacion)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', todas_las_preguntas)
    
    conn.commit()  # Guardar todos los cambios
    conn.close()   # Liberar la conexión
    
    return True  # Indicamos que sí se cargaron datos


def mostrar_estadisticas():
    """
    Muestra en consola un resumen de las preguntas cargadas.
    
    Útil para verificar que todo se cargó correctamente.
    
    Salida ejemplo:
        📊 Estadísticas de preguntas:
           Total: 95 preguntas
           🔢 NumPy: 45 preguntas
           🐼 Pandas: 50 preguntas
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Contar total de preguntas
    cursor.execute('SELECT COUNT(*) FROM preguntas')
    total = cursor.fetchone()[0]
    
    # Contar preguntas por tema (con icono)
    cursor.execute('''
        SELECT t.nombre, t.icono, COUNT(p.id) as total
        FROM temas t
        LEFT JOIN preguntas p ON t.id = p.tema_id
        GROUP BY t.id
    ''')
    
    por_tema = cursor.fetchall()
    conn.close()
    
    # Mostrar resultados formateados
    print(f"\n📊 Estadísticas de preguntas:")
    print(f"   Total: {total} preguntas")
    for tema in por_tema:
        print(f"   {tema['icono']} {tema['nombre']}: {tema['total']} preguntas")
    print()


# =============================================================================
# EJECUCIÓN DIRECTA DEL MÓDULO (para pruebas)
# =============================================================================

# Este bloque solo se ejecuta si ejecutas: python preguntas.py
# No se ejecuta cuando otro archivo hace: from preguntas import ...
if __name__ == '__main__':
    # Importamos aquí para evitar importaciones circulares
    from database import init_db, tablas_vacias
    
    print("🔧 Inicializando base de datos...")
    init_db()
    
    if tablas_vacias():
        print("📝 Cargando preguntas...")
        cargar_todas_las_preguntas()
        print("✅ Preguntas cargadas correctamente!")
    else:
        print("ℹ️  Las tablas ya tienen datos.")
    
    mostrar_estadisticas()
