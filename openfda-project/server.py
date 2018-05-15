
import http.server
import http.client
import json
import socketserver

PORT=8000

#Clase que utiliza herencia
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    url_openfda = "api.fda.gov"
    medicina_openfda = "/drug/label.json"
    active_ingredient_openfda = "&search=active_ingredient:"
    manufacturer_name_openfda = "&search=openfda.manufacturer_name:"

    #Creo una función con la página web principal
    def pagina_principal(self):
        web = """
            <html>
                <head>
                    <title>OPENFDA </title>
                </head>
                <body style= 'background-color: orange'>
                    <h1>OPCIONES DISPONIBLES: </h1>
                    <form method="get" action="listDrugs">
                        <input type = "submit" value="Drug List">
                        </input>
                    </form>
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    <form method="get" action="searchDrug">
                        <input type = "submit" value="Drug Search">
                        <input type = "text" name="drug"></input>
                        </input>
                    </form>
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    <form method="get" action="listCompanies">
                        <input type = "submit" value="Company List">
                        </input>
                    </form>
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    <form method="get" action="searchCompany">
                        <input type = "submit" value="Company Search">
                        <input type = "text" name="company"></input>
                        </input>
                    </form>
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    <form method="get" action="listWarnings">
                        <input type = "submit" value="Warnings List">
                        </input>
                    </form>
                    <img src = 'https://lasaludmovil.files.wordpress.com/2014/06/openfda_logo.jpg?w=640' >
                </body>
            </html>
                """
        return web

    #Creo otra función llamada "página_secundaria"
    def pagina_secundaria(self, lista):
        web2 = """
            <html>
                <head>
                    <title>OPENFDA </title>
                </head>
                <body style= 'background-color: pink'>
                    <ul>
                """
        #Recibe una lista de información con la que genera el html
        for i in lista:
            web2 += "<li>" + i + "</li>"

        web2 += """
                     </ul>
                </body>
             </html>
                """
        return web2


    def openfda_informacion(self, limit=10):

        #Creo la conexión con la página web
        conexion = http.client.HTTPSConnection(self.url_openfda)

        #Mando la petición GET para que la página web me devuelva la información
        conexion.request("GET", self.medicina_openfda + "?limit="+str(limit))

        #Creo la variable "respuesta", que contiene la respuesta de openfda
        respuesta = conexion.getresponse()

        #Creo la variable "contenido", que lee el contenido de la respuesta de openfda en json
        #y lo decodifico para que se interpreten todos los caracteres
        contenido = respuesta.read().decode("utf8")

        #La variable "informacion" contiene el fichero json en formato python, es decir, diccionarios, listas, etc.
        informacion = json.loads(contenido)

        resultados = informacion['results']
        return resultados


    #Utilizo el método GET
    def do_GET(self):

        #Separo la url por el signo "?" gracias a split
        recurso = self.path.split("?")
        if len(recurso) > 1:
            parametros = recurso[1]
        else:
            parametros = ""

        #Establezco este limite por defecto, que es el numero de resultados que apareceran
        limit = 1


        if parametros:
            #Utilizo de nuevo el split, pero en este caso separo por "="
            limite = parametros.split("=")
            if limite[0] == "limit":
                #Cambio el valor por defecto del limite (1) y convierto a entero el numero, que era tipo str
                limit = int(limite[1])

        else:
            print("No hay parámetros")



        #A continuación se muestran los 5 recursos

        if self.path == '/':

            self.send_response(200)
            #Cabecera que indica que el tipo de contenido que envio al cliente es html
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #Llamo a la primera función, que crea la página web
            html = self.pagina_principal()
            self.wfile.write(bytes(html, "utf8"))


        elif 'listDrugs' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #Creo una lista vacía
            farmacos = []

            #Llamo a la función que establece la conexión con openfda y me devuelve la información
            resultados = self.openfda_informacion(limit)


            for resultado in resultados:
                if ('generic_name' in resultado['openfda']):
                    #Añado los medicamentos a la lista vacía, con append
                    farmacos.append (resultado['openfda']['generic_name'][0])

                else:
                    #En el caso de no estar los medicamentos, añado que el nombre no está especificado
                    farmacos.append('El nombre no esta especificado')

            #Llama a la función "pagina_secundaria" y crea la pagina con los medicamentos de la lista "farmacos"
            pagina_html = self.pagina_secundaria(farmacos)
            self.wfile.write(bytes(pagina_html, "utf8"))


        #Mismo código que en el "elif" anterior
        elif 'listCompanies' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            empresas = []

            resultados = self.openfda_informacion(limit)

            for resultado in resultados:
                if ('manufacturer_name' in resultado['openfda']):
                    empresas.append (resultado['openfda']['manufacturer_name'][0])
                else:
                    empresas.append('No se conoce el nombre de la empresa')

            pagina_html = self.pagina_secundaria(empresas)
            self.wfile.write(bytes(pagina_html, "utf8"))


        elif 'searchDrug' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #EStablezco un limite por defecto, 10 en este caso
            limit = 10

            #Separo por "=", para obtener el nombre del medicamento, que está en la posición 1
            drug = self.path.split('=')[1]

            #Creo una lista vacia
            lista_medicamentos = []

            #Establezco la conexión con openfda
            conexion = http.client.HTTPSConnection(self.url_openfda)
            #Utilizo el método GET
            conexion.request("GET", self.medicina_openfda + "?limit="+str(limit) + self.active_ingredient_openfda + drug)

            #Respuesta de openfda
            respuesta = conexion.getresponse()
            #Decodifico para que se interpreten todos los caracteres
            contenido = respuesta.read().decode("utf8")

            #Convierto el fichero json en formato python
            informacion = json.loads(contenido)
            medicamentos = informacion['results']

            for resultado in medicamentos:
                if ('active_ingredient' in resultado['openfda']):
                    lista_medicamentos.append(resultado['openfda']['active_ingredient'][0])
                else:
                    lista_medicamentos.append('Desconocido')

            #Llamo a la función "pagina_secundaria" para crear la pagina html
            resultado_html = self.pagina_secundaria(lista_medicamentos)
            self.wfile.write(bytes(resultado_html, "utf8"))


        #Codigo similar al anterior
        elif 'searchCompany' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            limit = 10

            company = self.path.split('=')[1]

            lista_empresa = []

            conexion = http.client.HTTPSConnection(self.url_openfda)
            conexion.request("GET", self.medicina_openfda + "?limit=" + str(limit) + self.manufacturer_name_openfda + company)

            respuesta = conexion.getresponse()
            contenido = respuesta.read().decode("utf8")

            informacion = json.loads(contenido)
            medicamento = informacion['results']

            for resultado in medicamento:
                lista_empresa.append(resultado['openfda']['manufacturer_name'][0])

            resultado_html = self.pagina_secundaria(lista_empresa)
            self.wfile.write(bytes(resultado_html, "utf8"))


        #Extensiones

        elif 'listWarnings' in self.path:

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            advertencias = []

            #Llama a la función "openfda_informacion"
            resultados = self.openfda_informacion(limit)

            for resultado in resultados:
                if ('warnings' in resultado):
                    advertencias.append (resultado['warnings'][0])
                else:
                    advertencias.append('No especificado')

            resultado_html = self.pagina_secundaria(advertencias)
            self.wfile.write(bytes(resultado_html, "utf8"))




        #"redirect" me devuelve la página principal
        elif 'redirect' in self.path:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()


        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        #Si no tengo ninguno de los recursos anteriores, se envia este error
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Recurso incorrecto '{}'.".format(self.path).encode())
        return


#Aqui comienza el servidor

#Me permite utilizar el puerto 8000 siempre
socketserver.TCPServer.allow_reuse_address= True

#Manejador
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto: ", PORT)
httpd.serve_forever()