# !/usr/bin/env python3
# ## ###############################################
#
# webserver.py
# Starts a custom webserver and handles all requests
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################



import os
import sys
import json
import magic
import urllib.request
import threading
from proyecto import focos, dimmer_start,get_timbre,tiempo
from http.server import BaseHTTPRequestHandler, HTTPServer
# import time
# import time

status_camara1=1
status_camara2=1
bandera=0
bandera2=0
# Nombre o dirección IP del sistema anfitrión del servidor web
# address = "localhost"
address = "192.168.40.57"
# Puerto en el cual el servidor estará atendiendo solicitudes HTTP
# El default de un servidor web en produción debe ser 80
port = 8080

class WebServer(BaseHTTPRequestHandler):

	"""Sirve cualquier archivo encontrado en el servidor"""
	def _serve_file(self, rel_path):
		if not os.path.isfile(rel_path):
			self.send_error(404)
			return
		self.send_response(200)
		mime = magic.Magic(mime=True)
		self.send_header("Content-type", mime.from_file(rel_path))
		self.end_headers()
		with open(rel_path, 'rb') as file:
			self.wfile.write(file.read())


	"""Sirve el archivo de interfaz de usuario"""
	def _serve_ui_file(self):
		if not os.path.isfile("smarthome.html"):
			err = "user_interface.html not found."
			self.wfile.write(bytes(err, "utf-8"))
			print(err)
			return
		try:
			with open("smarthome.html", "r") as f:
				content = "\n".join(f.readlines())
		except:
			content = "Error reading smarthome.html"
		self.wfile.write(bytes(content, "utf-8"))

	def _parse_post(self, json_obj):
		if not 'action' in json_obj or not 'value' in json_obj:
			return
		switcher = {
			'foco'    : focos,
			'dimmer'  : dimmer_start,
			'programado': tiempo
		}
		func = switcher.get(json_obj['action'], None)
		if func:
			print('\tCall{}({})'.format(func, json_obj['value']))
			func(json_obj['value'])
			
	"""do_GET controla todas las solicitudes recibidas vía GET, es
	decir, páginas. Por seguridad, no se analizan variables que lleguen
	por esta vía"""
	def do_GET(self):
		# Revisamos si se accede a la raiz.
		# En ese caso se responde con la interfaz por defecto
		if self.path == '/':
			html='''
				<html>
				<head>
				<meta charset="UTF-8">
				<meta name="viewport" content="width=device-width, user-scalable=no,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0">
				<title> Smart Home</title>
				<link  href="style.css" rel="stylesheet" type="text/css" >
				<title>Temperature - Raspberry Pi Martínez Rojas José Eduardo</title>
				</head>
				<body>
				<h1> Smart Home </h1>
				<div>
				<p id="text" style="display:none">Alguien toca el timbre!</p>
				</div>
			
				<button class="accordion">Section Foco ON/OFF</button>
				<div class="panel">
				<div>
				<p> Foco encendido apagado</p> </div>
				<div>
				<label class="switch">
				<input type="checkbox" id="myCheck" onclick="myFunction()">
				<span class="slider round"></span>
				</label>
				</div>
				</div>
				
				<button class="accordion">Dimmer Foco</button>
				<div class="panel">
				<div>
				Ingresa el porcentaje de intesidad(0-100):
				<input type="text" id="fullName" name="fullName" value="">

				<button class="widebutton" onclick="handle(this, 'dimmer', 10)"> Submit</button>
				</div>
				</div>
				
				<button class="accordion">Foco programado</button>
				<div class="panel">
				<div>
				<label for="Ingresa Hora"> Start date:</label>
				<input id=hora type="time" name="hora" min="00:00" max="23:59" step="3600" >
				<div>
				<p></p>
				&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
				<button class="buttongreen"  onclick="handle(this, 'programado', 300)" > ON </button>
				<button class="buttonred"  onclick="handle(this, 'programado', 301)" > OFF </button>
				</div>
				
				
				
				</div>
				</div>
				
				
				<button class="accordion">Timbre</button>
				<div class="panel">
				<div id="hola">
				<div id="timbre" onmousemove="myFunction4({})">Timbrea
				</div>
				</div>
				</div>
				
				
				<button class="accordion" >Camaras</button>
				<div class="panel">
				<div id="camara1" onmousemove="camara({})"> Camara1
				<div>
				<a href=http://192.168.1.220:4747/video> Link_Camara1</a>
				</div>
				<div>
					<iframe width="720" height="480"  src="http://192.168.1.220:4747/video" frameborder="0" allowfullscreen="allowfullscreen"> </iframe>
				</div>
				</div>
				
				<div id="camara2" onmousemove="camara2({})">  Camara
				<div>
				<a href=http://192.168.1.219:4747/video> Link_Camara2 </a>
				</div>
				<div>
					<iframe width="720" height="480"  src="http://192.168.1.219:4747/video" frameborder="0" allowfullscreen="allowfullscreen"> </iframe>
				</div>
				</div>
				</div>
				<button class="accordion">Puerta Garaje </button>
				<div class="panel">
				<div>
				<p> Puerta Abierta Cerrada</p> </div>
				<div>
				<label class="switch">
                
				<input type="checkbox" id="myCheck2" onclick="myFunctionDoor(this)" value="Ocultar">
                <span class="slider round"></span>
				</label>
                <center>
                <img src="doorclose.jpeg" id="img">
                <center/>
				</div>
                
				</div>
                
				<script  src="jquery.js"></script>
				<script type="text/javascript" src="index.js"></script>
				
                </body>

				</html>
				
			'''
			# 200 es el código de respuesta satisfactorio (OK)
			# de una solicitud
			self.send_response(200)
			# La cabecera HTTP siempre debe contener el tipo de datos mime
			# del contenido con el que responde el servidor
			self.send_header("Content-type", "text/html")
			# Fin de cabecera
			self.end_headers()
			timbre=get_timbre()
			global status_camara1	
			global status_camara2

			self.wfile.write(html.format(timbre,status_camara1,status_camara2).encode("utf-8"))
			# Por simplicidad, se devuelve como respuesta el contenido del
			# archivo html con el código de la página de interfaz de usuario
			
		# En caso contrario, se verifica que el archivo exista y se sirve
		else:
			self._serve_file(self.path[1:])



	"""do_POST controla todas las solicitudes recibidas vía POST, es
	decir, envíos de formulario. Aquí se gestionan los comandos para
	la Raspberry Pi"""
	def do_POST(self):
		# Primero se obtiene la longitud de la cadena de datos recibida
		content_length = int(self.headers.get('Content-Length'))
		if content_length < 1:
			return
		# Después se lee toda la cadena de datos
		post_data = self.rfile.read(content_length)
		# Finalmente, se decodifica el objeto JSON y se procesan los datos.
		# Se descartan cadenas de datos mal formados
		try:
			jobj = json.loads(post_data.decode("utf-8"))
			self._parse_post(jobj)
		except:
			print(sys.exc_info())
			print("Datos POST no recnocidos")
def getData():
		global status_camara1	
		global status_camara2
		global bandera
		global bandera2
		try:
			if(bandera==0):
				status_camara1=urllib.request.urlopen("http://192.168.1.220:4747/video").getcode()
				bandera=1
				print(status_camara1)
		except:
			status_camara1=0
			pass
		try:
			if(bandera2==0):
				status_camara2=urllib.request.urlopen("http://192.168.1.219:4747/video").getcode()
				bandera2=1
		except:
			status_camara2=0
			pass
			
def main():
	# Inicializa una nueva instancia de HTTPServer con el
	# HTTPRequestHandler definido en este archivo
	webServer = HTTPServer((address, port), WebServer)
	print("Servidor iniciado")
	print ("\tAtendiendo solicitudes en http://{}:{}".format(
		address, port))

	try:
		dataCollector = threading.Thread(target= getData, args =())
		dataCollector.start() #comienze el hilo
		# Mantiene al servidor web ejecutándose en segundo plano
		webServer.serve_forever()
		dataCollector.join()# esperar hasta que matemos el hilo
	except KeyboardInterrupt:
		# Maneja la interrupción de cierre CTRL+C
		pass
	except:
		print(sys.exc_info())
	# Detiene el servidor web cerrando todas las conexiones
	webServer.server_close()
	# Reporta parada del servidor web en consola
	print("Server stopped.")


# Punto de anclaje de la función main
if __name__ == "__main__":
	main()
