import http.client
import json


headers = {'User-Agent': 'http-client'}

#Creo la conexion con la página web
conexion = http.client.HTTPSConnection("api.fda.gov")

#Mando la petición GET para que la página web me devuelva la información,
#pero esta vez solo quiero que me devuelva la información de 10 medicamentos (limit=10)
conexion.request("GET", "/drug/label.json?limit=10", None, headers)

#Creo la variable llamada "respuesta", que contiene la respuesta de openfda
respuesta = conexion.getresponse()

if respuesta.status == 404:
    print("Recurso no encontrado")
    exit(1)

#Creo la variable "contenido", que lee el contenido de la respuesta de openfda y lo decodifico en utf-8
#(al igual que en programa1.py)
contenido = respuesta.read().decode("utf-8")


conexion.close()



#La variable "informacion" contiene el fichero json en formato python, es decir, diccionarios, listas, etc.
informacion = json.loads(contenido)


for i in range (len (informacion['results'])):
    medicamento = informacion['results'][i]

    print ('El ID del medicamento ' + str(i + 1) + ' es: ',medicamento['id'])


