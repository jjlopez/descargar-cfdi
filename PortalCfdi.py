import requests
from HTMLForm import HTMLForm
from DescargarXML import DescargarXML
from ParserFormatSAT import ParserFormatSAT
from Header import Header
from Utilerias import Utilerias

class PortalCfdi:
    def __init__(self, rfc, contrasena):
        self.rfc = rfc
        self.contrasena = contrasena
        self.sesion = requests.Session()
        self.directorioAGuardar=''
        self.header = Header()
        self.hostCfdiau = 'cfdiau.sat.gob.mx'
        self.hostPortalCfdi = 'portalcfdi.facturaelectronica.sat.gob.mx'
        self.urlCfdiau = 'https://' + self.hostCfdiau + '/'
        self.urlPortalCfdi = 'https://' + self.hostPortalCfdi + '/'

    def __entrarAlaPaginaInicio(self):
        url = self.urlCfdiau + '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.sesion.post(url)

    def __enviarFormularioConCIEC(self):
        url = self.urlCfdiau + 'nidp/app/login?sid=0&sid=0'
        encabezados = self.header.obtener(
            self.hostCfdiau,
            self.urlCfdiau +
            '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        )

        valoresPost = {
            'option':'credential',
            'Ecom_User_ID':self.rfc,
            'Ecom_Password':self.contrasena,
            'submit':'Enviar'
        }

        self.sesion.post(url, data=valoresPost, headers=encabezados)

    def __leerFormulario(self, html):
        htmlFormulario = HTMLForm(html, 'form')
        inputValores = htmlFormulario.getFormValues()
        return inputValores

    def __leerFormularioDeRespuesta(self):
        url = self.urlPortalCfdi
        respuesta = self.sesion.get(url)
        htmlRespuesta = respuesta.text
        return self.__leerFormulario(htmlRespuesta)

    def __leerFormularioDeAccessControl(self, valoresPost):
        url = 'https://cfdicontribuyentes.accesscontrol.windows.net/v2/wsfederation'
        respuesta = self.sesion.post(url, data=valoresPost)
        htmlRespuesta = respuesta.text
        return self.__leerFormulario(htmlRespuesta)

    def __entrarAPantallaInicioSistema(self, valoresPost):
        url = self.urlPortalCfdi
        respuesta = self.sesion.post(url, data=valoresPost)
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
        url = self.urlPortalCfdi + 'Consulta.aspx'
        post = self.__obtenerValoresPostDelTipoDeBusqueda(htmlFuente)
        encabezados = self.header.obtener(
            self.hostCfdiau,
            self.urlPortalCfdi
        )
        respuesta = self.sesion.post(url, data=post, headers=encabezados)
        return respuesta.text

    def logueoDeUsuarioConCIEC(self):
        self. __entrarAlaPaginaInicio()
        self.__enviarFormularioConCIEC()
        valoresPost = self.__leerFormularioDeRespuesta()
        valoresPostAccessControl = self.__leerFormularioDeAccessControl(valoresPost)
        html = self.__entrarAPantallaInicioSistema(valoresPostAccessControl)
        self.__seleccionarTipo(html)

    def __entrarConsultaReceptor(self, filtros):
        url = self.urlPortalCfdi + 'ConsultaReceptor.aspx'
        respuesta = self.sesion.get(url)
        htmlRespuesta = respuesta.text
        inputValores = self.__leerFormulario(htmlRespuesta)
        util = Utilerias()
        post = util.mergeListas(inputValores, filtros.obtenerPOSTFormularioFechas())
        encabezados = self.header.obtenerAJAX(
            self.hostPortalCfdi,
            self.urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta = self.sesion.post(url, data=post, headers=encabezados)
        return respuesta.text, inputValores

    def __obtenerValoresPostBusquedaFechas(self, htmlFuente, inputValores, filtros):
        parser = ParserFormatSAT(htmlFuente)
        valoresCambioEstado = parser.obtenerValoresFormulario()
        util = Utilerias()
        temporal = util.mergeListas(inputValores, filtros.obtenerPOST())
        return util.mergeListas(temporal, valoresCambioEstado)
 
    def consultaReceptorFecha(self, filtros):
        url = self.urlPortalCfdi + 'ConsultaReceptor.aspx'
        htmlRespuesta, inputValores = self.__entrarConsultaReceptor(filtros)
        valoresPost = self.__obtenerValoresPostBusquedaFechas(
            htmlRespuesta,
            inputValores,
            filtros
        )
        encabezados = self.header.obtenerAJAX(
            self.hostPortalCfdi,
            self.urlPortalCfdi + 'ConsultaReceptor.aspx'
        )
        respuesta=self.sesion.post(url, data=valoresPost, headers=encabezados)
        return respuesta.text

    def consultar(self, directorioAGuardar, filtros):
        htmlRespuesta=self.consultaReceptorFecha(filtros);
        xml=DescargarXML(self.sesion, htmlRespuesta, directorioAGuardar)
        xml.obtenerEnlacesYDescargar()
