import psycopg2
from datetime import datetime

# Conexión a la base de datos
connection = psycopg2.connect(
    dbname="980proyectos",
    user="postgres",
    password="x8jx5yt5",
    host="localhost"
)
cursor = connection.cursor()
def ingresar_usuario():
    usuario = input("Ingrese su nombre de usuario: ")
    try:
        cursor.execute("SELECT usuario FROM tareas WHERE usuario = %s",(usuario,),)
        usuario = cursor.fetchone()
        if usuario:
            print("¡Inicio de sesión exitoso!")
            return usuario
        else:
            print("Nombre de usuario incorrecto.")
            return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None

def registrar_usuario(usuario):
    usuario = input("Ingrese su nombre de usuario: ")
    try:
        # Verificar si el nombre de usuario ya existe
        cursor.execute(
            "SELECT COUNT(*) FROM tareas WHERE usuario = %s",
            (usuario,),
        )
        cantidad_usuarios = cursor.fetchone()[0]
        if cantidad_usuarios > 0:
            print("El nombre de usuario ya está registrado. Por favor, elija otro.")
            return

        # Registrar el nuevo usuario si no existe
        cursor.execute(
            "INSERT INTO tareas (usuario) VALUES (%s)",
            (usuario,),
        )
        connection.commit()
        print("Usuario registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")

def agregar_tarea(usuario):
    tarea = input("Ingrese la descripción de la tarea: ")
    fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
    fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
    # Insertar tarea en la base de datos
    with connection.cursor() as cursor:
        cursor.execute("""INSERT INTO tareas (usuario, tarea, fecha_vencimiento, completada) 
                       VALUES (%s, %s, %s, %s)""", (usuario, tarea, fecha_vencimiento, False))
        connection.commit()

def completada(usuario):
    tarea = input("Ingrese la descripción de la tarea que desea marcar como completada: ")
    # Marcar tarea como completada en la base de datos
    with connection.cursor() as cursor:
        cursor.execute("UPDATE tareas SET completada = TRUE WHERE usuario = %s AND tarea = %s", (usuario, tarea))
        connection.commit()
    print("La tarea ha sido marcada como completada.")


def historial(usuario):
    # Obtener historial de tareas del usuario
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tareas WHERE usuario = %s", (usuario,))
        tareas = cursor.fetchall()
        for tarea in tareas:
            estado = "Completada" if tarea[4] else "Pendiente"
            print(f"ID: {tarea[0]}, Descripción: {tarea[2]}, Fecha de vencimiento: {tarea[3]}, Estado: {estado}")


def borrar_usuario(usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                "DELETE FROM tareas WHERE usuario = %s",
                (usuario,),
            )
            connection.commit()
            print("Datos del usuario borradas exitosamente.\n")
        except Exception as e:
            print(f"Error al borrar las datos del usuario: {e}")

def main():
    usuario = None
    while True:
        if usuario is None:
            print("Programa de gestion de tareas pendientes")
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                usuario = ingresar_usuario()
            elif opcion == "2":
                usuario = registrar_usuario(usuario)
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")
        else:
            print("1. Agregar nueva tarea")
            print("2. Marcar tarea como completada")
            print("3. Ver historial de tareas")
            print("4. Borrar datos del usuario")
            print("5. Regresar")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                agregar_tarea(usuario)
            elif opcion == "2":
                completada(usuario)
            elif opcion == "3":
                historial(usuario)
            elif opcion == "4":
                borrar_usuario(usuario)
                usuario=None
            elif opcion == "5":
                print("¡Hasta luego!\n")
                usuario = None
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")

if __name__ == "__main__":
    main()