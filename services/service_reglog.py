from include.bus_functions import *

service_name = "REGLO"

try:

    # Send SINIT to the bus
    message = generate_sinit(service_name)
    print ('sending {!r}'.format (message))
    sock.sendall (message)
    sinit = 1
    while True:
    # Look for the response
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len(data)
            print ('received {!r}'.format (data))
            if (sinit == 1):
                 sinit = 0
                 print("sinit ok")
            else:
                # If is not a SINIT message, then is a command from the client
                incoming_svr, command = extract_string_client(data)
                print("Incoming for:",incoming_svr)
                if incoming_svr==service_name: # Check if the command is for me
                    print("That's for me")
                    print("Command:", command)

                    # Send the command to the database service
                    if command.split(",")[0] == "REG":
                        reg, rol, usuario, contrasena, nombre, contacto = command.split(',')
                        query = "INSERT into usuarios (nombre_usuario, contrasena, nombre_completo, rol, contacto) values ('{}', '{}', '{}', '{}', '{}')".format(usuario, contrasena, nombre, rol, contacto)
                        answer = servbd_query(query)
                        if answer == "" or answer == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, nombre)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                    if command.split(",")[0] == "LOG":
                        log, Log_usuario, Log_contrasena = command.split(',')
                        query = "select nombre_completo from usuarios where nombre_usuario = '{}' and contrasena = '{}'".format(Log_usuario, Log_contrasena)
                        answer = servbd_query(query)
                        if answer == "" or answer == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

finally:
    print ('closing socket')
    sock.close()