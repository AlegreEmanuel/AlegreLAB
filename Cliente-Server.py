import socket
import requests
import json
import time



# Configuración del cliente
host = '192.168.201.57'
port = 8080

# Creación del socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexión al servidor
client_socket.connect((host, port))

# Envío de datos al servidor

temp_diccionario = {"temperatura": "", "humedad":""}
client_socket.sendall(json.dumps(temp_diccionario).encode('utf-8'))


# Recepción de datos del servidor
data = client_socket.recv(1024)

# Decodificación de los datos recibidos y muestra del resultado
print(f"Datos recibidos del servidor: {data.decode('utf-8')}")

# Cierre del socket
client_socket.close()

"""
r = requests.get('https://www.frcon.utn.edu.ar/galileo/downld02.txt')

server = socket.socket(family = socket.AF_INET, type=socket.SOCK_STREAM)
server.bind(("0.0.0.0",8080))

server.listen(2)

while True:
    connection, address = server.accept()
    while True:
            data = connection.recv(1024)
            print('received {0}'.format(data))
            if data:
                print('Enviando de regreso los dato al cliente ')
                Diccionario = json.loads(data.decode('utf-8'))
                
                texto = r.text.split("\r\n")
                tamaño = len(texto)
                array = texto[(tamaño-2)]
                

                if(Diccionario == {"temperatura":""}):
                    Diccionario['temperatura'] = array[18:23]
                    data = json.dumps(Diccionario).encode('utf-8')
                    connection.sendall(data)
                elif(Diccionario == {"humedad":""}):
                    Diccionario['humedad'] = array[40:43]
                    data = json.dumps(Diccionario).encode('utf-8')
                    connection.sendall(data)
                elif(Diccionario == {"temperatura":"","humedad":""}):
                    Diccionario['temperatura'] = array[18:23]
                    Diccionario['humedad'] = array[40:43]
                    data = json.dumps(Diccionario).encode('utf-8')
                    connection.sendall(data)
            else:
                print('no hay mas datos de', address)
                break


"""

