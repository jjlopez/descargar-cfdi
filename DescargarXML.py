import lxml.html


class DescargarXML:

    def __init__(self, sesion, html_source, direccion_descarga):
        self.__sesion = sesion
        self.__html_source = html_source
        self.__direccion_descarga = direccion_descarga
        self.__lista_xml = []

    def obtener_enlaces_descargar(self, nombre_default=''):
        i = 1
        document = lxml.html.fromstring(self.__html_source)
        for img in document.xpath('//img[@class="BtnDescarga"]'):
            url_xml = img.attrib['onclick'].replace(
                "return AccionCfdi('",
                "https://portalcfdi.facturaelectronica.sat.gob.mx/"
            )
            url_xml = url_xml.replace("','Recuperacion');", "")
            if nombre_default != '':
                nombre = nombre_default+'.xml'
            else:
                nombre = str(i) + '.xml'
            self.__descargar_xml(url_xml, nombre)
            i += 1
            self.__lista_xml.append(self.__direccion_descarga + nombre)

    def get_lista_documentos_descargados(self):
        return self.__lista_xml

    def __descargar_xml(self, url_xml, nombre):
        with open(self.__direccion_descarga + nombre, 'wb') as handle:
            response = self.__sesion.get(url_xml, stream=True)
            if not response.ok:
                pass

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
