import requests
import lxml.html

class DescargarXML:
    def __init__(self, sesion, htmlSource, direccionDescarga):
        self.sesion=sesion
        self.htmlSource=htmlSource
        self.direccionDescarga=direccionDescarga

    def obtenerEnlacesYDescargar(self):
        i=1
        document=lxml.html.fromstring(self.htmlSource)
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            urlXML=img.attrib['onclick'].replace("return AccionCfdi('", "https://portalcfdi.facturaelectronica.sat.gob.mx/");
            urlXML=urlXML.replace("','Recuperacion');", "")
            self.descargarXML(urlXML, str(i)+'.xml')
            i+=1

    def descargarXML(self, urlXML, name):
        with open(self.direccionDescarga + name , 'wb') as handle:
            response = self.sesion.get(urlXML, stream=True)
            if not response.ok:
                pass

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
