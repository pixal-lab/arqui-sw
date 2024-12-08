from include.bus_functions import *
from datetime import datetime

service_name = "PRESC"

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

                    if command.split(",")[0] == "PRESC":
                        PRESC,id_d, id_p, nombre_d, nombre_p, id_medicamento, instrucciones, nombre_medicamento = command.split(',')
                        query = "INSERT into prescripcion(id_medicamento, id_paciente, nombre_doctor, nombre_paciente, id_doctor, instrucciones, nombre_medicamento) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(id_medicamento,id_p,nombre_d,nombre_p,id_d, instrucciones, nombre_medicamento)
                        print(f"Executing query: {query}")
                        answer = servbd_query(query)
                        print(f"Query result: {answer}")  # Debug query output
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

                    if command.split(",")[0] == "PRESVP":
                        PRESVD, id_p = command.split(',')
                        query="SELECT nombre_doctor, nombre_medicamento, instrucciones, id_prescripcion from prescripcion where id_paciente = '{}'".format(id_p)
                        print(f"Executing query: {query}")
                        answer = servbd_query(query)
                        print(f"Query result: {answer}")  # Debug query output
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                            
                    if command.split(",")[0] == "PRESVD":
                        PRESVD, id_d, id_p = command.split(',')
                        query="SELECT nombre_paciente, nombre_medicamento, instrucciones, id_prescripcion from prescripcion where id_doctor = '{}' and id_paciente = '{}'".format(id_d, id_p)
                        print(f"Executing query: {query}")
                        answer = servbd_query(query)
                        print(f"Query result: {answer}")  # Debug query output
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)              



finally:
    print('closing socket')
    sock.close()