La librería ofrece el método **ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)** que inserta un nuevo par de mensajes a la base de datos de CASH. Para ello, se realiza una
petición de inserción a dicha base de datos cuyos parámetros corresponden a los
argumentos de la función.

**Parámetros:**
    

- usr (str): El usuario.

- num_chat (int): Número de chat.

- contexto (str): Contexto del chat.

- lista_msg (json): Un JSON enviado por BS con una lista de {"role": "user", "content": userMsg.msg} donde "role" puede ser system, user o assistant y content el contexto la pregunta y la respuesta respectivamente.

- tipoIA (enum): Un enumerado que puede ser PASADO, PRESENTE, FUTURO, COMPRA.

- cerrado (boolean): Un booleano que indica si el chat está cerrado o no.

**POST:**

JSONResponse: Respuesta de la petición POST a la API de CASH (Backend)

def ins_historico(usr, num_chat, contexto, lista_msg, tipoIA, cerrado)


Para instalar esta librería basta con pip install journeylib.

Es posible encontrar la librería en PyPi en el siguiente link: https://pypi.org/project/journeylib/