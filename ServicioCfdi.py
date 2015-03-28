from PortalCfdi import PortalCfdi
from FiltrosRecibidos import FiltrosRecibidos


class ServicioCfdi:
    def __init__(self, rfc, contrasena):
        self.__rfc = rfc
        self.__contrasena = contrasena
        self.__resultado = False
        self.__mensaje_error = ''
        self.__lista_documentos_descargados = []

    def __peticion_portal_cfdi(self, directorio_guardar, filtros):
        portal_cfdi = PortalCfdi(self.__rfc, self.__contrasena)
        self.__resultado = portal_cfdi.consultar(directorio_guardar, filtros)
        if not self.__resultado:
            self.__mensaje_error = portal_cfdi.error()
        else:
            self.__lista_documentos_descargados = portal_cfdi.\
                lista_cfdis()
        return self.__resultado

    def lista_cfdis(self):
        return self.__lista_documentos_descargados

    def error(self):
        return self.__mensaje_error

    def descargar_fecha(self, directorio_guardar, annio, mes, dia):
        filtros = FiltrosRecibidos()
        filtros.annio = annio
        filtros.mes = mes
        filtros.dia = dia
        return self.__peticion_portal_cfdi(directorio_guardar, filtros)

    def descargar_anniomes(self, directorio_guardar, annio, mes):
        filtros = FiltrosRecibidos()
        filtros.annio = annio
        filtros.mes = mes
        return self.__peticion_portal_cfdi(directorio_guardar, filtros)

    def descargar_folio(self, directorio_guardar, folio_fiscal):
        filtros = FiltrosRecibidos()
        filtros.folio_fiscal = folio_fiscal
        return self.__peticion_portal_cfdi(directorio_guardar, filtros)

    def descargar(self, directorio_guardar, filtros):
        return self.__peticion_portal_cfdi(directorio_guardar, filtros)
