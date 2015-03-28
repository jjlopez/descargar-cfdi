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
        self.__directorio_guardar = ''
        self.__header = Header()
        self.__host_cfdiau = 'cfdiau.sat.gob.mx'
        self.__host_portal_cfdi = 'portalcfdi.facturaelectronica.sat.gob.mx'
        self.__url_cfdiau = 'https://' + self.__host_cfdiau + '/'
        self.__url_portal_cfdi = 'https://' + self.__host_portal_cfdi + '/'
        self.__url_cfdi_cont = ('https://cfdicontribuyentes.accesscontrol.'
                              'windows.net/')
        self.__error = ''
        self.__lista_documentos = []

    def __entrar_pagina_inicio(self):
        url = self.__url_cfdiau + \
               '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.__sesion.post(url)

    def __enviar_formulario_ciec(self):
        url = self.__url_cfdiau + 'nidp/app/login?sid=0&sid=0'
        encabezados = self.__header.obtener(
            self.__host_cfdiau,
            self.__url_cfdiau +
            '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        )
        valores_post = {
            'option': 'credential',
            'Ecom_User_ID': self.__rfc,
            'Ecom_Password': self.__contrasena,
            'submit': 'Enviar'
        }
        self.__sesion.post(url, data=valores_post, headers=encabezados)

    def __leer_formulario(self, html):
        html_formulario = HTMLForm(html, 'form')
        input_valores = html_formulario.get_form_values()
        return input_valores

    def __leer_formulario_respuesta(self):
        url = self.__url_portal_cfdi
        respuesta = self.__sesion.get(url)
        html_respuesta = respuesta.text
        return self.__leer_formulario(html_respuesta)

    def __leer_formulario_access_control(self, valores_post):
        url = self.__url_cfdi_cont + 'v2/wsfederation'
        respuesta = self.__sesion.post(url, data=valores_post)
        html_respuesta = respuesta.text
        return self.__leer_formulario(html_respuesta)

    def __entrar_pantalla_inicio_sistema(self, valores_post):
        url = self.__url_portal_cfdi
        respuesta = self.__sesion.post(url, data=valores_post)
        html_respuesta = respuesta.text
        return html_respuesta

    def __obtener_valores_post_tipo_busqueda(self, html_fuente):
        tipo_busqueda = 'RdoTipoBusquedaReceptor'
        input_valores = self.__leer_formulario(html_fuente)
        input_valores['ctl00$MainContent$TipoBusqueda'] = tipo_busqueda
        input_valores['__ASYNCPOST'] = 'true'
        input_valores['__EVENTTARGET'] = ''
        input_valores['__EVENTARGUMENT'] = ''
        input_valores['ctl00$ScriptManager1'] = ('ctl00$MainContent$'
                                                'UpnlBusqueda|'
                                                'ctl00$MainContent$'
                                                'BtnBusqueda')
        return input_valores

    def __seleccionar_tipo(self, html_fuente):
        url = self.__url_portal_cfdi + 'Consulta.aspx'
        post = self.__obtener_valores_post_tipo_busqueda(html_fuente)
        encabezados = self.__header.obtener(
            self.__host_cfdiau,
            self.__url_portal_cfdi
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text

    def __logueo_usuario_ciec(self):
        self.__entrar_pagina_inicio()
        self.__enviar_formulario_ciec()
        valores_post = self.__leer_formulario_respuesta()

        valores_post_access_ctrl = self.\
            __leer_formulario_access_control(valores_post)

        html = self.__entrar_pantalla_inicio_sistema(valores_post_access_ctrl)
        self.__seleccionar_tipo(html)

    def __entrar_consulta_receptor(self, filtros):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        html_respuesta = respuesta.text
        input_valores = self.__leer_formulario(html_respuesta)
        util = Utilerias()
        post = util.\
            mezcla_listas(input_valores, filtros.obtener_post_formulario_fechas())
        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text, input_valores

    def __obtener_valores_post_busqueda_fechas(self, htmlFuente, inputValores, filtros):
        parser = ParserFormatSAT(htmlFuente)
        valoresCambioEstado = parser.obtener_valores_formulario()
        util = Utilerias()
        temporal = util.mezcla_listas(inputValores, filtros.obtener_post())
        return util.mezcla_listas(temporal, valoresCambioEstado)

    def __consulta_receptor_fecha(self, filtros):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        htmlRespuesta, inputValores = self.__entrar_consulta_receptor(filtros)
        valoresPost = self.__obtener_valores_post_busqueda_fechas(
            htmlRespuesta,
            inputValores,
            filtros
        )
        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(
            url,
            data=valoresPost,
            headers=encabezados
        )
        return respuesta.text

    def __consulta_receptor_folio(self, filtros):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        inputValores = self.__leer_formulario(htmlRespuesta)
        util = Utilerias()
        valoresPost = util.mezcla_listas(inputValores, filtros.obtener_post())

        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
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
        return self.__lista_documentos

    def consultar(self, directorio_guardar, filtros):
        try:
            self.__logueo_usuario_ciec()
            if filtros.folio_fiscal != '':
                htmlRespuesta = self.__consulta_receptor_folio(filtros)
                nombre = filtros.folio_fiscal
            else:
                htmlRespuesta = self.__consulta_receptor_fecha(filtros)
                nombre = ''

            xml = DescargarXML(
                self.__sesion,
                htmlRespuesta,
                directorio_guardar
            )
            xml.obtener_enlaces_descargar(nombre)
            self.__lista_documentos = xml.obtener_lista_documentos_descargados()
            return True
        except:
            error = traceback.format_exc()
            self.__error = error
            return False
