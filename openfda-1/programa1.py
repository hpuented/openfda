import http.client
import json


headers = {'User-Agent': 'http-client'}

#Creo la conexión con la página web
conexion = http.client.HTTPSConnection("api.fda.gov")

#Mando la petición GET para que la página web me devuelva la información
conexion.request("GET", "/drug/label.json", None, headers)

#Creo la variable llamada "respuesta", que contiene la respuesta de openfda
respuesta = conexion.getresponse()

if respuesta.status == 404:
    print("Recurso no encontrado")
    exit(1)

#Creo la variable "contenido", que lee el contenido de la respuesta de openfda en json
#y lo decodifico para que se interpreten todos los caracteres
contenido = respuesta.read().decode("utf-8")


conexion.close()



#La variable "informacion" contiene el fichero json en formato python, es decir, diccionarios, listas, etc.
informacion = json.loads(contenido)


medicamento = informacion['results'][0]

#Imprimo la información
print('El ID del medicamento es: ',medicamento['id'])
print('El proposito es: ',medicamento['purpose'][0])

print('El fabricante es: ',medicamento['openfda']['manufacturer_name'][0])