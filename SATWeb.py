import requests
import lxml.html

class SATWeb:
    def __init__(self, rfc, contrasena):
        self.rfc = rfc
        self.contrasena = contrasena
        self.sesion = s = requests.Session()

    def __entrarAlaPaginaInicio(self):
        url = 'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.sesion.post(url)
