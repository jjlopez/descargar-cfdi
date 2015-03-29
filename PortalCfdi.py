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

    def __entra_consulta_receptor(self, filtros):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        html_respuesta = respuesta.text
        input_valores = self.__leer_formulario(html_respuesta)
        util = Utilerias()
        post = util.\
            mezcla_listas(
                input_valores,
                filtros.obtener_post_formulario_fechas()
            )
        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text, input_valores

    def __obtener_valores_post_busqueda_fechas(self, html, inputs, filtros):
        parser = ParserFormatSAT(html)
        valores_cambio_estado = parser.obtener_valores_formulario()
        util = Utilerias()
        temporal = util.mezcla_listas(inputs, filtros.obtener_post())
        return util.mezcla_listas(temporal, valores_cambio_estado)

    def __consulta_receptor_fecha(self, filtros):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        html_respuesta, input_valores = self.__entra_consulta_receptor(filtros)
        valores_post = self.__obtener_valores_post_busqueda_fechas(
            html_respuesta,
            input_valores,
            filtros
        )
        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(
            url,
            data=valores_post,
            headers=encabezados
        )
        return respuesta.text

    def __consulta_receptor_folio(self, fltrs):
        url = self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        html_respuesta = respuesta.text
        input_valores = self.__leer_formulario(html_respuesta)
        util = Utilerias()
        valores_post = util.mezcla_listas(input_valores, fltrs.obtener_post())

        encabezados = self.__header.obtener_ajax(
            self.__host_portal_cfdi,
            self.__url_portal_cfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(
            url,
            data=valores_post,
            headers=encabezados
        )
        return respuesta.text

    def error(self):
        return self.__error

    def lista_cfdis(self):
        return self.__lista_documentos

    def consultar(self, directorio_guardar, filtros):
        try:
            self.__logueo_usuario_ciec()
            if filtros.folio_fiscal != '':
                html_respuesta = self.__consulta_receptor_folio(filtros)
                nombre = filtros.folio_fiscal
            else:
                html_respuesta = self.__consulta_receptor_fecha(filtros)
                nombre = ''

            xml = DescargarXML(
                self.__sesion,
                html_respuesta,
                directorio_guardar
            )
            xml.obtener_enlaces_descargar(nombre)
            self.__lista_documentos = xml.get_lista_documentos_descargados()
            return True
        except:
            error = traceback.format_exc()
            self.__error = error
            return False
