% Carga del paquete de base de datos de Octave
pkg load database

% Conexión a la base de datos PostgreSQL (necesitas cambiar los valores)
conn = pq_connect(setdbopts('dbname','980proyectos','host','localhost',
'port','5432','user','postgres','password','x8jx5yt5'))

% Función para registrar un nuevo usuario
function registrar_usuario(conn, nombre_usuario)
    query = sprintf("INSERT INTO usuarios2 (nombre_usuario) VALUES ('%s')", nombre_usuario);
    db_execute(conn, query);
    disp("Usuario registrado exitosamente.");
endfunction

% Función para ingresar con un nombre de usuario existente
function ingresar_usuario(nombre_usuario)
    disp(sprintf("Bienvenido, %s!", nombre_usuario));
endfunction

% Función para agregar una nueva tarea
function agregar_tarea(conn, nombre_usuario, tarea, fecha_vencimiento)
    query = sprintf("INSERT INTO tareas (nombre_usuario, tarea, fecha_vencimiento) VALUES ('%s', '%s', '%s')", nombre_usuario, tarea, fecha_vencimiento);
    db_execute(conn, query);
    disp("Tarea agregada exitosamente.");
endfunction

% Función para marcar una tarea como completada
function completar_tarea(conn, id_tarea)
    query = sprintf("UPDATE tareas SET completada = true WHERE id = %d", id_tarea);
    db_execute(conn, query);
    disp("Tarea marcada como completada.");
endfunction

% Función para ver el historial de tareas de un usuario
function ver_historial(conn, nombre_usuario)
    query = sprintf("SELECT * FROM tareas WHERE nombre_usuario = '%s'", nombre_usuario);
    result = db_query(conn, query);
    disp(result);
endfunction

% Función para borrar datos del usuario
function borrar_datos_usuario(conn, nombre_usuario)
    query = sprintf("DELETE FROM tareas WHERE nombre_usuario = '%s'", nombre_usuario);
    db_execute(conn, query);
    query = sprintf("DELETE FROM usuarios2 WHERE nombre_usuario = '%s'", nombre_usuario);
    db_execute(conn, query);
    disp("Datos del usuario borrados exitosamente.");
endfunction

% Men? principal
disp("Bienvenido al sistema de gesti?n de tareas pendientes.");
disp("1. Ingresar con nombre de usuario");
disp("2. Registrar nuevo usuario");
opcion = input("Seleccione una opci?n: ");

switch opcion
    case 1
        nombre_usuario = input("Ingrese su nombre de usuario: ", "s");
        ingresar_usuario(nombre_usuario);

        % Opciones adicionales para el usuario una vez ingresado
        disp("1. Agregar nueva tarea");
        disp("2. Marcar tarea como completada");
        disp("3. Ver historial de tareas");
        disp("4. Borrar datos del usuario");
        opcion_ingreso = input("Seleccione una opci?n: ");

        switch opcion_ingreso
            case 1
                tarea = input("Ingrese la nueva tarea: ", "s");
                fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ", "s");
                agregar_tarea(conn, nombre_usuario, tarea, fecha_vencimiento);
            case 2
                id_tarea = input("Ingrese el ID de la tarea a marcar como completada: ");
                completar_tarea(conn, id_tarea);
            case 3
                ver_historial(conn, nombre_usuario);
            case 4
                borrar_datos_usuario(conn, nombre_usuario);
            otherwise
                disp("Opci?n no v?lida.");
        endswitch

    case 2
        nombre_usuario = input("Ingrese su nombre de usuario: ", "s");
        registrar_usuario(conn, nombre_usuario);

        % Opciones adicionales para el usuario una vez registrado
        disp("1. Agregar nueva tarea");
        disp("2. Marcar tarea como completada");
        disp("3. Ver historial de tareas");
        disp("4. Borrar datos del usuario");
        opcion_registro = input("Seleccione una opci?n: ");

        switch opcion_registro
            case 1
                tarea = input("Ingrese la nueva tarea: ", "s");
                fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ", "s");
                agregar_tarea(conn, nombre_usuario, tarea, fecha_vencimiento);
            case 2
                id_tarea = input("Ingrese el ID de la tarea a marcar como completada: ");
                completar_tarea(conn, id_tarea);
            case 3
                ver_historial(conn, nombre_usuario);
            case 4
                borrar_datos_usuario(conn, nombre_usuario);
            otherwise
                disp("Opci?n no v?lida.");
        endswitch

    otherwise
        disp("Opci?n no v?lida.");
endswitch


% Cierre de la conexión a la base de datos
db_close(conn);
