import datetime


class FiltrosRecibidos:

    def __init__(self):
        self.annio = str(datetime.date.today().year)
        self.mes = '1'
        self.dia = '0'
        self.horaInicial = '0'
        self.minutoInicial = '0'
        self.segundoInicial = '0'
        self.horaFinal = '23'
        self.minutoFinal = '59'
        self.segundoFinal = '59'
        self.rfcEmisor = ''
        self.__estado = '1'  # 1.-Vigente,0.-Cancelado
        self.tipo = '-1'
        self.folioFiscal = ''

    def __formate_dia(self):
        if int(self.dia) < 10:
            self.dia = '0' + self.dia
        return self.dia

    def obtener_post(self):
        post = {}
        post['__ASYNCPOST'] = 'true'
        post['__EVENTARGUMENT'] = ''
        post['__EVENTTARGET'] = ''
        post['__LASTFOCUS'] = ''
        post['ctl00$MainContent$BtnBusqueda'] = 'Buscar CFDI'
        post['ctl00$MainContent$CldFecha$DdlAnio'] = self.annio
        post['ctl00$MainContent$CldFecha$DdlDia'] = self.__formateaDia()
        post['ctl00$MainContent$CldFecha$DdlHora'] = self.horaInicial
        post['ctl00$MainContent$CldFecha$DdlHoraFin'] = self.horaFinal
        post['ctl00$MainContent$CldFecha$DdlMes'] = self.mes
        post['ctl00$MainContent$CldFecha$DdlMinuto'] = self.minutoInicial
        post['ctl00$MainContent$CldFecha$DdlMinutoFin'] = self.minutoFinal
        post['ctl00$MainContent$CldFecha$DdlSegundo'] = self.segundoInicial
        post['ctl00$MainContent$CldFecha$DdlSegundoFin'] = self.segundoFinal
        post['ctl00$MainContent$DdlEstadoComprobante'] = self.__estado
        post['ctl00$MainContent$FiltroCentral'] = self.__obtenFiltroCentral()
        post['ctl00$MainContent$TxtRfcReceptor'] = self.rfcEmisor
        post['ctl00$MainContent$TxtUUID'] = self.folioFiscal
        post['ctl00$MainContent$ddlComplementos'] = self.tipo
        post['ctl00$MainContent$hfInicialBool'] = 'false'
        post['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|'\
                                       'ctl00$MainContent$BtnBusqueda'
        return post

    def __obten_filtro_central(self):
        if self.folioFiscal != '':
            return 'RdoFolioFiscal'
        else:
            return 'RdoFechas'

    def obtener_post_formulario_fechas(self):
        post = {}
        annio = datetime.date.today().year
        post['__ASYNCPOST'] = 'true'
        post['__EVENTARGUMENT'] = ''
        post['__EVENTTARGET'] = 'ctl00$MainContent$RdoFechas'
        post['__LASTFOCUS'] = ''
        post['ctl00$MainContent$CldFecha$DdlAnio'] = str(annio)
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
        post['ctl00$MainContent$hfInicialBool'] = 'true'
        post['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|'\
                                       'ctl00$MainContent$RdoFechas'
        return post
