import psycopg2

#conexión con la base de datos
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
        
def leer_preferencias_usuario():
    print("Ingrese sus preferencias de género de películas (opcional, presione Enter para omitir):")
    año = input("Ingrese un año de estreno (opcional, presione Enter para omitir): ")
    genero = input("Ingrese el género de su preferencia (opcional, presione Enter para omitir): ")
    director = input("Ingrese su director favorito (opcional, presione Enter para omitir): ")
    actores = input("Ingrese a qué actores le gustaría ver (opcional, presione Enter para omitir): ")
    clasificacion = input("Ingrese la clasificación que desea (opcional, presione Enter para omitir): ")
    
    # Eliminar espacios en blanco al inicio y al final
    año = año.strip()
    genero = genero.strip()
    director = director.strip()
    actores = actores.strip()
    clasificacion = clasificacion.strip()
    
    return año, genero, director, actores, clasificacion

#funcion de obtenico de datos
def recomendar_peliculas(conexion, año, genero, director, actores, clasificacion):
    try:
        cursor = conexion.cursor()
        # Construir la consulta SQL para buscar películas que coincidan con las preferencias del usuario
        query = "SELECT * FROM peliculas WHERE "
        if año:
            query += f"año = {año} AND "
        if genero:
            query += f"lower(genero) LIKE '%%{genero.lower()}%%' AND "
        if director:
            query += f"lower(director) LIKE '%%{director.lower()}%%' AND "
        if actores:
            query += "ARRAY["
            for actor in actores.split(','):
                query += f"'{actor.strip()}',"
            query = query[:-1]  # Eliminar la última coma
            query += "] <@ actores AND "
        if clasificacion:
            query += f"lower(clasificacion) LIKE '%%{clasificacion.lower()}%%' AND "
        query = query[:-5]  # Eliminar el último 'AND'
        
        cursor.execute(query)
        peliculas_recomendadas = cursor.fetchall()
        return peliculas_recomendadas
    except psycopg2.Error as e:
        print("Error al buscar películas:", e)

# Función principal
def main():
    conexion = conectar_bd()
    if conexion is not None:
        año, genero, director, actores, clasificacion = leer_preferencias_usuario()

        peliculas_recomendadas = recomendar_peliculas(conexion, año, genero, director, actores, clasificacion)
        if peliculas_recomendadas:
            print("Películas recomendadas:")
            for pelicula in peliculas_recomendadas:
                print(pelicula)
        else:
            print("Lo siento, no se encontraron películas que coincidan con sus preferencias.")
        conexion.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    main()
