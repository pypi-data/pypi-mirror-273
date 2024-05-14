#Imports necesarios para las funciones de la libreria
import requests
from fastapi.responses import JSONResponse

#Metodo de prueba para el despliege de la libreria
def hola_journey():
    print('Holitaa, esta es una librería diseñada y publicada por JourneyGen.')



#Implementacion de las funciones necesarias para la libreria
"""
METODO INSERTAR HISTORICO
Descripcion: Inserta un nuevo par de mensajes a la bd de CASH
"""
def ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado, url='http://ismi.fi.upm.es:8080/insertar/chat'):
    
    datos_post = { # Formato con el que se consume la api
        'id_usuario': usr,
        'num_chat': num_chat,
        'contexto': contexto,
        'lista_msg': lista_msg,
        'tipoIA': tipoIA,
        'cerrado': cerrado
    }
    response = requests.post(url, json=datos_post)

    return JSONResponse(content=response.json(), status_code=response.status_code)

def get_historico_falso(usr, url='http://farlier.org:5000/chat/obtener'):

    datos_post = {
        'usr': usr
    }
    response = requests.post(url, json=datos_post)

    return {'respuesta': response.json(), 'codigo': response.status_code}

def ins_historico_falso(usr, msgs, url='http://farlier.org:5000/chat/insertar'):

    datos_post = {
        'usr': usr,
        'msgs': msgs
    }
    response = requests.post(url, json=datos_post)

    return {'respuesta': response.json(), 'codigo': response.status_code}