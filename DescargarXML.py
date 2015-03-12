import requests
import lxml.html

class DescargarXML:
    def __init__(self, htmlSource, direccionDescarga):
        self.htmlSource=htmlSource
        self.direccionDescarga=direccionDescarga

    def obtenerEnlacesYDescargar(self):
        document=lxml.html.fromstring(self.htmlSource)
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            urlXML=img.attrib['onclick'].replace("return AccionCfdi('", "https://portalcfdi.facturaelectronica.sat.gob.mx/");
            urlXML=urlXML.replace("','Recuperacion');", "")
