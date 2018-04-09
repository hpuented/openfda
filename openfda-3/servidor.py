import http.server
import socketserver
import http.client
import json


PORT = 6766


def lista_medicamentos():

    #Creo una lista vacía
    lista1 = []

    #Código explicado en programa1.py
    headers = {'User-Agent': 'http-client'}

    conexion = http.client.HTTPSConnection("api.fda.gov")
    conexion.request("GET", "/drug/label.json?limit=10", None, headers)

    respuesta = conexion.getresponse()
    print(respuesta.status, respuesta.reason)

    if respuesta.status == 404:
        print("Recurso no encontrado")
        exit(1)

    contenido = respuesta.read().decode("utf-8")
    conexion.close()

    informacion = json.loads(contenido)

    for i in range(len(informacion['results'])):
        medicamento = informacion['results'][i]

        if (medicamento['openfda']):
            print('El nombre del medicamento ' + str(i + 1) + ' es: ', medicamento['openfda']['substance_name'][0])
            lista1.append(medicamento['openfda']['substance_name'][0])

        else:
            print('El nombre del medicamento ' + str(i+1) + ' no esta especificado')
            lista1.append("El nombre no esta especificado")

    #Ahora "lista1" ya no está vacía, contiene el listado de los medicamentos
    return lista1


#Esta clase utiliza herencia
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    #Utilizo el método do_GET
    def do_GET(self):

        self.send_response(200)

        #Cabecera que indica que el contenido que envio al cliente es html
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        #Creo el html
        contenido = """
            <!doctype html>
            <html>
            <body style= 'background-color: orange'>
                <h1>LISTADO DE MEDICAMENTOS:</h1>
                <img src = 'https://estaticos.muyinteresante.es/media/cache/760x570_thumb/uploads/images/article/57b55f5d5cafe89bdc8b4567/medicamentos_0.jpg' >
            </body>
            </html>
        """

        #La variable "lista2" contiene la lista de los medicamentos
        lista2 = lista_medicamentos ()

        for i in lista2:
            contenido += "<ul><li>" + i + "</li></ul>" + "<br>"

        #Contesta a la petición con la inforación que tiene la variable "contenido"
        self.wfile.write(bytes(contenido, "utf8"))
        return


# ----------------------------------
# El servidor comienza a aqui
# ----------------------------------

# Establecemos como manejador nuestra propia clase
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto: ", PORT)


try:
    httpd.serve_forever()

except KeyboardInterrupt:
    print("")
    print("Servidor interrumpido por el usuario")


print("")
print("Servidor parado")

httpd.server_close()




