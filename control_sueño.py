# Importar librerías
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

# Conectar a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="x8jx5yt5",
    database="980proyectos",
)

cursor = conn.cursor()

# Función para insertar un registro de sueño
def insertar_sueño(nombre, fecha, hora):
    cursor.execute("INSERT INTO sueño (nombre, fecha, hora) VALUES (%s, %s, %s)", (nombre, fecha, hora))
    conn.commit()

# Función para obtener todos los registros de sueño de un nombre
def get_sueño(nombre):
    cursor.execute("SELECT * FROM sueño WHERE nombre = %s", (nombre,))
    return cursor.fetchall()

# Función para obtener el promedio de horas de sueño por día de la semana de un nombre
def sueño_semanal(nombre):
    cursor.execute("SELECT EXTRACT(DOW FROM fecha) AS weekday, AVG(hora) AS average FROM sueño WHERE nombre = %s GROUP BY weekday ORDER BY weekday", (nombre,))
    return cursor.fetchall()

# Función para mostrar un gráfico de barras con el promedio de horas de sueño por día de la semana
def grafica_sueño(data):
    semana = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    promedio_total = np.mean([row[1] for row in data])
    min_dia = min(data, key=lambda row: row[1])
    max_dia = max(data, key=lambda row: row[1])
    print(f"Tu promedio total es de {promedio_total:.2f}")
    print(f"tu tiempo de sueño nimimo fue el {semana[int(min_dia[0])]}, con {min_dia[1]:.2f}")
    print(f"tu tiempo de sueño maximo fie el {semana[int(max_dia[0])]}, con {max_dia[1]:.2f}")
def sugerencia_sueño(data):
    semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    promedio_total = np.mean([row[1] for row in data])
    min_dia = min(data, key=lambda row: row[1])
    max_dia = max(data, key=lambda row: row[1])
    sugerencia = []
    if promedio_total < 7:
        sugerencia.append(f"""Deberías dormir más horas en general. El promedio recomendado es de al menos 7
                          hora por noche. Su promedio actual es {promedio_total:.2f} hora.""")
    if abs(min_dia[1] - max_dia[1]) > 2:
        sugerencia.append(f"""Deberías tener un horario de sueño más regular. Durmiendon mucho más o mucho menos algunos
                          días puede afectar su ritmo carcadiano. Tu día con menos horas de sueño
                          es el {semana[int(min_dia[0])]}, con {min_dia[1]:.2f} hora. Tu dia 
                           con mas horas de sueño {semana[int(max_dia[0])]}, con {max_dia[1]:.2f} hora.""")
    if not sugerencia:
        sugerencia.append("¡Feilicadades! Tienes un buen habito de sueño")
    return sugerencia

# Función para validar la entrada del usuario
def validar_u(prompt, type, min=None, max=None):
    while True:
        try:
            value = type(input(prompt))
            if min is not None and value < min:
                raise ValueError(f"El valor debe ser mayor o igual a {min}")
            if max is not None and value > max:
                raise ValueError(f"El valor debe ser menor o igual a {max}")
            return value
        except ValueError as e:
            print(f"Entrada inválida: {e}")
def menu():
    print("Selecciona una opción:")
    print("1. Registrar horas de sueño")
    print("2. Ver registros de sueño")
    print("3. Ver análisis de sueño")
    print("4. Ver sugerencias")
    print("5. Regresar")
# Función principal
while True:
    # Obtener el nombre del usuario
    regis = input("""Programa de registro y análisis de sueño. \n1. Ingresar\n2.Registrar\n3. Salir 
    \nSeleccione una opccion: """)
    if regis == "1":
        nombre = input("Ingresa tu nombre:  ")
        print(f"Bienvenido de vuelta {nombre}")
    elif regis == "2":
        nombre = input("Ingresa tu nombre:  ")
        print("Usuario registrado exitosamente")
    elif regis == "3":
        break
    else: 
        print("opción no valida")
    # Mostrar el menú interactivo
    menu()
    # Obtener la opción del usuario
    option = validar_u("Elige una opción: ", int, 1, 5)
    # Repetir hasta que el usuario elija salir
    while option != 5:
        # Ejecutar la opción elegida
        if option == 1:
            # Registrar horas de sueño
            fecha = input("Registrar fecha (AAAA-MM-DD) ")
            hora = validar_u("Horas de sueño: ", float, 0)
            insertar_sueño(nombre, fecha, hora)
            print("Registro guardado con éxito.")
        elif option == 2:
            # Ver registros de sueño
            sueño_data = get_sueño(nombre)
            if sueño_data:
                print("Estos son tus registros de sueño:")
                for row in sueño_data:
                    print(f"Fecha: {row[1]}, Horas: {row[2]}")
            else:
                print("No tienes registros de sueño.")
        elif option == 3:
            # Ver análisis de patrón de sueño
            sueño_promedio = sueño_semanal(nombre)
            if sueño_promedio:
                print("Este es tu análisis de patrón de sueño:")
                grafica_sueño(sueño_promedio)
            else:
                print("No tienes suficientes datos para el análisis.")
        elif option == 4:
            # Ver sugerencias para mejorar la calidad de descanso
            sueño_promedio = sueño_semanal(nombre)
            if sueño_promedio:
                print("Estas son tus sugerencias para mejorar la calidad de sueño:")
                sueño_suggestions = sugerencia_sueño(sueño_promedio)
                for suggestion in sueño_suggestions:
                    print(f"- {suggestion}")
            else:
                print("No tienes suficientes datos para las sugerencias.")
        # Mostrar el menú interactivo de nuevo
        menu()
        # Obtener la opción del usuario de nuevo
        option = validar_u("Elige una opción ", int, 1, 5)
    # Despedirse del usuario
    print("Gracias por usar el programa. ¡Hasta pronto!")


