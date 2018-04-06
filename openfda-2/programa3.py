import http.client
import json

headers = {'User-Agent': 'http-client'}

#Creo un bucle while
while True:

    #Creo la conexión con la página web
    conexion = http.client.HTTPSConnection("api.fda.gov")

    #Mando la petición GET, pero con un límite de 100; además, establezco que la búsqueda sea solamente del acetylsalicylic.
    conexion.request("GET", '/drug/label.json?limit=100&search=active_ingredient:"acetylsalicylic"', None, headers)

    #Creo las variables (como en programa1.py y programa2.py)
    respuesta = conexion.getresponse()

    if respuesta.status == 404:
        print("Recurso no encontrado")
        exit(1)

    contenido = respuesta.read().decode("utf-8")

    conexion.close()


    #La variable "informacion" contiene el fichero json en formato python, es decir, diccionarios, listas, etc.
    informacion = json.loads(contenido)


    for i in range (len (informacion['results'])):
        medicamento = informacion['results'][i]

        if (medicamento['openfda']):
            print('El fabricante del medicamento es: ', medicamento['openfda']['manufacturer_name'][0])

        else:
            print("El nombre del fabricante no está disponible")
    #Rompo el bucle while
    break





