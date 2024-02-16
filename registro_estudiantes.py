import psycopg2

# Conexión a la base de datos
try:
    connection = psycopg2.connect(
        database="980proyectos",
        user="postgres",
        password="x8jx5yt5",
        host="localhost",
    )
    cursor = connection.cursor()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()

# Función para agregar un nuevo estudiante
def agregar_estudiante():
    nombre = input("Ingrese el nombre del estudiante: ")
    edad = int(input("Ingrese la edad del estudiante: "))
    genero = input("Ingrese el género del estudiante (M/F): ")
    direccion = input("Ingrese la dirección del estudiante: ")

    try:
        cursor.execute(
            """
            INSERT INTO estudiantes (nombre, edad, genero, direccion)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, edad, genero, direccion),
        )
        connection.commit()
        print("Estudiante agregado exitosamente")
    except Exception as e:
        print(f"Error al agregar estudiante: {e}")

# Función para editar la información de un estudiante
def editar_estudiante():
    nombre = input("Ingrese el nombre del estudiante a editar: ")
    nuevo_nombre = input("Ingrese el nuevo nombre del estudiante: ")
    edad = int(input("Ingrese la nueva edad del estudiante: "))
    genero = input("Ingrese el nuevo género del estudiante (M/F): ")
    direccion = input("Ingrese la nueva dirección del estudiante: ")

    try:
        cursor.execute(
            """
            UPDATE estudiantes
            SET nombre = %s, edad = %s, genero = %s, direccion = %s
            WHERE nombre = %s
            """,
            (nuevo_nombre, edad, genero, direccion, nombre),
        )
        connection.commit()
        print("Estudiante editado exitosamente")
    except Exception as e:
        print(f"Error al editar estudiante: {e}")

# Función para eliminar un estudiante
def eliminar_estudiante():
    nombre = input("Ingrese el nombre del estudiante a eliminar: ")

    try:
        cursor.execute("""DELETE FROM estudiantes WHERE nombre = %s""", (nombre,))
        connection.commit()
        print("Estudiante eliminado exitosamente")
    except Exception as e:
        print(f"Error al eliminar estudiante: {e}")

# Menú principal
while True:
    print("\n**Programa de registro de estudiantes**")
    print("1. Agregar nuevo estudiante")
    print("2. Editar información de un estudiante")
    print("3. Eliminar estudiante")
    print("4. Salir")

    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:
        agregar_estudiante()
    elif opcion == 2:
        editar_estudiante()
    elif opcion == 3:
        eliminar_estudiante()
    elif opcion == 4:
        break
    else:
        print("Opción no válida.")

# Cerrar conexión a la base de datos
cursor.close()
connection.close()
