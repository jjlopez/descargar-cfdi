class FiltrosRecibidos:

    def __init__(self):
        self.annio=''
        self.mes=''
        self.dia=''

    def obtenerPOST(self):
        post={}
        post['__ASYNCPOST'] = 'true'
        post['__EVENTARGUMENT'] = ''
        post['__EVENTTARGET'] = ''
        post['__LASTFOCUS'] = ''
        post['ctl00$MainContent$BtnBusqueda'] = 'Buscar CFDI'
        post['ctl00$MainContent$CldFecha$DdlAnio'] = self.annio
        post['ctl00$MainContent$CldFecha$DdlDia'] = self.dia
        post['ctl00$MainContent$CldFecha$DdlHora'] = '0'
        post['ctl00$MainContent$CldFecha$DdlHoraFin'] = '23'
        post['ctl00$MainContent$CldFecha$DdlMes'] = self.mes
        post['ctl00$MainContent$CldFecha$DdlMinuto'] = '0'
        post['ctl00$MainContent$CldFecha$DdlMinutoFin'] = '59'
        post['ctl00$MainContent$CldFecha$DdlSegundo'] = '0'
        post['ctl00$MainContent$CldFecha$DdlSegundoFin'] = '59'
        post['ctl00$MainContent$DdlEstadoComprobante'] = '-1'
        post['ctl00$MainContent$FiltroCentral'] = 'RdoFechas'
        post['ctl00$MainContent$TxtRfcReceptor'] = ''
        post['ctl00$MainContent$TxtUUID'] = ''
        post['ctl00$MainContent$ddlComplementos'] = '-1'
        post['ctl00$MainContent$hfInicialBool'] = 'false'
        post['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|ctl00$MainContent$BtnBusqueda'
        return post

    def obtenerPOSTFormularioFechas(self):
        post={}
        post['__ASYNCPOST'] = 'true'
        post['__EVENTARGUMENT'] = ''
        post['__EVENTTARGET']='ctl00$MainContent$RdoFechas'
        post['__LASTFOCUS'] = ''
        post['ctl00$MainContent$CldFecha$DdlAnio'] = '2015'
        post['ctl00$MainContent$CldFecha$DdlDia'] = '0'
        post['ctl00$MainContent$CldFecha$DdlHora'] = '0'
        post['ctl00$MainContent$CldFecha$DdlHoraFin'] = '23'
        post['ctl00$MainContent$CldFecha$DdlMes'] = '1'
        post['ctl00$MainContent$CldFecha$DdlMinuto'] = '0'
        post['ctl00$MainContent$CldFecha$DdlMinutoFin'] = '59'
        post['ctl00$MainContent$CldFecha$DdlSegundo'] = '0'
        post['ctl00$MainContent$CldFecha$DdlSegundoFin'] = '59'
        post['ctl00$MainContent$DdlEstadoComprobante'] = '-1'
        post['ctl00$MainContent$FiltroCentral'] = 'RdoFechas'
        post['ctl00$MainContent$TxtRfcReceptor'] = ''
        post['ctl00$MainContent$TxtUUID'] = ''
        post['ctl00$MainContent$ddlComplementos'] = '-1'
        post['ctl00$MainContent$hfInicialBool']='true'
        post['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|ctl00$MainContent$RdoFechas'
        return post

