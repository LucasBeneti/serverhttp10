from socket import *

servername = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servername, serverPort)) # por ser tcp precisa rolar esse connect antes
msg = input('Digite qualquer coisa lowercase: ')
clientSocket.send(bytes(msg,'utf-8'))
resultado = clientSocket.recv(1024)
print(f"From server: {resultado}")
clientSocket.close()