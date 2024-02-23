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
    print(f"Error de conexión con la base de datos: {e}")
    exit()

def registrar_usuario():
    nombre_usuario = input("Ingrese un nombre de usuario: ")
    try:
        cursor.execute(
            """
            INSERT INTO RegistroSueño(nombre_usuario)
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
            FROM RegistroSueño
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

# Función para registrar horas de sueño
def registrar_horas_sueño(nombre_usuario):
    fecha = input("Ingrese la fecha de registro (YYYY-MM-DD): ")
    horas_sueño = int(input("Ingrese la cantidad de horas de sueño: "))
    try:
        cursor.execute(
            "INSERT INTO RegistroSueño (nombre_usuario, fecha, horas_sueño) VALUES (%s, %s, %s)",
            (nombre_usuario, fecha, horas_sueño),
        )
        connection.commit()
        print("Registro de sueño añadido exitosamente.")
    except Exception as e:
        print(f"Error al registrar las horas de sueño: {e}")

# Función para ver el historial de sueño
def ver_historial_sueño(nombre_usuario):
    try:
        cursor.execute(
            "SELECT fecha, horas_sueño FROM RegistroSueño WHERE nombre_usuario = %s ORDER BY fecha DESC",
            (nombre_usuario,),
        )
        registros = cursor.fetchall()
        print("Historial de sueño:")
        for registro in registros:
            print(f"Fecha: {registro[0]}, Horas de sueño: {registro[1]}")
    except Exception as e:
        print(f"Error al obtener el historial de sueño: {e}")

# Función para borrar un registro de sueño
def borrar_registro_sueño(nombre_usuario):
    fecha = input("Ingrese la fecha del registro a borrar (YYYY-MM-DD): ")
    try:
        cursor.execute(
            "DELETE FROM RegistroSueño WHERE nombre_usuario = %s AND fecha = %s",
            (nombre_usuario, fecha),
        )
        connection.commit()
        print("Registro de sueño borrado exitosamente.")
    except Exception as e:
        print(f"Error al borrar el registro de sueño: {e}")

# Función para analizar patrones de sueño
def analizar_patrones_sueño(nombre_usuario):
    try:
        # Promedio de horas de sueño
        cursor.execute(
            "SELECT AVG(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        promedio = cursor.fetchone()[0]

        # Máximo de horas de sueño
        cursor.execute(
            "SELECT fecha, MAX(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s GROUP BY fecha ORDER BY MAX(horas_sueño) DESC LIMIT 1",
            (nombre_usuario,),
        )
        maximo = cursor.fetchone()

        # Mínimo de horas de sueño
        cursor.execute(
            "SELECT fecha, MIN(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s GROUP BY fecha ORDER BY MIN(horas_sueño) ASC LIMIT 1",
            (nombre_usuario,),
        )
        minimo = cursor.fetchone()

        print(f"\nPromedio de horas de sueño: {promedio:.2f} horas.")
        if maximo:
            print(f"Mayor cantidad de sueño el {maximo[0]} con {maximo[1]} horas.")
        if minimo:
            print(f"Menor cantidad de sueño el {minimo[0]} con {minimo[1]} horas.")
    except Exception as e:
        print(f"Error al analizar patrones de sueño: {e}")

# Función para ofrecer sugerencias para mejorar la calidad del sueño
def sugerencias_calidad_sueño(nombre_usuario):
    try:
        # Promedio de horas de sueño
        cursor.execute(
            "SELECT AVG(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        promedio = cursor.fetchone()[0]

        # Máximo de horas de sueño
        cursor.execute(
            "SELECT MAX(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        maximo = cursor.fetchone()[0]

        # Mínimo de horas de sueño
        cursor.execute(
            "SELECT MIN(horas_sueño) FROM RegistroSueño WHERE nombre_usuario = %s",
            (nombre_usuario,),
        )
        minimo = cursor.fetchone()[0]

        print(f"\nPromedio de horas de sueño: {promedio:.2f} horas.")
        if promedio < 7:
            print("Parece que no estás durmiendo lo suficiente. Intenta establecer una rutina nocturna que promueva el sueño.")
        elif promedio > 9:
            print("Estás durmiendo más de lo recomendado para la mayoría de los adultos. Si te sientes muy cansado durante el día, considera consultar a un médico.")
        else:
            print("Tu promedio de sueño está dentro del rango recomendado. ¡Sigue así!")

        if minimo < 5:
            print("Tus noches de menor sueño son muy cortas. Asegúrate de no tener grandes variaciones en tu horario de sueño.")
        
        if maximo > 10:
            print("Algunas de tus noches tienen un exceso de sueño. Intenta evitar dormir mucho más de lo habitual para mantener un ritmo regular.")

        # Sugerencias generales
        print("\nSugerencias generales para mejorar la calidad del sueño:")
        print("- Mantén un horario regular para dormir y despertar.")
        print("- Reduce la exposición a pantallas electrónicas antes de dormir.")
        print("- Asegúrate de que tu dormitorio sea un espacio tranquilo, oscuro y fresco.")
        print("- Considera hacer ejercicio regularmente, pero no justo antes de dormir.")
    except Exception as e:
        print(f"Error al generar sugerencias para mejorar la calidad del sueño: {e}")

def main():
    nombre_usuario = None
    while True:
        if nombre_usuario is None:
            print("Programa de control de sueño")
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
            print("1. Registrar horas de sueño")
            print("2. Ver historial de sueño")
            print("3. Borrar registro de sueño")
            print("4. Analizar patrones de sueño")
            print("5. Sugerencias para mejorar el sueño")
            print("6. Regresar")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                registrar_horas_sueño(nombre_usuario)
            elif opcion == "2":
                ver_historial_sueño(nombre_usuario)
            elif opcion == "3":
                borrar_registro_sueño(nombre_usuario)
            elif opcion == "4":
                analizar_patrones_sueño(nombre_usuario)
            elif opcion == "5":
                sugerencias_calidad_sueño( nombre_usuario)
            elif opcion == "6":
                nombre_usuario = None
            else:
                print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    main()
# Cerrar conexión con la base de datos al salir del programa
cursor.close()
connection.close()
