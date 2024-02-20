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

def registrar_usuario():
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    try:
        cursor.execute(
            """
            INSERT INTO GastosAlimentos(nombre_usuario)
            VALUES (%s)
            """,
            (nombre_usuario,),
        )
        connection.commit()
        print("¡Usuario registrado exitosamente!")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")

# Función para iniciar sesión
def ingresar_usuario():
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    try:
        cursor.execute(
            """
            SELECT nombre_usuario
            FROM GastosAlimentos
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

# Función para registrar gastos en alimentos
def registrar_gasto_alimentos(nombre_usuario):
    fecha = datetime.now().date()
    monto = float(input("Ingrese el monto gastado en alimentos: "))
    categoria = input("Ingrese la categoría del gasto en alimentos: ")
    meta_calorias = int(input("Ingrese la calorías consumidas: "))
    try:
        cursor.execute(
            """
            INSERT INTO GastosAlimentos(nombre_usuario, fecha, monto, categoria, meta_calorias)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre_usuario, fecha, monto, categoria, meta_calorias),
        )
        connection.commit()
        print("¡Gasto en alimentos registrado exitosamente!")
    except Exception as e:
        print(f"Error al registrar gasto en alimentos: {e}")

# Función para ver historial de gastos en alimentos
def ver_historial_gastos_alimentos(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT fecha, monto, categoria, meta_calorias
            FROM GastosAlimentos
            WHERE nombre_usuario = %s
            ORDER BY fecha DESC
            """,
            (nombre_usuario,),
        )
        historial = cursor.fetchall()
        if historial:
            print("Historial de gastos en alimentos:")
            for fecha, monto, categoria, meta_calorias in historial:
                print(f"Fecha: {fecha}, Monto: {monto}, Categoría: {categoria}, Meta de calorías: {meta_calorias}")
        else:
            print("No hay registros de gastos en alimentos para este usuario.")
    except Exception as e:
        print(f"Error al obtener historial de gastos en alimentos: {e}")

# Función para realizar análisis de hábitos alimenticios
def analisis_habitos_alimenticios(nombre_usuario):
    try:
        cursor.execute(
            """
            SELECT SUM(monto) AS total_gastado, AVG(monto) AS gasto_promedio, AVG(meta_calorias) AS calorias
            FROM GastosAlimentos
            WHERE nombre_usuario = %s
            """,
            (nombre_usuario,),
        )
        resultado = cursor.fetchone()
        if resultado:
            total_gastado = resultado[0]
            gasto_promedio = resultado[1]
            calorias = resultado[2]
            print(f"Total gastado en alimentos: {total_gastado}")
            print(f"Gasto promedio por día: {gasto_promedio}")
            print(f"Calorias promedio por día: {calorias} Kcal")
            # Puedes agregar más estadísticas según sea necesario
        else:
            print("No hay registros de gastos en alimentos para este usuario.")
    except Exception as e:
        print(f"Error al realizar análisis de hábitos alimenticios: {e}")

# Función para ajustar presupuesto
def ajustar_presupuesto(nombre_usuario):
    nuevo_presupuesto = float(input("Ingrese el nuevo presupuesto para gastos en alimentos: "))
    try:
        cursor.execute(
            """
            UPDATE GastosAlimentos
            SET presupuesto = %s
            WHERE nombre_usuario = %s
            """,
            (nuevo_presupuesto, nombre_usuario),
        )
        connection.commit()
        print("Presupuesto ajustado exitosamente.")
    except Exception as e:
        print(f"Error al ajustar presupuesto: {e}")

# Función para establecer metas nutricionales
def establecer_metas_nutricionales(nombre_usuario):
    meta_calorias = int(input("Ingrese su meta de calorías diarias: "))
    try:
        cursor.execute(
            """
            UPDATE GastosAlimentos
            SET meta_calorias = %s
            WHERE nombre_usuario = %s
            """,
            (meta_calorias, nombre_usuario),
        )
        connection.commit()
        print("Metas nutricionales establecidas exitosamente.")
    except Exception as e:
        print(f"Error al establecer metas nutricionales: {e}")

# Menú principal
def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de seguimiento de gastos en alimentos")
            print("Por favor, ingrese o registre un usuario.")
            opcion = input("1. Ingresar\n2. Registrar\n3. Salir\nSeleccione una opción: ")
            if opcion == "1":
                nombre_usuario = ingresar_usuario()
            elif opcion == "2":
                nombre_usuario = registrar_usuario()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione nuevamente.")
        else:
            print("1. Registrar gasto en alimentos")
            print("2. Ver historial de gastos en alimentos")
            print("3. Análisis de hábitos alimenticios")
            print("4. Ajustar presupuesto")
            print("5. Establecer metas nutricionales")
            print("6. regresar")

            opcion2 = input("Ingrese una opción: ")

            if opcion2 == "1":
                registrar_gasto_alimentos(nombre_usuario)
            elif opcion2 == "2":              
                ver_historial_gastos_alimentos(nombre_usuario)
            elif opcion2 == "3":
                analisis_habitos_alimenticios(nombre_usuario)
            elif opcion2 == "4":
                ajustar_presupuesto(nombre_usuario)
            elif opcion2 == "5":
                establecer_metas_nutricionales(nombre_usuario)
            elif opcion2 == "6":
                print("¡Hasta luego!")
                nombre_usuario=None
            else:
                print("Opción no válida.")

if __name__ == "__main__":
    main()
cursor.close()
connection.close()
