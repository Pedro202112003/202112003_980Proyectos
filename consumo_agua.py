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

# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    try:
        cursor.execute(
            """
            INSERT INTO consumoAgua(nombre_usuario)
            VALUES (%s)
            """,
            (nombre_usuario,),
        )
        connection.commit()
        print("¡Usuario registrado exitosamente!")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")

# Función para iniciar sesión
# Función para iniciar sesión
def ingresar_usuario():
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        cursor.execute("SELECT nombre_usuario FROM consumoAgua WHERE nombre_usuario = %s",(nombre_usuario,),
        )
        usuario = cursor.fetchone()
        if usuario:
            print("¡Inicio de sesión exitoso!")
            print("Recuerda mantener tu cuerpo hidratado. ¡Bebe agua regularmente!")
            return nombre_usuario
        else:
            print("Nombre de usuario incorrecto.")
            return None
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return None


# Función para ingresar consumo de agua
def ingresar_consumo_agua(nombre_usuario):
    fecha = datetime.now().date()
    cantidad = float(input("Ingrese la cantidad de agua consumida en litros: "))
    try:
        cursor.execute(
            """
            INSERT INTO consumoAgua(nombre_usuario, fecha, cantidad)
            VALUES (%s, %s, %s)
            """,
            (nombre_usuario, fecha, cantidad),
        )
        connection.commit()
        print("¡Consumo de agua registrado exitosamente!")
    except Exception as e:
        print(f"Error al registrar el consumo de agua: {e}")

# Función para ver historial de consumo de agua
def ver_historial(nombre_usuario):
    try:
        cursor.execute("SELECT fecha, cantidad FROM consumoAgua WHERE nombre_usuario = %s ORDER BY fecha DESC",(nombre_usuario,),)
        historial = cursor.fetchall()
        if historial:
            print("Historial de consumo de agua:")
            for fecha, cantidad in historial:
                print(f"Fecha: {fecha}, Cantidad: {cantidad} litros")
        else:
            print("No hay registros de consumo de agua para este usuario.")
    except Exception as e:
        print(f"Error al obtener historial: {e}")

# Función para ver estadísticas de consumo de agua
def ver_estadisticas(nombre_usuario):
    try:
        cursor.execute("SELECT AVG(cantidad) AS ingesta_promedio FROM consumoAgua WHERE nombre_usuario = %s",(nombre_usuario,),)
        estadisticas = cursor.fetchone()
        if estadisticas[0]:
            ingesta_promedio = estadisticas[0]
            print(f"Ingesta promedio de agua: {ingesta_promedio} litros por día")
        else:
            print("No hay suficientes registros para calcular estadísticas.")
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")

# Función para borrar todos los datos del usuario
def borrar_datos_usuario(nombre_usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                """
                DELETE FROM consumoAgua
                WHERE nombre_usuario = %s
                """,
                (nombre_usuario,),
            )
            connection.commit()
            print("¡Todos los datos del usuario han sido borrados exitosamente!")
        except Exception as e:
            print(f"Error al borrar los datos del usuario: {e}")
    else:
        print("Operación cancelada.")

# Menú principal
def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de seguimiento de consumo diario de agua")
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                nombre_usuario = ingresar_usuario()
                cursor.execute("SELECT COUNT(*) FROM tareas WHERE usuario = %s", (nombre_usuario,))
                count = cursor.fetchone()[0]
                if count == 0:
                    print("El usuario ingresado no está registrado. Por favor, inténtelo de nuevo.")
                    nombre_usuario = None
                    continue
            elif opcion == "2":
                nombre_usuario = registrar_usuario()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")
        else:
            print("1. Ingresar consumo de agua")
            print("2. Ver historial de consumo de agua")
            print("3. Ver estadísticas de consumo de agua")
            print("4. Borrar todos los datos del usuario")
            print("5. Regresar")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                ingresar_consumo_agua(nombre_usuario)
            elif opcion == "2":
                ver_historial(nombre_usuario)
            elif opcion == "3":
                ver_estadisticas(nombre_usuario)
            elif opcion == "4":
                borrar_datos_usuario(nombre_usuario)
            elif opcion == "5":
                nombre_usuario = None
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
cursor.close()
connection.close()
