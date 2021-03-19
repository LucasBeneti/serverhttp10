import os
import base64

def encodeImage(fileName):
    # relativePath = 'src/images/' + fileName
    # absImagePath = os.path.abspath(relativePath)
    # print(relativePath)
    try:
        with open(relativePath,'rb') as imageFile:
            encoded_res = base64.b64encode(imageFile.read())
    except:
        print('deu ruim')
        raise Error('deu merda na imagem')
        encoded_res = ''
    finally:
        print(encoded_res)
        return encoded_res

# imagem_convertida = encodeImage('lucasAvatar.jpeg')
# print(imagem_convertida)

def testeFunc():
    raise Error('blabla')

def checkFileExistance(filePath):
    try:
        path_check = os.path.abspath(f'src/{filePath}')
        if os.path.isfile(path_check):
            print('achou file')
        else:
            testeFunc()
    except:
        print('deu ruim')

encodeImage('lucasAvatar.jpeg')