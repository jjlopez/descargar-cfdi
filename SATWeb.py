import requests
from HTMLForm import HTMLForm

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
        inputValores = htmlFormulario.readAndGetInputValues()
        return inputValores

    def __leerFormularioDeAccessControl(self, valores):
        url = 'https://cfdicontribuyentes.accesscontrol.windows.net/v2/wsfederation'
        respuesta = self.sesion.post(url, data=valores)
        htmlFuente = respuesta.text
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.readAndGetInputValues()
        return inputValores

    def __entrarAPantallaInicioSistema(self, valores):
        url = 'https://portalcfdi.facturaelectronica.sat.gob.mx'
        respuesta = self.sesion.post(url, data=valores)
        html = respuesta.text
        return html

    def __seleccionarTipo(self, htmlFuente):
        valores = {}
        htmlFormulario = HTMLForm(htmlFuente, 'form')
        inputValores = htmlFormulario.readAndGetInputValues()
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
        html = respuesta.text
        print(html)
