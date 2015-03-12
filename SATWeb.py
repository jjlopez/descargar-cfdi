import requests
from HTMLForm import HTMLForm
from DescargarXML import DescargarXML

class SATWeb:
    def __init__(self, rfc, contrasena):
        self.rfc = rfc
        self.contrasena = contrasena
        self.sesion = requests.Session()

    def __entrarAlaPaginaInicio(self):
        url = 'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0'
        self.sesion.post(url)

    def __enviarFormularioConCIEC(self):
        url = 'https://cfdiau.sat.gob.mx/nidp/app/login?sid=0&sid=0'
        encabezados = {
            'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.5',
            'Connection':'keep-alive',
            'Host':'cfdiau.sat.gob.mx',
            'Referer':'https://cfdiau.sat.gob.mx/nidp/app/login?id=SATUPCFDiCon&sid=0&option=credential&sid=0',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Content-Type':'application/x-www-form-urlencoded',
        }
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

    def consultaReceptor(self):
        url= 'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx'
        respuesta = self.sesion.get(url)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.getFormValues()
        inputValores['__ASYNCPOST'] = 'true'
        inputValores['__EVENTARGUMENT'] = ''
        inputValores['__EVENTTARGET'] = ''
        inputValores['__LASTFOCUS'] = ''
        inputValores['ctl00$MainContent$BtnBusqueda'] = 'Buscar CFDI'
        inputValores['ctl00$MainContent$CldFecha$DdlAnio'] = '2015'
        inputValores['ctl00$MainContent$CldFecha$DdlDia'] = '0'
        inputValores['ctl00$MainContent$CldFecha$DdlHora'] = '0'
        inputValores['ctl00$MainContent$CldFecha$DdlHoraFin'] = '23'
        inputValores['ctl00$MainContent$CldFecha$DdlMes'] = '3'
        inputValores['ctl00$MainContent$CldFecha$DdlMinuto'] = '0'
        inputValores['ctl00$MainContent$CldFecha$DdlMinutoFin'] = '59'
        inputValores['ctl00$MainContent$CldFecha$DdlSegundo'] = '0'
        inputValores['ctl00$MainContent$CldFecha$DdlSegundoFin'] = '59'
        inputValores['ctl00$MainContent$DdlEstadoComprobante'] = '-1'
        inputValores['ctl00$MainContent$FiltroCentral'] = 'RdoFechas'
        inputValores['ctl00$MainContent$TxtRfcReceptor'] = ''
        inputValores['ctl00$MainContent$TxtUUID'] = ''
        inputValores['ctl00$MainContent$ddlComplementos'] = '-1'
        inputValores['ctl00$MainContent$hfInicialBool'] = 'false'
        inputValores['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|ctl00$MainContent$BtnBusqueda'
        url= 'https://portalcfdi.facturaelectronica.sat.gob.mx/ConsultaReceptor.aspx'
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

        respuesta = self.sesion.post(url, data=inputValores, headers=encabezados)
        htmlFuente = respuesta.text
        xml=DescargarXML(htmlFuente, './')
        xml.descargar()
        self.guardaTablaHTML(htmlFuente)

    def guardaTablaHTML(self, htmlFuente):
        file = open("cfdi.html", "w")
        file.write(htmlFuente)
        file.close()
