import traceback
import requests
from HTMLForm import HTMLForm
from DescargarXML import DescargarXML
from ParserFormatSAT import ParserFormatSAT
from Header import Header
from Utilerias import Utilerias


class PortalCfdi:

    def __init__(self, rfc, contrasena):
        self.__rfc = rfc
        self.__contrasena = contrasena
        self.__sesion = requests.Session()
        self.__directorioAGuardar = ''
        self.__header = Header()
        self.__hostCfdiau = 'cfdiau.sat.gob.mx'
        self.__hostPortalCfdi = 'portalcfdi.facturaelectronica.sat.gob.mx'
        self.__urlCfdiau = 'https://' + self.__hostCfdiau + '/'
        self.__urlPortalCfdi = 'https://' + self.__hostPortalCfdi + '/'
        self.__urlCfdiCont = ('https://cfdicontribuyentes.accesscontrol.'
                              'windows.net/')
        self.__error = ''
        self.__listaDocumentos = []

    def __entrar_pagina_inicio(self):
        url = self.__urlCfdiau + \
               '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.__sesion.post(url)

    def __enviar_formulario_ciec(self):
        url = self.__urlCfdiau + 'nidp/app/login?sid=0&sid=0'
        encabezados = self.__header.obtener(
            self.__hostCfdiau,
            self.__urlCfdiau +
            '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        )
        valoresPost = {
            'option': 'credential',
            'Ecom_User_ID': self.__rfc,
            'Ecom_Password': self.__contrasena,
            'submit': 'Enviar'
        }
        self.__sesion.post(url, data=valoresPost, headers=encabezados)

    def __leer_formulario(self, html):
        htmlFormulario = HTMLForm(html, 'form')
        inputValores = htmlFormulario.get_form_values()
        return inputValores

    def __leer_formulario_respuesta(self):
        url = self.__urlPortalCfdi
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        return self.__leer_formulario(htmlRespuesta)

    def __leer_formulario_access_control(self, valoresPost):
        url = self.__urlCfdiCont + 'v2/wsfederation'
        respuesta = self.__sesion.post(url, data=valoresPost)
        htmlRespuesta = respuesta.text
        return self.__leer_formulario(htmlRespuesta)

    def __entrar_pantalla_inicio_sistema(self, valoresPost):
        url = self.__urlPortalCfdi
        respuesta = self.__sesion.post(url, data=valoresPost)
        htmlRespuesta = respuesta.text
        return htmlRespuesta

    def __obtener_valores_post_tipo_busqueda(self, htmlFuente):
        tipo_busqueda = 'RdoTipoBusquedaReceptor'
        inputValores = self.__leer_formulario(htmlFuente)
        inputValores['ctl00$MainContent$TipoBusqueda'] = tipo_busqueda
        inputValores['__ASYNCPOST'] = 'true'
        inputValores['__EVENTTARGET'] = ''
        inputValores['__EVENTARGUMENT'] = ''
        inputValores['ctl00$ScriptManager1'] = ('ctl00$MainContent$'
                                                'UpnlBusqueda|'
                                                'ctl00$MainContent$'
                                                'BtnBusqueda')
        return inputValores

    def __seleccionar_tipo(self, htmlFuente):
        url = self.__urlPortalCfdi + 'Consulta.aspx'
        post = self.__obtener_valores_post_tipo_busqueda(htmlFuente)
        encabezados = self.__header.obtener(
            self.__hostCfdiau,
            self.__urlPortalCfdi
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text

    def __logueo_usuario_ciec(self):
        self.__entrar_pagina_inicio()
        self.__enviar_formulario_ciec()
        valoresPost = self.__leer_formulario_respuesta()

        valoresPostAccessControl = self.\
            __leer_formulario_access_control(valoresPost)

        html = self.__entrar_pantalla_inicio_sistema(valoresPostAccessControl)
        self.__seleccionar_tipo(html)

    def __entrar_consulta_receptor(self, filtros):
        url = self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        inputValores = self.__leer_formulario(htmlRespuesta)
        util = Utilerias()
        post = util.\
            mezcla_listas(inputValores, filtros.obtener_post_formulario_fechas())
        encabezados = self.__header.obtener_ajax(
            self.__hostPortalCfdi,
            self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text, inputValores

    def __obtener_valores_post_busqueda_fechas(self, htmlFuente, inputValores, filtros):
        parser = ParserFormatSAT(htmlFuente)
        valoresCambioEstado = parser.obtener_valores_formulario()
        util = Utilerias()
        temporal = util.mezcla_listas(inputValores, filtros.obtener_post())
        return util.mezcla_listas(temporal, valoresCambioEstado)

    def __consulta_receptor_fecha(self, filtros):
        url = self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        htmlRespuesta, inputValores = self.__entrar_consulta_receptor(filtros)
        valoresPost = self.__obtener_valores_post_busqueda_fechas(
            htmlRespuesta,
            inputValores,
            filtros
        )
        encabezados = self.__header.obtener_ajax(
            self.__hostPortalCfdi,
            self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(
            url,
            data=valoresPost,
            headers=encabezados
        )
        return respuesta.text

    def __consulta_receptor_folio(self, filtros):
        url = self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        inputValores = self.__leer_formulario(htmlRespuesta)
        util = Utilerias()
        valoresPost = util.mezcla_listas(inputValores, filtros.obtener_post())

        encabezados = self.__header.obtener_ajax(
            self.__hostPortalCfdi,
            self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(
            url,
            data=valoresPost,
            headers=encabezados
        )
        return respuesta.text

    def obtiene_mensaje_error(self):
        return self.__error

    def obtiene_lista_documentos_descargados(self):
        return self.__listaDocumentos

    def consultar(self, directorioAGuardar, filtros):
        try:
            self.__logueo_usuario_ciec()
            if filtros.folioFiscal != '':
                htmlRespuesta = self.__consulta_receptor_folio(filtros)
                nombre = filtros.folioFiscal
            else:
                htmlRespuesta = self.__consulta_receptor_fecha(filtros)
                nombre = ''

            xml = DescargarXML(
                self.__sesion,
                htmlRespuesta,
                directorioAGuardar
            )
            xml.obtener_enlaces_descargar(nombre)
            self.__listaDocumentos = xml.obtener_lista_documentos_descargados()
            return True
        except:
            error = traceback.format_exc()
            self.__error = error
            return False
