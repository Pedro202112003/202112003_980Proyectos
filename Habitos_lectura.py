import psycopg2
import random
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
def registrar_usuario(nombre_usuario):
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        # Verificar si el nombre de usuario ya existe
        cursor.execute(
            "SELECT COUNT(*) FROM HabitosLectura WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        cantidad_usuarios = cursor.fetchone()[0]
        if cantidad_usuarios > 0:
            print("El nombre de usuario ya está registrado. Por favor, elija otro.")
            return

        # Registrar el nuevo usuario si no existe
        cursor.execute(
            "INSERT INTO HabitosLectura (nombre_usuario) VALUES (%s)",
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
            FROM HabitosLectura
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
        print(f"Error al ingreasar: {e}")
        return None

# Función para ingresar libro leído
def ingresar_libro_leido(nombre_usuario):
    titulo_libro = input("Ingrese el título del libro leído: ")
    autor_libro = input("Ingrese el autor del libro leído: ")
    fecha = datetime.now().date()
    meta_lectura = int(input("Ingrese uan meta de dias para terminar el libro: "))
    try:
        cursor.execute(
            """
            INSERT INTO HabitosLectura(nombre_usuario, titulo_libro, autor_libro, fecha, meta_lectura)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre_usuario, titulo_libro, autor_libro, fecha, meta_lectura),
        )
        connection.commit()
        print("¡Libro leído registrado exitosamente!")
    except Exception as e:
        print(f"Error al registrar libro leído: {e}")

# Función para establecer meta de lectura

# Función para recibir recomendaciones
def obtener_recomendaciones(cursor):
    try:
        cursor.execute(
            """
            SELECT titulo, autor
            FROM RecomendacionesLibros
            ORDER BY RANDOM()
            LIMIT 5
            """
        )
        recomendaciones = cursor.fetchall()
        if recomendaciones:
            print("¡Aquí van algunas recomendaciones de libros para ti!")
            for titulo, autor in recomendaciones:
                print(f"Libro: {titulo} (Autor: {autor})")
        else:
            print("Lo sentimos, no hay recomendaciones disponibles en este momento.")
    except Exception as e:
        print(f"Error al recibir recomendaciones: {e}")
# Función para ver historial de lectura
def ver_historial_lectura(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT titulo_libro, autor_libro, fecha, meta_lectura
            FROM HabitosLectura
            WHERE nombre_usuario = %s
            ORDER BY fecha DESC
            """,
            (nombre_usuario,),
        )
        historial = cursor.fetchall()
        if historial:
            print("Historial de lectura:")
            for titulo_libro, autor_libro, fecha, meta_lectura in historial:
                print(f"Fecha: {fecha}, Libro: {titulo_libro} (Autor: {autor_libro}), Meta: {meta_lectura} dias")
        else:
            print("No hay registros de lectura para este usuario.")
    except Exception as e:
        print(f"Error al obtener historial de lectura: {e}")

# Función para borrar todos los datos del usuario
def borrar_usuario(nombre_usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                "DELETE FROM HabitosLectura WHERE nombre_usuario = %s",
                (nombre_usuario,),
            )
            connection.commit()
            print("Datos del usuario borrado exitosamente.\n")
        
        except Exception as e:
            print(f"Error al borrar las datos del usuario: {e}")
    else:
        print("Los datos no seran borrados")

# Menú principal
def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de seguimiento de hábitos de lectura")
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                nombre_usuario = ingresar_usuario()
            elif opcion == "2":
                nombre_usuario = registrar_usuario(nombre_usuario)
            elif opcion == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")
        else:
            print("1. Ingresar libro leído")
            print("2. Recibir recomendaciones")
            print("3. Ver historial de lectura")
            print("4. Borrar todos los datos del usuario")
            print("5. Regresar")

            opcion = input("Ingrese una opción: ")
            if opcion == "1":
                ingresar_libro_leido(nombre_usuario)
            elif opcion == "2":
                obtener_recomendaciones(cursor)
            elif opcion == "3":
                ver_historial_lectura(nombre_usuario)
            elif opcion == "4":
                borrar_usuario(nombre_usuario)
                nombre_usuario = None
            elif opcion == "5":
                print("¡Hasta luego!\n")
                nombre_usuario = None
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
cursor.close()
connection.close()
