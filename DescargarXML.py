import requests
import lxml.html

class DescargarXML:
    def __init__(self, htmlSource, direccionDescarga):
        self.htmlSource=htmlSource
        self.direccionDescarga=direccionDescarga

    def descargar(self):
        document=lxml.html.fromstring(self.htmlSource)
        inputValues = {}
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            print(img.attrib['onclick'])
