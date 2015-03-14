import requests
import lxml.html

class DescargarXML:
    def __init__(self, sesion, htmlSource, direccionDescarga):
        self.__sesion=sesion
        self.__htmlSource=htmlSource
        self.__direccionDescarga=direccionDescarga
        self.__listaXML = []

    def obtenerEnlacesYDescargar(self):
        i=1
        document=lxml.html.fromstring(self.__htmlSource)
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            urlXML=img.attrib['onclick'].replace("return AccionCfdi('", "https://portalcfdi.facturaelectronica.sat.gob.mx/");
            urlXML=urlXML.replace("','Recuperacion');", "")
            nombre = str(i)+'.xml'
            self.__descargarXML(urlXML, nombre)
            i+=1
            self.__listaXML.append(self.__direccionDescarga + nombre)

    def obtenerListaDeDocumentosDescargados(self):
        return self.__listaXML

    def __descargarXML(self, urlXML, name):
        with open(self.__direccionDescarga + name , 'wb') as handle:
            response = self.__sesion.get(urlXML, stream=True)
            if not response.ok:
                pass

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
