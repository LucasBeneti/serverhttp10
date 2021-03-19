import os
import socket
import _thread
import base64

# ip do note na rede local
HOST = '192.168.0.78'
PORT = 12000 # porta aleatória

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((HOST, PORT))
serverSocket.listen(1) # pool de requests na lista de espera
print(f"Listening on {HOST}:{PORT}")

file_extension_dict = {
    'css':'Content-Type: text/css',
    'html':'Content-Type: text/html',
    'js':'Content-Type: text/javascript',
    'gif':'Content-Type: image/gif',
    'png':'Content-Type: image/png',
    'jpeg':'Content-Type: image/jpeg',
    'bmp':'Content-Type: image/bmp',
    'webp':'Content-Type: image/webp',
}

def encodeImage(fileName):
    try:
        with open(fileName,'rb') as imageFile:
            encoded_res = base64.b64encode(imageFile.read())
    except:
        raise Error('Erro na leitura da imagem')
        encoded_res = ''
    finally:
        # print(encoded_res)
        return str(encoded_res)

def getErrorResponse():
    file_reader = open('src/404.html')
    responseContent = file_reader.read()
    file_reader.close()
    responseStatus = 404
    statusMessage = 'Not Found'
    contentType = file_extension_dict['html']
    final_response = {
        'status': responseStatus,
        'statusMessage': statusMessage,
        'data': responseContent,
        'contentType': contentType,
    }
    return final_response

def getResponseContent(fileName):
    file_extension = fileName.split('.')[-1]
    img_extensions = ['gif', 'png', 'jpeg', 'bmp', 'webp']
    final_response = {}
    # print('extensao da file:',file_extension)
    # print('filename entrando na getContent', fileName)
    if (fileName == ''):
        print('entrou no primeiro if do getContent')
        with open("src/index.html","rb") as file_reader:
            file_content = file_reader.read()
        response_status = 200
        status_message = 'OK'
        content_type = file_extension_dict['html']
        
    elif (file_extension in file_extension_dict):
        with open(f"src/{fileName}", "rb") as file_reader:
            file_content = file_reader.read()
        response_status = 200
        status_message = 'OK'
        content_type = file_extension_dict[file_extension]
    else:
        raise Error('algum erro no arquivo pedido')

    final_response = {
        'status': response_status,
        'statusMessage': status_message,
        'data': file_content,
        'contentType': content_type,
    }
    return final_response

def checkFileExistance(filePath):
    path_check = os.path.abspath(f'{filePath}')
    print(path_check)
    if os.path.isfile(path_check):
        return True
    else:
        raise Error('FILE NOT FOUND check file')
        return False


def parseRequest(request):
    fileNameRaw = request.split('\n')[0].split(' ')[1]
    fileName = fileNameRaw[1:]
    print('fileName', fileName)
    try:
        fileToCheck = 'src/' + fileName
        if (fileName == ''):
            response = getResponseContent(fileName)
        elif (checkFileExistance(fileToCheck)):
            # pega o conteudo correto da file
            response = getResponseContent(fileName)
        else:
            raise Error('FILE NOT FOUND parseRequest')
    except:
        response = getErrorResponse()
    finally:
        return response

def handleResponse(connection):
    request = connection.recv(4096).decode()
    print(request)

    response_body = parseRequest(request)

    headerTuple = ('HTTP/1.0 ', f"{response_body['status']}", f"{response_body['statusMessage']}\n", f"{response_body['contentType']}\n","Connection: close\n",'\n')
    formattedResponse ="".join(headerTuple).encode() + response_body['data']
    # print('formattedResponse: \n', formattedResponse)
    connection.sendall(formattedResponse)
    connection.close()

while 1:
    client_connection, client_addr = serverSocket.accept()
    _thread.start_new_thread(handleResponse, (client_connection,))

    

serverSocket.close()

# esse erro tá acontecendo depois de um tempo do servidor não receber nenhum request
# Unhandled exception in thread started by <function handleResponse at 0x7fd9cbc90158>
# Traceback (most recent call last):
#   File "serverTCP.py", line 126, in handleResponse
#     response_body = parseRequest(request)
#   File "serverTCP.py", line 105, in parseRequest
#     fileNameRaw = request.split('\n')[0].split(' ')[1]
# IndexError: list index out of range