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
            "SELECT COUNT(*) FROM viajes WHERE usuario = %s",
            (nombre_usuario,),
        )
        cantidad_usuarios = cursor.fetchone()[0]
        if cantidad_usuarios > 0:
            print("El nombre de usuario ya está registrado. Por favor, elija otro.")
            return

        # Registrar el nuevo usuario si no existe
        cursor.execute(
            "INSERT INTO viajes (usuario) VALUES (%s)",
            (nombre_usuario,),
        )
        connection.commit()
        print("Usuario registrado exitosamente.")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")

# Función para iniciar sesión
def ingresar_usuario():
    usuario = input("Ingrese su nombre de usuario: ")
    try:
        cursor.execute(
            """
            SELECT usuario
            FROM viajes
            WHERE usuario = %s
            """,
            (usuario,),
        )
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

# Función para ingresar datos de gastos
def ingresar_gastos(usuario):
    fecha = input("Ingrese la fecha de sus nuevos gastos (DD/MM/AAAA): ")
    monto = float(input("Ingrese el monto del gasto en Q: "))
    categoria = input("Ingrese la categoría del pago: ")
    try:
        cursor.execute(
            """
            INSERT INTO viajes(usuario, fecha, monto, categoria)
            VALUES (%s, %s, %s, %s)
            """,
            (usuario, fecha, monto, categoria),
        )
        connection.commit()
        print("¡Gasto ingresado exitosamente!")
    except Exception as e:
        print(f"Error al agregar el gasto: {e}")

# Función para ver resumen de gastos
def ver_resumen(usuario):
    try:
        cursor.execute(
            """
            SELECT fecha, monto, categoria
            FROM viajes
            WHERE usuario = %s
            """,
            (usuario,),
        )
        resumen = cursor.fetchall()
        if resumen:
            print("Resumen de gastos:")
            for fecha, monto, categoria in resumen:
                print(f"Fecha: {fecha}, Monto: {monto}, Categoría: {categoria}")
        else:
            print("No hay gastos registrados para este usuario.")
    except Exception as e:
        print(f"Error al obtener resumen: {e}")

# Función para ajustar viajes
def ajustar_gastos(usuario):
    categoria = input("Ingrese la categoría del gasto a ajustar: ")
    nuevo_monto = float(input("Ingrese el nuevo monto para la categoría: "))
    try:
        cursor.execute(
            """
            UPDATE viajes
            SET monto = %s
            WHERE usuario = %s AND categoria = %s
            """,
            (nuevo_monto, usuario, categoria),
        )
        connection.commit()
        print("Gasto ajustado exitosamente")
    except Exception as e:
        print(f"Error al ajustar gasto: {e}")

def borrar_usuario(usuario):
    confirmacion = input("¿Está seguro que desea borrar todos los datos? (S/N): ")
    if confirmacion.upper() == "S":
        try:
            cursor.execute(
                "DELETE FROM viajes WHERE usuario = %s",
                (usuario,),
            )
            connection.commit()
            print("Datos del usuario borrado exitosamente.\n")
        
        except Exception as e:
            print(f"Error al borrar las datos del usuario: {e}")
    else:
        print("Los datos no seran borrados")

# Menú principal
def main():
    usuario = None
    while True:
        if usuario is None:
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("Programa de seguimiento de viajes\n1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                usuario = ingresar_usuario()
            elif opcion == "2":
                usuario = registrar_usuario(usuario)
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")        

        else:
            print("1. Agregar nuevo gasto")
            print("2. Ver historial de gastos")
            print("3. Ajustar gastos")
            print("4. Borrar datos del usuario")
            print("5. regresar")

            opcion = input("Ingrese una opción: ")

            if opcion == "1":
                ingresar_gastos(usuario)
            elif opcion == "2":
                ver_resumen(usuario)
            elif opcion == "3":
                ajustar_gastos(usuario)
            elif opcion == "4":
                borrar_usuario(usuario)
                usuario=None
            elif opcion == "5":
                print("¡Hasta luego!")
                usuario = None
            else:
                print("Opción no válida.")


if __name__ == "__main__":
    main()

cursor.close()
connection.close()
