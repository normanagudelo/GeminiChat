import os
import requests
import json
from datetime import datetime

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=*poner aqui la key API de gemini para desarrollo"

headers = {
    'Content-Type': 'application/json',
}

# Obtener el directorio actual
directorio_actual = os.getcwd()

# Solicitar al usuario un nombre para la conversación
nombre_conversacion = input("Nombre de la conversación actual o anterior: ")

# Verificar si se ingresó un nombre
if not nombre_conversacion:
    # Si no se ingresó un nombre, asignar la fecha de hoy como nombre
    nombre_conversacion = datetime.now().strftime("%Y%m%d%H%M%S")

# Crear la ruta completa utilizando el directorio actual y el nombre de la conversación
ruta_conversacion = os.path.join(directorio_actual, nombre_conversacion)

# Imprimir el nombre de la conversación
print("Nombre de la conversacion:", nombre_conversacion)
print("Ruta de respaldo del chat", ruta_conversacion)

while True:
    consulta = input("<USUARIO>: ")

    if consulta.lower() == "salir":
        print("Saliendo del programa. Sugerencias escribir a normanagudelo@gmail.com")
        break  # Sale del bucle while

    # Adicionar la consulta al contenido del archivo
    with open(ruta_conversacion, 'a') as archivo:
        archivo.write(f'Tu: {consulta}\n')

    # Leer el archivo y crear el string textoPre
    with open(ruta_conversacion, 'r') as archivo_lectura:
        ConsultaFinal = archivo_lectura.read()

    data = {
        'contents': [
            {
                'parts': [
                    {'text': ConsultaFinal}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        try:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            print('<GeminiChat>:'+ generated_text)

            # Adicionar la respuesta al contenido del archivo
            with open(ruta_conversacion, 'a') as archivo:
                archivo.write(f'{generated_text}\n\n')

        except KeyError:
            print("La estructura de la respuesta no es la esperada.")
    else:
        print(f"Error en la solicitud: {response.status_code} - {response.text}")
