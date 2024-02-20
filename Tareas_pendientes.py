import psycopg2

# Función para conectar a la base de datos
def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname="980proyectos",
            user="postgres",
            password="x8jx5yt5",
            host="localhost",
            port="5432"  # El puerto por defecto de PostgreSQL es 5432
        )
        print("Conexión establecida correctamente.")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)

# Función para registrar un nuevo usuario
def registrar_usuario(conn, nombre_usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios2 (nombre_usuario) VALUES (%s)", (nombre_usuario,))
        conn.commit()
        print("Usuario registrado exitosamente.")
    except psycopg2.Error as e:
        print("Error al registrar usuario:", e)

# Función para ingresar con un nombre de usuario existente
def ingresar_usuario(nombre_usuario):
    print(f"Bienvenido, {nombre_usuario}!")

# Función para agregar una nueva tarea
def agregar_tarea(conn, id_usuario, tarea, fecha_vencimiento):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tareas (id_usuario, tarea, fecha_vencimiento) VALUES (%s, %s, %s)", (id_usuario, tarea, fecha_vencimiento))
        conn.commit()
        print("Tarea agregada exitosamente.")
    except psycopg2.Error as e:
        print("Error al agregar tarea:", e)

# Función para marcar una tarea como completada
def completar_tarea(conn, nombre_usuario, texto_tarea):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET completada = 1 WHERE nombre_usuario = %s AND tarea = %s", (nombre_usuario, texto_tarea,))
        conn.commit()
        print("Tarea marcada como completada.")
    except psycopg2.Error as e:
        print("Error al marcar tarea como completada:", e)
# Función para ver el historial de tareas de un usuario
def ver_historial(conn, nombre_usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, tarea, fecha_vencimiento, completada FROM tareas WHERE id_usuario = (SELECT id FROM usuarios2 WHERE nombre_usuario = %s)", (nombre_usuario,))
        tareas = cursor.fetchall()
        for tarea in tareas:
            tarea_id, descripcion, fecha_vencimiento, completada = tarea
            completada_str = "Completada" if completada else "Pendiente"
            print(f"Tarea {tarea_id}: {descripcion} - Fecha de vencimiento: {fecha_vencimiento} - Estado: {completada_str}")
    except psycopg2.Error as e:
        print("Error al obtener historial de tareas:", e)


# Función para borrar datos del usuario
def borrar_datos_usuario(conn, nombre_usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id_usuario = (SELECT id FROM usuarios2 WHERE nombre_usuario = %s)", (nombre_usuario,))
        cursor.execute("DELETE FROM usuarios2 WHERE nombre_usuario = %s", (nombre_usuario,))
        conn.commit()
        print("Datos del usuario borrados exitosamente.")
    except psycopg2.Error as e:
        print("Error al borrar datos del usuario:", e)

def obtener_id_usuario_por_nombre(conn, nombre_usuario):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios2 WHERE nombre_usuario = %s", (nombre_usuario,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]  # Devuelve el primer elemento de la tupla (el ID del usuario)
        else:
            print("No se encontró el usuario con el nombre especificado.")
            return None
    except psycopg2.Error as e:
        print("Error al obtener ID de usuario por nombre:", e)
        return None

# Menú principal
while True:
    print("Bienvenido al sistema de gestión de tareas pendientes.")
    print("1. Ingresar con nombre de usuario")
    print("2. Registrar nuevo usuario")
    opcion = input("Seleccione una opción: ")

    conn = conectar_bd()

    if opcion == "1":
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        ingresar_usuario(nombre_usuario)

        # Opciones adicionales para el usuario una vez ingresado
        print("1. Agregar nueva tarea")
        print("2. Marcar tarea como completada por texto")
        print("3. Ver historial de tareas")
        opcion_ingreso = input("Seleccione una opción: ")

        if opcion_ingreso == "1":
            tarea = input("Ingrese la nueva tarea: ")
            fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
            agregar_tarea(conn, nombre_usuario, tarea, fecha_vencimiento)
        elif opcion_ingreso == "2":
            texto_tarea = input("Ingrese el texto de la tarea a marcar como completada: ")
            completar_tarea(conn, nombre_usuario, texto_tarea)
        elif opcion_ingreso == "3":
            ver_historial(conn, nombre_usuario)
        else:
            print("Opción no válida.")

    elif opcion == "2":
        nombre_usuario = input("Ingrese su nombre de usuario: ")
        registrar_usuario(conn, nombre_usuario)

    # Cierre de la conexión a la base de datos
        conn.close()
