import psycopg2

# Conexión a la base de datos
conexion = psycopg2.connect(
    database="canciones",
    user="postgres",
    password="x8jx5yt5",
    host="localhost"
)

# Función para mostrar todas las canciones
def mostrar_canciones():
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM canciones")
    canciones = cursor.fetchall()
    cursor.close()

    for cancion in canciones:
        print(f"Nombre: {cancion[0]}")
        print(f"Artista: {cancion[1]}")
        print("-" * 20)


# Función para buscar canciones por artista
def buscar_por_artista(artista):
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM canciones WHERE artista = %s", (artista,)
    )
    canciones = cursor.fetchall()
    cursor.close()

    if canciones:
        for cancion in canciones:
            print(f"Nombre: {cancion[0]}")
            print(f"Artista: {cancion[1]}")
            print(f"Letra: {cancion[2]}")
            print("-" * 20)
    else:
        print(f"No se encontraron canciones del artista {artista}")

# funcion para buscar canciones por nombre
def buscar_por_nombre(nombre):
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM canciones WHERE nombre LIKE %s", (f"%{nombre}%",)
    )
    canciones = cursor.fetchall()
    cursor.close()

    if canciones:
        for cancion in canciones:
            print(f"Nombre: {cancion[0]}")
            print(f"Artista: {cancion[1]}")
            print(f"Letra: {cancion[2]}")
            print("-" * 20)
    else:
        print(f"No se encontraron canciones con el nombre {nombre}")

# Menú principal
while True:
    print("-" * 20)
    print("**Buscador de canciones**")
    print("-" * 20)
    print("1. Mostrar todas las canciones")
    print("2. Buscar canción por artista")
    print("3. Buscar canción por nombre")
    print("4. Salir")
    print("-" * 20)

    opcion = input("Elige una opción: ")

    if opcion == "1":
        mostrar_canciones()
    elif opcion == "2":
        artista = input("Introduce el nombre del artista: ")
        buscar_por_artista(artista)
    elif opcion == "3":
        nombre = input("Introduce el nombre de la canción: ")
        buscar_por_nombre(nombre)
    elif opcion == "4":
        print("¡Hasta la próxima!")
        break
    else:
        print("Opción no válida. Inténtalo de nuevo.")

# Cierre de la conexión a la base de datos
conexion.close()
