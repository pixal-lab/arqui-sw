from include.bus_functions import *
from datetime import datetime

service_name = "INVEN"

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

                    if command.split(",")[0] == "INFO":
                        INFO, id_de_algo = command.split(',')
                        query = "SELECT nombre, cantidad_disponible, precio, informacion FROM inventario_farmaceutico"
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

                    if command.split(",")[0] == "INFOD":
                        INFOD, id_de_algo = command.split(',')
                        query = "SELECT nombre, cantidad_disponible, precio, id_medicamento FROM inventario_farmaceutico"
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