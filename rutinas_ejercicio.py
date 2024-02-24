import psycopg2

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

# Función para registrar un nuevo usuario
def registrar_usuario(nombre_usuario):
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        # Verificar si el nombre de usuario ya existe
        cursor.execute(
            "SELECT COUNT(*) FROM rutinas WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        cantidad_usuarios = cursor.fetchone()[0]
        if cantidad_usuarios > 0:
            print("El nombre de usuario ya está registrado. Por favor, elija otro.")
            return

        # Registrar el nuevo usuario si no existe
        cursor.execute(
            "INSERT INTO rutinas (nombre_usuario) VALUES (%s)",
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
            "SELECT nombre_usuario FROM rutinas WHERE nombre_usuario = %s",(nombre_usuario,),)
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

# Función para ingresar datos de rutina y metas
def ingresar_rutina(nombre_usuario):
    fecha = input("Ingrese la fecha de la rutina (DD/MM/AAAA): ")
    ejercicio = input("Ingrese el ejercicio realizado: ")
    duracion = float(input("Ingrese la duración del ejercicio en minutos: "))
    meta = float(input("Ingrese la meta de tiempo diario para este ejercicio (en minutos): "))
    completada = False  # Inicialmente, la rutina no está completada

    try:
        cursor.execute(
            """
            INSERT INTO rutinas(nombre_usuario, fecha, ejercicio, duracion, meta, completada)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre_usuario, fecha, ejercicio, duracion, meta, completada),
        )
        connection.commit()
        print("¡Rutina ingresada exitosamente!")
    except Exception as e:
        print(f"Error al agregar la rutina: {e}")

# Función para visualizar estadísticas
def ver_estadisticas(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT AVG(duracion) AS duracion_promedio,
                   COUNT(*) AS total_rutinas,
                   SUM(CASE WHEN completada THEN 1 ELSE 0 END) AS rutinas_completadas,
                   COUNT(*) - SUM(CASE WHEN completada THEN 1 ELSE 0 END) AS rutinas_incompletas
            FROM rutinas
            WHERE nombre_usuario = %s
            """,
            (nombre_usuario,),
        )
        estadisticas = cursor.fetchone()
        if estadisticas:
            duracion_promedio = estadisticas[0]
            total_rutinas = estadisticas[1]
            rutinas_completadas = estadisticas[2]
            rutinas_incompletas = estadisticas[3]

            print("Estadísticas generales:")
            print(f"Duración promedio de ejercicio: {duracion_promedio} minutos")
            print(f"Total de rutinas registradas: {total_rutinas}")
            print(f"Rutinas completadas: {rutinas_completadas}")
            print(f"Rutinas incompletas: {rutinas_incompletas}")
        else:
            print("No hay datos de rutinas registradas para este usuario.")
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")

# Función para ver historial de rutinas y metas
def ver_historial(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT fecha, ejercicio, duracion, meta, completada
            FROM rutinas
            WHERE nombre_usuario = %s
            """,
            (nombre_usuario,),
        )
        historial = cursor.fetchall()
        if historial:
            print("Historial de rutinas y metas:")
            for fecha, ejercicio, duracion, meta, completada in historial:
                completada_texto = "Sí" if completada else "No"
                print(f"Fecha: {fecha}, Ejercicio: {ejercicio}, Duración: {duracion} minutos, Meta: {meta} minutos, Completada: {completada_texto}")
        else:
            print("No hay rutinas registradas para este usuario.")
    except Exception as e:
        print(f"Error al obtener historial: {e}")

# Función para marcar una rutina como completada
def completar_rutina(nombre_usuario):
    fecha = input("Ingrese la fecha de la rutina que desea marcar como completada (DD/MM/AAAA): ")
    try:
        cursor.execute(
            """
            UPDATE rutinas
            SET completada = TRUE
            WHERE nombre_usuario = %s AND fecha = %s
            """,
            (nombre_usuario, fecha),
        )
        connection.commit()
        print("¡Rutina marcada como completada exitosamente!")
    except Exception as e:
        print(f"Error al marcar la rutina como completada: {e}")

def borrar_usuario(nombre_usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                "DELETE FROM GastosAlimentos WHERE nombre_usuario = %s",
                (nombre_usuario,),
            )
            connection.commit()
            print("Datos del usuario borrado exitosamente.\n")
        
        except Exception as e:
            print(f"Error al borrar las datos del usuario: {e}")
    else:
        print("Los datos no seran borrados")


def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de seguimiento de rutinas diarias de ejercicios")
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
            print("1. Ingresar nueva rutina")
            print("2. Ver historial de rutinas y metas")
            print("3. Marcar rutina como completada")
            print("4. Ver estadísticas")
            print("5. borrar datos del usuario")
            print("6. regresar")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                ingresar_rutina(nombre_usuario)
            elif opcion == "2":
                ver_historial(nombre_usuario)
            elif opcion == "3":
                completar_rutina(nombre_usuario)
            elif opcion == "4":
                ver_estadisticas(nombre_usuario)
            elif opcion == "5":
                borrar_usuario(nombre_usuario)
                nombre_usuario = None
            elif opcion == "6":
                print("¡Hasta luego!\n")
                nombre_usuario=None
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
cursor.close()
connection.close()
