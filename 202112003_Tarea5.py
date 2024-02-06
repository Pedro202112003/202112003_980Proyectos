def registrar_datos():
    nombre = input("Ingrese su nombre: ")
    altura = float(input("Ingrese su altura (en metros): "))
    peso = float(input("Ingrese su peso (en kilogramos): "))

    with open("imc.txt", "w") as archivo:
        archivo.write(f"{nombre},{altura},{peso}")

    print("¡Datos registrados exitosamente!")


registrar_datos()

def calcular_imc():
    with open("imc.txt", "r") as archivo:
        datos = archivo.readline().split(",")

    altura = float(datos[1])
    peso = float(datos[2])
    imc = peso / (altura * altura)

    print(f"Su IMC es: {imc}")

    if imc < 18.5:
        print("Su categoría es: Bajo peso")
    elif imc < 25:
        print("Su categoría es: Peso normal")
    elif imc < 30:
        print("Su categoría es: Sobrepeso")
    else:
        print("Su categoría es: Obesidad")



def guardar_datos():
    with open("imc.txt", "r") as archivo:
        datos = archivo.readline().split(",")

    nombre = datos[0]
    altura = float(datos[1])
    peso = float(datos[2])
    imc = peso / (altura * altura)

    if imc <= 18.5:
        categoria = "Bajo peso"
    elif imc > 18.5 and imc <= 25:
        categoria = "Peso normal"
    elif imc < 25 and imc <=30:
        categoria = "Sobrepeso"
    else:
        categoria = "Obesidad"

    with open("imc.txt", "w") as archivo:
        archivo.write(f"{nombre}, {altura}, {peso}, {imc}, {categoria}")


    print("¡Datos guardados exitosamente!")


def leer_datos():
    try:
        with open("imc.txt", "r") as archivo:
            datos = archivo.readline()
        print(f"Datos: {datos}")

    except FileNotFoundError:
        print("¡Ya no existe el registro de datos!")


def borrar_datos():
    import os

    os.remove("imc.txt")

    print("¡Datos borrados exitosamente!")


def menu():
    while True:
        print("\n**Menú**")
        print("1. Calcular IMC")
        print("2. Guardar datos")
        print("3. leer datos")
        print("4. Borrar datos")
        print("5. Salir")

        opcion = int(input("Ingrese una opción: "))

        if opcion == 1:
            calcular_imc()
        elif opcion == 2:
            guardar_datos()
        elif opcion == 3:
            leer_datos()
        elif opcion == 4:
            borrar_datos()
        elif opcion == 5:
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
menu()