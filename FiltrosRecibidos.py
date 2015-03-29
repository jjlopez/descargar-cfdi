import datetime


class FiltrosRecibidos:

    def __init__(self):
        self.annio = str(datetime.date.today().year)
        self.mes = '1'
        self.dia = '0'
        self.hora_inicial = '0'
        self.minuto_inicial = '0'
        self.segundo_inicial = '0'
        self.hora_final = '23'
        self.minuto_final = '59'
        self.segundo_final = '59'
        self.rfc_emisor = ''
        self.__estado = '1'  # 1.-Vigente,0.-Cancelado
        self.tipo = '-1'
        self.folio_fiscal = ''

    def __formatea_dia(self):
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
        post['ctl00$MainContent$CldFecha$DdlDia'] = self.__formatea_dia()
        post['ctl00$MainContent$CldFecha$DdlHora'] = self.hora_inicial
        post['ctl00$MainContent$CldFecha$DdlHoraFin'] = self.hora_final
        post['ctl00$MainContent$CldFecha$DdlMes'] = self.mes
        post['ctl00$MainContent$CldFecha$DdlMinuto'] = self.minuto_inicial
        post['ctl00$MainContent$CldFecha$DdlMinutoFin'] = self.minuto_final
        post['ctl00$MainContent$CldFecha$DdlSegundo'] = self.segundo_inicial
        post['ctl00$MainContent$CldFecha$DdlSegundoFin'] = self.segundo_final
        post['ctl00$MainContent$DdlEstadoComprobante'] = self.__estado
        post['ctl00$MainContent$FiltroCentral'] = self.__obten_filtro_central()
        post['ctl00$MainContent$TxtRfcReceptor'] = self.rfc_emisor
        post['ctl00$MainContent$TxtUUID'] = self.folio_fiscal
        post['ctl00$MainContent$ddlComplementos'] = self.tipo
        post['ctl00$MainContent$hfInicialBool'] = 'false'
        post['ctl00$ScriptManager1'] = 'ctl00$MainContent$UpnlBusqueda|'\
                                       'ctl00$MainContent$BtnBusqueda'
        return post

    def __obten_filtro_central(self):
        if self.folio_fiscal != '':
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
