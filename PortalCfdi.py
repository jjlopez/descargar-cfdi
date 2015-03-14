import requests
from HTMLForm import HTMLForm
from DescargarXML import DescargarXML
from ParserFormatSAT import ParserFormatSAT
from Header import Header

class PortalCfdi:
    def __init__(self, rfc, contrasena):
        self.rfc = rfc
        self.contrasena = contrasena
        self.sesion = requests.Session()
        self.directorioAGuardar=''
        self.header = Header()
        self.urlCfdiau = 'https://cfdiau.sat.gob.mx/'

    def __entrarAlaPaginaInicio(self):
        url = self.urlCfdiau + '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.sesion.post(url)

    def __enviarFormularioConCIEC(self):
        url = self.urlCfdiau + 'nidp/app/login?sid=0&sid=0'
        encabezados = self.header.obtener(
            self.urlCfdiau +
            '/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        )

        valores = {'option':'credential', 'Ecom_User_ID':self.rfc, 'Ecom_Password':self.contrasena, 'submit':'Enviar'}
        self.sesion.post(url, data=valores,headers=encabezados)

    def __leerFormularioDeRespuesta(self):
        url = 'https://portalcfdi.facturaelectronica.sat.gob.mx/'
        respuesta = self.sesion.get(url)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.getFormValues()
        return inputValores

    def __leerFormularioDeAccessControl(self, valores):
        url = 'https://cfdicontribuyentes.accesscontrol.windows.net/v2/wsfederation'
        respuesta = self.sesion.post(url, data=valores)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.getFormValues()
        return inputValores

    def __entrarAPantallaInicioSistema(self, valores):
        url = 'https://portalcfdi.facturaelectronica.sat.gob.mx'
        respuesta = self.sesion.post(url, data=valores)
        html = respuesta.text
        return html

    def __seleccionarTipo(self, htmlFuente):
        valores = {}
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.getFormValues()
        inputValores['ctl00$MainContent$TipoBusqueda'] = 'RdoTipoBusquedaReceptor'
        inputValores['__ASYNCPOST'] = 'true'
        inputValores['__EVENTTARGET'] = ''
        inputValores['__EVENTARGUMENT'] = ''
        inputValores['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|ctl00$MainContent$BtnBusqueda'

        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Connection':'keep-alive',
            'Host':'cfdiau.sat.gob.mx',
            'Referer':'https://portalcfdi.facturaelectronica.sat.gob.mx',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-Type':'application/x-www-form-urlencoded',
        }

        url = 'https://portalcfdi.facturaelectronica.sat.gob.mx/Consulta.aspx'
        respuesta = self.sesion.post(url, data=inputValores, headers=encabezados)
        html = respuesta.text

    def logueoDeUsuarioConCIEC(self):
        self. __entrarAlaPaginaInicio()
        self.__enviarFormularioConCIEC()
        inputValores = self.__leerFormularioDeRespuesta()
        inputValores = self.__leerFormularioDeAccessControl(inputValores)
        html = self.__entrarAPantallaInicioSistema(inputValores)
        self.__seleccionarTipo(html)


    def consultaReceptorFecha(self, filtros):
        url= 'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx'
        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'portalcfdi.facturaelectronica.sat.gob.mx',
            'Referer':'https://portalcfdi.facturaelectronica.sat.gob.mx/Consulta.aspx',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
        }

        respuesta = self.sesion.get(url)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')

        inputValores = htmlFormulario.getFormValues()
        post=inputValores.copy()
        post.update(filtros.obtenerPOSTFormularioFechas())
        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'portalcfdi.facturaelectronica.sat.gob.mx',
            'Referer':'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
            'X-MicrosoftAjax':'Delta=true',
            'x-requested-with':'XMLHttpRequest',
            'Pragma':'no-cache'
        }
        respuesta=self.sesion.post(url, data=post, headers=encabezados)
        htmlFuente=respuesta.text
        parser=ParserFormatSAT(htmlFuente)
        valoresCambioEstado=parser.obtenerValoresFormulario()


        post=inputValores.copy()
        post.update(filtros.obtenerPOST())
        post.update(valoresCambioEstado)
        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'portalcfdi.facturaelectronica.sat.gob.mx',
            'Referer':'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
            'X-MicrosoftAjax':'Delta=true',
            'x-requested-with':'XMLHttpRequest',
            'Pragma':'no-cache'
        }
        respuesta=self.sesion.post(url, data=post, headers=encabezados)
        htmlFuente=respuesta.text

        return htmlFuente


    def consultaReceptor(self, filtros):
        url= 'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx'
        respuesta = self.sesion.get(url)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.getFormValues()
        url= 'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx'
        post=inputValores.copy()
        post.update(filtros.obtenerPOST())
        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Host':'portalcfdi.facturaelectronica.sat.gob.mx',
            'Referer':'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
            'X-MicrosoftAjax':'Delta=true',
            'x-requested-with':'XMLHttpRequest'
        }
        respuesta = self.sesion.post(url, data=post, headers=encabezados)
        htmlFuente = respuesta.text
        return htmlFuente

    def consultar(self, directorioAGuardar, filtros):
        htmlFuente=self.consultaReceptorFecha(filtros);
        self.guardaTablaHTML(htmlFuente)
        xml=DescargarXML(self.sesion, htmlFuente, directorioAGuardar)
        xml.obtenerEnlacesYDescargar()

    def guardaTablaHTML(self, htmlFuente):
        file = open("cfdi.html", "w")
        file.write(htmlFuente)
        file.close()
