from include.bus_functions import *
from datetime import datetime

def registro():
    service_name = "REGLO"
    print(service_name)
  
    usuario = input("Ingrese usuario: ")
    contrasena = input("Ingrese password: ")
    nombre = input("Ingrese nombre completo: ")
    contacto = input("Ingrese contacto: ")
    rol = "Paciente"
    
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

    message = generate_string(service_name, 'LOG,{},{},Paciente'.format(username, password))
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

    message = generate_string(service_name, 'GETID,{},Paciente'.format(usuario))
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

def ver_historial(id_paciente):
    service_name = "HISTO"
    print(service_name)
    
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

def ver_doctores(id_paciente):

    #print("A continuación se visualizarán los doctores presentes: ")
    service_name = "CITAS"
    
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
                print("Error.")
                return -1
            else:
                return answer
        break

def ver_citas(id_paciente):

    #print("A continuación se visualizarán los doctores presentes: ")
    service_name = "CITAS"
    print(service_name)
    
    message = generate_string(service_name, 'VER,{}'.format(id_paciente))
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



def agendar(id_paciente, nombre_paciente):
    service_name = "CITAS"
    print(service_name)
    
    
    id_doctor = input('Por favor, introduzca el ID del doctor con el cual quiere realizar la cita:\n' + str(ver_doctores(id_paciente))+'\n')

    message = generate_string(service_name, 'AGENDAR,{},{},{}'.format(id_paciente, nombre_paciente, id_doctor))
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
                print("cita agendada exitosamente")
                return answer
        break


def lista_citas(id_paciente):
    service_name = "CITAS"
    print(service_name)
    
    # Send the query request to the server
    message = generate_string(service_name, 'REAGENDAR,{}'.format(id_paciente))
    sock.sendall(message)
    
    results_array = []  # Array to store results

    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))  # First 5 bytes give expected message size

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                # Assuming `answer` contains newline-separated results
                results_array = answer.split("\n")  # Convert answer into a list of results
                return results_array
        break

def cambiar_hora(id_cita, dia, hora):
    service_name = "CITAS"
    print(service_name)
    
    #Send the query request to the server
    message = generate_string(service_name, 'CAMBIAR,{},{},{}'.format(id_cita,dia,hora))
    sock.sendall(message)
    
    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))  # First 5 bytes give expected message size

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                print("Modificación exitosa!")
        break

def fecha_valida(string_fecha, formato_fecha='%d-%m-%Y'):
    try:
        datetime.strptime(string_fecha, formato_fecha)
        return True
    except:
        return False

def hora_valida(string_tiempo, formato_tiempo='%H:%M:%S'):
    try:
        datetime.strptime(string_tiempo, formato_tiempo)
        return True
    except:
        return False
    
def inventario_info(id_paciente):
    service_name = "CITAS"
    print(service_name)
    
    # Send the query request to the server
    message = generate_string(service_name, 'INFO, {}'.format(id_paciente))
    sock.sendall(message)
    
    results_array = []  # Array to store results

    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))  # First 5 bytes give expected message size

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            #print(f"Received data: {data}")
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                # Assuming `answer` contains newline-separated results
                results_array = answer.split("\n")  # Convert answer into a list of results
                return results_array
        break

def reagendar_cita(id_paciente):
    citas = lista_citas(id_paciente)  # Call the function once and store the result

    if citas:  # Check if the function returned any results
        numero=0
        for cita in citas:  # Iterate over each item in the list
            print(f"Cita {numero + 1}: {cita}")
            numero=numero + 1
        
    else:
        print("No se encontraron citas.")
        return

    eleccion=input("¿Qué cita desea modificar ")
    correcta=int(eleccion)
    final_correcta=correcta-1
    try:
        prueba = citas[int(final_correcta)]
    except:
        print("Elección errónea!")
    else:
        citas_split=citas[int(final_correcta)].strip().split()
        id_cita=citas_split[0].rstrip(',')
        #print(id_cita)
        print("1. La hora")
        print("2. Dia y hora")
        print("3. Cancelar cita")
        print("4. Volver atrás")
        opcion= input("Que desea cambiar? ")
        match opcion:
            case '1' :
                hora = input("Ingrese nueva hora(Formato 20:30:00, eso sería a las 20:30. utilizar formato 24hrs.) ")
                if hora_valida(hora, '%H:%M:%S') == True:
                    dia="nada"
                    cambiar_hora(id_cita, dia, hora)
                    print("\n")
                    print("hora modificada exitosamente.")
                else:
                    print("hora invalida!")

            
            case '2':
                hora = input("Ingrese nueva hora(ejemplo 20:30:00, eso sería a las 20:30. utilizar formato 24hrs.) ")
                if hora_valida(hora, '%H:%M:%S') == True:
                    dia=input("Ingrese nueva fecha(formato 20-12-2024, eso sería 20 de diciembre 2024) ")
                    if fecha_valida(dia, '%d-%m-%Y') == True:
                        cambiar_hora(id_cita, dia, hora)
                        print("\n")
                    else:
                        print("fecha invalida!")
                else:
                    print("hora invalida!")
            case '3':
                hora="nada"
                dia="nada"
                cambiar_hora(id_cita,dia,hora)
                print("\n")
                print("Cita borrada!")
            case '4':
                print("\n")


def ver_prescripcion(id_paciente):
    service_name = "CITAS"
    print(service_name)
    # Send the query request to the server
    message = generate_string(service_name, 'PRESVP,{}'.format(id_paciente))
    sock.sendall(message)
    
    results_array = []  # Array to store results

    while True:
        amount_received = 0
        amount_expected = int(sock.recv(5))  # First 5 bytes give expected message size

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            service_name, status, answer = extract_string_bus(data)
            
            if answer == "ERROR" or status == "NK":
                print("Error al ingresar.")
                return None
            else:
                print("\n")
                results_array = answer.split("\n")
                return results_array
        break

def main():
    logged_in = False
    nombre = None
    id_paciente = None

    while True:
        if logged_in:
            print("Hola paciente {}, seleccione una opción:".format(nombre))
            print("1. Ver historial medico")
            print("2. Ver lista de doctores")
            print("3. Ver citas medicas realizado")
            print("4. agendar con un doctor")
            print("5. Re-agendar cita médica")
            print("6. Información sobre medicamentos, cantidades, precio, nombre.")
            print("7. mis prescripcciones")
            print("0. Salir")
            option = input("Ingrese opción: \n")
            print("\n")

            match option:
                case '0':
                    print("Saliendo del programa.")
                    print("\n")
                    sock.close()
                    break
                case '1':
                    ver_historial(id_paciente)
                    print("\n")
                case '2':
                    print(ver_doctores(id_paciente)+"\n")
                    print("\n")
                case '3':
                    ver_citas(id_paciente)
                    print("\n")
                case '4':
                    agendar(id_paciente, nombre)
                    print("\n")
                case '5':
                    reagendar_cita(id_paciente)
                    print("\n")
                case '6':
                    info=inventario_info(id_paciente)
                    for x in info:
                        print(x)
                    print("\n")
                case '7':
                    prescripciones=ver_prescripcion(id_paciente)
                    if prescripciones:
                        numero=0
                        for prescripcion in prescripciones:
                            print(prescripcion)                  
                case _:
                    print("Opción no válida.")
                    print("\n")
        else:
            print("Seleccione una opción:")
            print("1. Registrarse")
            print("2. Iniciar sesion")
            print("0. Salir")
        
            option = input("Ingrese opción: \n")
            print("\n")

            match option:
                case '1':
                    usuario, nombre = registro()
                    if nombre is not None:
                        logged_in = True
                        id_paciente = get_id(usuario)
                    print("\n")
                case '2':
                    usuario, nombre = iniciar_sesion()
                    if nombre is not None:
                        logged_in = True
                        id_paciente = get_id(usuario)
                    print("\n")
                case '0':
                    print("Saliendo del programa.")
                    print("\n")
                    sock.close()
                    break
                case _:
                    print("Opción no válida.")
                    print("\n")

if __name__ == "__main__":
    main()