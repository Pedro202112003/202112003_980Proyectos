import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Función para conectar a la base de datos PostgreSQL
def conectar_bd():
    try:
        conexion = psycopg2.connect(
            dbname="980proyectos",
            user="postgres",
            password="x8jx5yt5",
            host="localhost"
        )
        print("Conexión establecida a la base de datos")
        return conexion
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)

# Función para seleccionar el sensor
def seleccionar_sensor(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM sensores")
        sensores = cursor.fetchall()
        print("Seleccione el sensor:")
        for sensor in sensores:
            print(f"{sensor[0]}. {sensor[1]}")
        id_sensor = int(input("Ingrese el ID del sensor que desea analizar: "))
        return id_sensor
    except psycopg2.Error as e:
        print("Error al seleccionar el sensor:", e)

# Función para obtener los datos del sensor seleccionado
def obtener_datos_sensor(conexion, id_sensor):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT tiempo, lectura FROM lecturas WHERE id_sensor = %s", (id_sensor,))
        datos = cursor.fetchall()
        # Crear un DataFrame de pandas con los datos obtenidos
        df = pd.DataFrame(datos, columns=['Tiempo', 'Lectura'])
        return df
    except psycopg2.Error as e:
        print("Error al obtener los datos del sensor:", e)

# Función para mostrar los datos del sensor en forma de tabla
def mostrar_tabla(datos_sensor):
    print("Datos del sensor seleccionado:")
    print(datos_sensor)

# Función para mostrar los datos del sensor en forma de gráfico
def mostrar_grafico(datos_sensor):
    plt.plot(datos_sensor['Tiempo'], datos_sensor['Lectura'])
    plt.xlabel("Tiempo")
    plt.ylabel("Lectura")
    plt.title("Datos del sensor")
    plt.show()

# Función principal del menú
def menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Seleccionar sensor")
        print("2. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            conexion = conectar_bd()
            if conexion is not None:
                id_sensor = seleccionar_sensor(conexion)
                datos_sensor = obtener_datos_sensor(conexion, id_sensor)
                if datos_sensor is not None:
                    sub_menu(datos_sensor)
                conexion.close()
                print("Conexión cerrada")
        elif opcion == "2":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

# Función para el submenú de visualización
def sub_menu(datos_sensor):
    while True:
        print("\n--- Submenú de Visualización ---")
        print("1. Mostrar tabla")
        print("2. Mostrar gráfico")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            mostrar_tabla(datos_sensor)
        elif opcion == "2":
            mostrar_grafico(datos_sensor)
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    menu_principal()
