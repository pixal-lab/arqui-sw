from include.bus_functions import *

def registro():
    service_name = "REGLO"
    print(service_name)
  
    usuario = input("Ingrese usuario: ")
    contrasena = input("Ingrese password: ")
    nombre = input("Ingrese nombre completo: ")
    contacto = input("Ingrese contacto: ")
    rol = "Paciente"
    
    message = generate_string(service_name, 'REG,{},{},{},{},{}'.format(usuario, contrasena, nombre, rol, contacto))
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

    message = generate_string(service_name, 'LOG,{},{}'.format(username, password))
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

def main():
    logged_in = False
    nombre = None

    while True:
        if logged_in:
            print("Hola paciente {}, seleccione una opción:".format(nombre))
        else:
            print("Seleccione una opción:")
            print("1. Registrarse")
            print("2. Iniciar sesion")
        
            option = input("Ingrese opción: ")

            match option:
                case '1':
                    usuario, nombre = registro()
                    if nombre is not None:
                        logged_in = True
                case '2':
                    usuario, nombre = iniciar_sesion()
                    if nombre is not None:
                        logged_in = True
                case '0':
                    print("Saliendo del programa.")
                    sock.close()
                    break
                case _:
                    print("Opción no válida.")

if __name__ == "__main__":
    main()