import psycopg2

#conexión con la base de datos
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

#Funcion para ingresar datos 
def ingresar_gastos():
    fecha=input("ingrese sus nuevos gastos (DD/MM/AAAA): ")
    descripcion=input("ingrese la descripcion del gasto: ")
    monto=float(input("Ingrese el monto del gasto en Q: "))
    metodo_pago=input("Ingrese el metodo de pago: ")
    categoria=input("ingrese la categoria del pago: ")

    try:
        cursor.execute(
            """
            INSERT INTO presupuesto(fecha, descripcion, monto, metodo_pago, categoria)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (fecha, descripcion, monto, metodo_pago, categoria),
        )
        connection.commit()
        print("¡Gasto ingresado exitosamente!")
    except Exception as e:
        print(f"Error al agregar el gasto: {e}")

#Funcion para resumen de gastos segun categoria
def ver_resumen():
    opcion = input(
        "Seleccione cómo desea ver el resumen de gastos (1: por fecha, 2: por método de pago 3: categoria): "
    )

    try:
        if opcion == "1":
            cursor.execute(
                """
                SELECT fecha, SUM(monto) AS total
                FROM presupuesto
                GROUP BY fecha
                ORDER BY fecha DESC
                """
            )
            print("Resumen de gastos por fecha:")
            for fecha, total in cursor.fetchall():
                print(f"{fecha}: Q{total}")
        elif opcion == "2":
            cursor.execute(
                """
                SELECT metodo_pago, SUM(monto) AS total
                FROM presupuesto
                GROUP BY metodo_pago
                ORDER BY total DESC
                """
            )
            print("Resumen de gastos por método de pago:")
            for metodo_pago, total in cursor.fetchall():
                print(f"{metodo_pago}: Q{total}")
        
        elif opcion == "3":
            cursor.execute(
                """
                SELECT categoria, SUM(monto) AS total
                FROM presupuesto
                GROUP BY categoria
                ORDER BY total DESC
                """
            )
            print("resumen de gastos pir categoria: ")
            for categoria, total in cursor.fetchall():
                print(f"{categoria}: Q{total}")

        else:
            print("Opción no válida.")

    except Exception as e:
        print(f"Error al obtener resumen: {e}")

# Función para ajustar presupuestos
def ajustar_presupuesto():
    categoria = input("Ingrese la categoría del presupuesto a ajustar: ")
    nuevo_presupuesto = float(input("Ingrese el nuevo presupuesto para la categoría: "))

    try:
        cursor.execute(
            """
            UPDATE presupuesto
            SET monto = %s
            WHERE categoria = %s
            """,
            (nuevo_presupuesto, categoria),
        )
        connection.commit()
        print("Presupuesto actualizado exitosamente")
    except Exception as e:
        print(f"Error al actualizar presupuesto: {e}")

# Menú principal
#def menu():
while True:
    print("\n**Programa de seguimiento de presupuesto personal**")
    print("1. Agregar nuevo gasto")
    print("2. Ver resumen de gastos")
    print("3. Ajustar presupuestos")
    print("4. Salir")

    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:
        ingresar_gastos()
    elif opcion == 2:
        ver_resumen()
    elif opcion == 3:
        ajustar_presupuesto()
    elif opcion == 4:
        print("¡Hasta luego!")
        break
    else:
        print("opción no válida.")

##menu()
cursor.close()
connection.close()
        


