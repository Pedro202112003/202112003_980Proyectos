import psycopg2
from datetime import datetime

# Conexión con la base de datos
try:
    connection = psycopg2.connect(
        database="980proyectos",
        user="postgres",
        password="x8jx5yt5",
        host="localhost",
    )
    cursor = connection.cursor()
except Exception as e: 
    print(f"Error de conexión con la base de datos {e}")
    exit()

def registrar_usuario(nombre_usuario):
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        # Verificar si el nombre de usuario ya existe
        cursor.execute(
            "SELECT COUNT(*) FROM ProyectosPersonales WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        cantidad_usuarios = cursor.fetchone()[0]
        if cantidad_usuarios > 0:
            print("El nombre de usuario ya está registrado. Por favor, elija otro.")
            return

        # Registrar el nuevo usuario si no existe
        cursor.execute(
            "INSERT INTO ProyectosPersonales (nombre_usuario) VALUES (%s)",
            (nombre_usuario,),
        )
        connection.commit()
        print("Usuario registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")

# Función para iniciar sesión
def ingresar_usuario():
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        cursor.execute(
            """
            SELECT nombre_usuario
            FROM ProyectosPersonales
            WHERE nombre_usuario = %s
            """,
            (nombre_usuario,),
        )
        usuario = cursor.fetchone()
        if usuario:
            print("¡Inicio de sesión exitoso!")
            return nombre_usuario
        else:
            print("Nombre de usuario incorrecto.")
            return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None
    
# Función para registrar una nueva tarea en el proyecto personal
def registrar_tarea(nombre_usuario):
    tarea = input("Ingrese la descripción de la tarea: ")
    fecha_limite = input("Ingrese la fecha límite de la tarea (YYYY-MM-DD): ")
    try:
        cursor.execute(
            """
            INSERT INTO ProyectosPersonales(nombre_usuario, tarea, fecha_limite, completada)
            VALUES (%s, %s, %s, FALSE)
            """,
            (nombre_usuario, tarea, fecha_limite),
        )
        connection.commit()
        print("¡Tarea registrada exitosamente!")
    except Exception as e:
        print(f"Error al registrar tarea: {e}")

# Función para marcar una tarea como completada
def marcar_tarea_completada(nombre_usuario):
    tarea_id = int(input("Ingrese el ID de la tarea que desea marcar como completada: "))
    try:
        cursor.execute(
            """
            UPDATE ProyectosPersonales
            SET completada = TRUE
            WHERE id = %s AND nombre_usuario = %s
            """,
            (tarea_id, nombre_usuario),
        )
        connection.commit()
        print("¡Tarea marcada como completada exitosamente!")
    except Exception as e:
        print(f"Error al marcar tarea como completada: {e}")

# Función para ver el historial de tareas del proyecto personal
def ver_historial_tareas(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT id, tarea, fecha_limite, completada
            FROM ProyectosPersonales
            WHERE nombre_usuario = %s
            ORDER BY fecha_limite DESC
            """,
            (nombre_usuario,),
        )
        historial = cursor.fetchall()
        if historial:
            print("Historial de tareas:")
            for tarea in historial:
                tarea_id, descripcion, fecha_limite, completada = tarea
                completada_str = "Completada" if completada else "Pendiente"
                print(f"ID: {tarea_id}, Descripción: {descripcion}, Fecha límite: {fecha_limite}, Estado: {completada_str}")
        else:
            print("No hay tareas registradas para este usuario.")
    except Exception as e:
        print(f"Error al obtener historial de tareas: {e}")

# Función para borrar una tarea del proyecto personal
# Función para borrar todas las tareas de un usuario
def borrar_tarea(nombre_usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                "DELETE FROM ProyectosPersonales WHERE nombre_usuario = %s",
                (nombre_usuario,),
            )
            connection.commit()
            print("Tareas del usuario borradas exitosamente.")
        except Exception as e:
            print(f"Error al borrar las tareas del usuario: {e}")


def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de seguimiento de proyectos personales")
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                nombre_usuario = ingresar_usuario()
            elif opcion == "2":
                nombre_usuario = registrar_usuario(nombre_usuario)
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")
        else:
            print("1. Registrar nueva tarea")
            print("2. Marcar tarea como completada")
            print("3. Ver historial de tareas")
            print("4. Borrar Usuario")
            print("5. Regresar")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                registrar_tarea(nombre_usuario)
            elif opcion == "2":
                marcar_tarea_completada(nombre_usuario)
            elif opcion == "3":
                ver_historial_tareas(nombre_usuario)
            elif opcion == "4":
                borrar_tarea(nombre_usuario)
                nombre_usuario=None
            elif opcion == "5":
                print("¡Hasta luego!")
                nombre_usuario=None
            else:
                print("Opción no válida.")
                
if __name__ == "__main__":
    main()
# Cerrar conexión con la base de datos al salir del programa
cursor.close()
connection.close()
