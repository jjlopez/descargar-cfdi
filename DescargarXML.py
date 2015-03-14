import requests
import lxml.html

class DescargarXML:
    def __init__(self, sesion, htmlSource, direccionDescarga):
        self.sesion=sesion
        self.htmlSource=htmlSource
        self.direccionDescarga=direccionDescarga
        self.__listaXML = []

    def obtenerEnlacesYDescargar(self):
        i=1
        document=lxml.html.fromstring(self.htmlSource)
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            urlXML=img.attrib['onclick'].replace("return AccionCfdi('", "https://portalcfdi.facturaelectronica.sat.gob.mx/");
            urlXML=urlXML.replace("','Recuperacion');", "")
            nombre = str(i)+'.xml'
            self.__descargarXML(urlXML, nombre)
            i+=1
            self.__ListaXML.append(nombre)

    def __descargarXML(self, urlXML, name):
        with open(self.direccionDescarga + name , 'wb') as handle:
            response = self.sesion.get(urlXML, stream=True)
            if not response.ok:
                pass

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
