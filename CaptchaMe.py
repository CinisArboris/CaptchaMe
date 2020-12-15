import pytesseract
import urllib.parse
import base64
import PIL
import io
import requests
import time

class CaptchaMe:
	origenURL = ''
	tierra = ''
	marlo = ''
	fila = ''
	columna = ''
	nombreImagen = ''
	imagenPNG = 0
	imagenDato = 0
	llave = ''
	mazorca = ''

	def __init__ (self, origenURL, nombreImagen):
		self.origenURL = origenURL
		self.nombreImagen = nombreImagen
		print ('Iniciar..........ok \n')

	def cargar(self):
		#print ('nombreImagen', self.nombreImagen)
		self.imagenPNG = PIL.Image.open(self.nombreImagen)
		self.imagenDato = self.imagenPNG.load()
		self.fila = self.imagenPNG.size[0]
		self.columna = self.imagenPNG.size[1]
		print ('Cargar...........ok \n')

	def limpiarPuntos(self):
		tiempoA = time.time()
		fila = 0
		columna = 0
		#print (self.fila, self.columna)
		while (fila < self.fila):
			columna = 0
			while (columna < self.columna):
				if (self.imagenDato[fila,columna] == (0, 0, 0)):
					self.imagenDato[fila,columna] = (255, 255, 255)
				columna = columna + 1
			fila = fila + 1
		self.imagenPNG.save(self.nombreImagen)
		self.imagenPNG.close()
		tiempoB = time.time()
		print ('limpiarPuntos.....ok   ', 'Tiempo limpiarPuntos', self.fila, self.columna, tiempoB - tiempoA)

	def colar(self):
		tiempoA = time.time()
		pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files (x86)\Tesseract-OCR\tesseract')
		#print (pytesseract.image_to_string(PIL.Image.open('image.png')))
		self.llave = pytesseract.image_to_string(PIL.Image.open('image.png'))
		tiempoB = time.time()
		print ('colar.....ok   ', 'Tiempo colar', self.fila, self.columna, tiempoB - tiempoA)

	def procesar(self):
		tiempoA = time.time()
		print ('origenURL', '\n', self.origenURL, '\n')
		self.tierra = requests.Session()	#objeto
		#respuesta / objeto
		self.mazorca = self.tierra.get(self.origenURL)
		print ('mazorca Content', '\n', self.mazorca.content, '\n')
		galleta = self.mazorca.cookies
		print ('mazorca Galleta', '\n', galleta, '\n')
		
		self.marlo = self.mazorca.content
		self.marlo = self.marlo.split()
		self.marlo = self.marlo[10]
		self.marlo = str(self.marlo)[29:(len(self.marlo)-1)] + '====='
		#print ('marlo INFO', '\n', self.marlo[:200], '\n')
		
		imagen = PIL.Image.open(io.BytesIO(base64.b64decode(self.marlo)))
		imagen.save("image.png")
		
		self.cargar()
		self.limpiarPuntos()
		self.colar()
		
		valores = {'cametu':self.llave}
		self.mazorca = self.tierra.post(self.origenURL, valores)
		
		print ('mazorca Content', '\n', self.mazorca.content, '\n')
		galleta = self.mazorca.cookies
		print ('mazorca Galleta', '\n', galleta, '\n')
		
		print ('url', '\n', self.mazorca.url + '\n')
		print ('llave', self.llave)
		tiempoB = time.time()
		
		print ('procesar.....ok   ', 'Tiempo procesar', self.fila, self.columna, tiempoB - tiempoA)

test = 'http://challenge01.root-me.org/programmation/ch8/';
cm = CaptchaMe('#',
	'image.png')
cm.procesar()




