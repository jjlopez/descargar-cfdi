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
        self.__directorioAGuardar=''
        self.__header = Header()
        self.__hostCfdiau = 'cfdiau.sat.gob.mx'
        self.__hostPortalCfdi = 'portalcfdi.facturaelectronica.sat.gob.mx'
        self.__urlCfdiau = 'https://' + self.__hostCfdiau + '/'
        self.__urlPortalCfdi = 'https://' + self.__hostPortalCfdi + '/'
        self.__urlCfdiCont='https://cfdicontribuyentes.accesscontrol.windows.net/'
        self.__error = ''

    def __entrarAlaPaginaInicio(self):
        url = self.__urlCfdiau + '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.__sesion.post(url)

    def __enviarFormularioConCIEC(self):
        url = self.__urlCfdiau + 'nidp/app/login?sid=0&sid=0'
        encabezados = self.__header.obtener(
            self.__hostCfdiau,
            self.__urlCfdiau +
            '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        )
        valoresPost = {
            'option':'credential',
            'Ecom_User_ID':self.__rfc,
            'Ecom_Password':self.__contrasena,
            'submit':'Enviar'
        }
        self.__sesion.post(url, data=valoresPost, headers=encabezados)

    def __leerFormulario(self, html):
        htmlFormulario = HTMLForm(html, 'form')
        inputValores = htmlFormulario.getFormValues()
        return inputValores

    def __leerFormularioDeRespuesta(self):
        url = self.__urlPortalCfdi
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        return self.__leerFormulario(htmlRespuesta)

    def __leerFormularioDeAccessControl(self, valoresPost):
        url = self.__urlCfdiCont + 'v2/wsfederation'
        respuesta = self.__sesion.post(url, data=valoresPost)
        htmlRespuesta = respuesta.text
        return self.__leerFormulario(htmlRespuesta)

    def __entrarAPantallaInicioSistema(self, valoresPost):
        url = self.__urlPortalCfdi
        respuesta = self.__sesion.post(url, data=valoresPost)
        htmlRespuesta = respuesta.text
        return htmlRespuesta

    def __obtenerValoresPostDelTipoDeBusqueda(self, htmlFuente):
        inputValores = self.__leerFormulario(htmlFuente)
        inputValores['ctl00$MainContent$TipoBusqueda'] = 'RdoTipoBusquedaReceptor'
        inputValores['__ASYNCPOST'] = 'true'
        inputValores['__EVENTTARGET'] = ''
        inputValores['__EVENTARGUMENT'] = ''
        inputValores['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|ctl00$MainContent$BtnBusqueda'
        return inputValores


    def __seleccionarTipo(self, htmlFuente):
        url = self.__urlPortalCfdi + 'Consulta.aspx'
        post = self.__obtenerValoresPostDelTipoDeBusqueda(htmlFuente)
        encabezados = self.__header.obtener(
            self.__hostCfdiau,
            self.__urlPortalCfdi
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text

    def __logueoDeUsuarioConCIEC(self):
        self.__entrarAlaPaginaInicio()
        self.__enviarFormularioConCIEC()
        valoresPost = self.__leerFormularioDeRespuesta()
        valoresPostAccessControl = self.__leerFormularioDeAccessControl(valoresPost)
        html = self.__entrarAPantallaInicioSistema(valoresPostAccessControl)
        self.__seleccionarTipo(html)

    def __entrarConsultaReceptor(self, filtros):
        url = self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        respuesta = self.__sesion.get(url)
        htmlRespuesta = respuesta.text
        inputValores = self.__leerFormulario(htmlRespuesta)
        util = Utilerias()
        post = util.mergeListas(inputValores, filtros.obtenerPOSTFormularioFechas())
        encabezados = self.__header.obtenerAJAX(
            self.__hostPortalCfdi,
            self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.__sesion.post(url, data=post, headers=encabezados)
        return respuesta.text, inputValores

    def __obtenerValoresPostBusquedaFechas(self, htmlFuente, inputValores, filtros):
        parser = ParserFormatSAT(htmlFuente)
        valoresCambioEstado = parser.obtenerValoresFormulario()
        util = Utilerias()
        temporal = util.mergeListas(inputValores, filtros.obtenerPOST())
        return util.mergeListas(temporal, valoresCambioEstado)
 
    def __consultaReceptorFecha(self, filtros):
        url = self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        htmlRespuesta, inputValores = self.__entrarConsultaReceptor(filtros)
        valoresPost = self.__obtenerValoresPostBusquedaFechas(
            htmlRespuesta,
            inputValores,
            filtros
        )
        encabezados = self.__header.obtenerAJAX(
            self.__hostPortalCfdi,
            self.__urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta=self.__sesion.post(url, data=valoresPost, headers=encabezados)
        return respuesta.text

    def obtieneMensajeError(self):
        return self.__error

    def consultar(self, directorioAGuardar, filtros):
        try:
            self.__logueoDeUsuarioConCIEC()
            htmlRespuesta=self.__consultaReceptorFecha(filtros);
            xml=DescargarXML(self.__sesion, htmlRespuesta, directorioAGuardar)
            xml.obtenerEnlacesYDescargar()
            return True
        except:
            error = traceback.format_exc()
            self.__error = error
            return False
