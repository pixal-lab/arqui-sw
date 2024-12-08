from include.bus_functions import *
from datetime import datetime

service_name = "CITAS"

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
                    if command.split(",")[0] == "AGENDAR":
                        AGENDAR, id_paciente, nombre_paciente, id_doctor = command.split(',')

                        fecha_formateada=datetime.now().strftime('%Y-%m-%d %H:%M:00')
                        query = "INSERT into citas (id_paciente, id_doctor, nombre_paciente, nombre_doctor, fecha) values ('{}', '{}', '{}', (SELECT nombre_completo FROM usuarios WHERE id_usuario = '{}'), '{}')".format(id_paciente, id_doctor, nombre_paciente, id_doctor, fecha_formateada)
                        answer = servbd_query(query)
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

                    if command.split(",")[0] == "GET":
                        rol="Doctor"
                        GET, id_paciente = command.split(',')
                        query = "select id_usuario, nombre_completo from usuarios where rol = '{}' ".format(rol)
                        answer = servbd_query(query)
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

                    if command.split(",")[0] == "VER":
                        VER, id_paciente = command.split(',')
                        query = "select nombre_doctor, fecha from citas where id_paciente = '{}' ".format(id_paciente)
                        answer = servbd_query(query)
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)


                    if command.split(",")[0] == "REAGENDAR":
                        REAGENDAR, id_paciente = command.split(',')
                        query = "select id_cita, nombre_doctor, fecha from citas where id_paciente = '{}' ".format(id_paciente)
                        answer = servbd_query(query)
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

                    if command.split(",")[0] == "REAGENDARD":
                        REAGENDARD, id_doctore = command.split(',')
                        query = "select id_cita, nombre_paciente, fecha, id_paciente from citas where id_doctor = '{}' ".format(id_doctore)
                        answer = servbd_query(query)
                        if answer == "" or answer[:5] == "ERROR":
                            message = generate_string(service_name, "ERROR")
                            print('sending {!r}'.format (message))
                            sock.sendall (message)
                        else:
                            message = generate_string(service_name, answer)
                            print('sending {!r}'.format (message))
                            sock.sendall (message)

                    if command.split(",")[0] == "CAMBIAR":
                        print(f"Received command: {command}")
                        CAMBIAR, id_cita, dia, hora = command.split(',')
                        #print(f"Generating message with: id_cita={id_cita}, dia={dia}, hora={hora}")

                        if dia=="nada" and hora!= "nada":
                            hour, minute, second = hora.split(':')
                            string_intervalo="{} minutes".format(int(hour) * 60 + int(minute))
                            query = "UPDATE citas set fecha = DATE_TRUNC('day', fecha) + INTERVAL '{} minute' WHERE id_cita = '{}'".format(string_intervalo, id_cita)
                        elif hora=="nada" and dia=="nada":
                            query = "DELETE from citas where id_cita = '{}'".format(id_cita)
                        elif dia != "nada" and hora != "nada":
                            day, month, year = dia.split("-")
                            fecha_trabajada="{}-{}-{}".format(year,month,day)
                            parte_fecha = fecha_trabajada
                            parte_tiempo = hora 
                            fecha_nueva = "{} {}".format(parte_fecha, parte_tiempo)
                            query = "UPDATE citas SET fecha = '{}' WHERE id_cita = '{}'".format(fecha_nueva, id_cita)

                        answer = servbd_query(query)
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