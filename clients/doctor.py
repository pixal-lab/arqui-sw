from include.bus_functions import *

def registro():
    service_name = "REGLO"
    print(service_name)
  
    usuario = input("Ingrese usuario: ")
    contrasena = input("Ingrese password: ")
    nombre = input("Ingrese nombre completo: ")
    contacto = input("Ingrese contacto: ")
    rol = "Doctor"
    
    message = generate_string(service_name, 'REG,{},{},{},{},{}'.format(rol, usuario, contrasena, nombre, contacto))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None, None
            else:
                print('Se ha ingresado correctamente')
                return usuario, answer
        break

def iniciar_sesion():
    service_name = "REGLO"
    print(service_name)
    username = input("Ingrese usuario: ")
    password = input("Ingrese password: ")

    message = generate_string(service_name, 'LOG,{},{},Doctor'.format(username, password))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None, None
            else:
                print('Bienvenido {}.'.format(answer))
                return username, answer
        break

def get_id(usuario):
    service_name = "REGLO"
    print(service_name)

    message = generate_string(service_name, 'GETID,{},Doctor'.format(usuario))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error al obtener ID.")
                return None, None
            else:
                return answer
        break

def get_lista_paciente():
    service_name = "REGLO"
    message = generate_string(service_name, '{}'.format("GET_LIST_P"))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error.")
                return -1
            else:
                return answer
        break

def insertar_historial(id_doctor):
    service_name = "HISTO"
    print(service_name)
    id_paciente = input('Ingrese ID del Paciente\n' + str(get_lista_paciente())+'\n')
    descripcion = input("Ingrese descripcion: ")
    
    message = generate_string(service_name, 'INS,{},{},{}'.format(id_paciente, id_doctor, descripcion))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                print('Se ha ingresado correctamente')
                return answer
        break

def ver_historial():
    service_name = "HISTO"
    print(service_name)
    id_paciente = input('Ingrese ID del Paciente\n' + str(get_lista_paciente())+'\n')
    
    message = generate_string(service_name, 'GET,{}'.format(id_paciente))
    sock.sendall(message)
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                print(answer)
                return answer
        break

def main():
    logged_in = False
    nombre = None
    id_doctor = None

    while True:
        if logged_in:
            print("Hola doctor {}, seleccione una opción:".format(nombre))
            print("1. Ingresar historial medico")
            print("2. Ver historial medico")
            print("0. Salir")
            
            option = input("Ingrese opción: ")
            
            match option:
                case '0':
                    print("Saliendo del programa.")
                    sock.close()
                    break
                case '1':
                    insertar_historial(id_doctor)
                case '2':
                    ver_historial()
                case _:
                    print("Opción no válida.")
        else:
            print("Seleccione una opción:")
            print("1. Registrarse")
            print("2. Iniciar sesion")
            print("0. Salir")
        
            option = input("Ingrese opción: ")

            match option:
                case '1':
                    usuario, nombre = registro()
                    if nombre is not None:
                        logged_in = True
                        id_doctor = get_id(usuario)
                case '2':
                    usuario, nombre = iniciar_sesion()
                    if nombre is not None:
                        logged_in = True
                        id_doctor = get_id(usuario)
                case '0':
                    print("Saliendo del programa.")
                    sock.close()
                    break
                case _:
                    print("Opción no válida.")

if __name__ == "__main__":
    main()