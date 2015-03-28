from PortalCfdi import PortalCfdi
from FiltrosRecibidos import FiltrosRecibidos


class ServicioCfdi:
    def __init__(self, rfc, contrasena):
        self.__rfc = rfc
        self.__contrasena = contrasena
        self.__resultado = False
        self.__mensajeError = ''
        self.__listaDocumentosDescargados = []

    def __peticion_portal_cfdi(self, directorioAGuardar, filtros):
        portalCfdi = PortalCfdi(self.__rfc, self.__contrasena)
        self.__resultado = portalCfdi.consultar(directorioAGuardar, filtros)
        if not self.__resultado:
            self.__mensajeError = portalCfdi.obtieneMensajeError()
        else:
            self.__listaDocumentosDescargados = portalCfdi.\
                obtieneListaDocumentosDescargados()
        return self.__resultado

    def obtieneListaDocumentosDescargados(self):
        return self.__listaDocumentosDescargados

    def obtieneMensajeError(self):
        return self.__mensajeError

    def descargarPorAnnioMesYDia(self, directorioAGuardar, annio, mes, dia):
        filtros = FiltrosRecibidos()
        filtros.annio = annio
        filtros.mes = mes
        filtros.dia = dia
        return self.__peticion_portal_cfdi(directorioAGuardar, filtros)

    def descargarPorAnnioYMes(self, directorioAGuardar, annio, mes):
        filtros = FiltrosRecibidos()
        filtros.annio = annio
        filtros.mes = mes
        return self.__peticion_portal_cfdi(directorioAGuardar, filtros)

    def descargarPorFolioFiscal(self, directorioAGuardar, folioFiscal):
        filtros = FiltrosRecibidos()
        filtros.folioFiscal = folioFiscal
        return self.__peticion_portal_cfdi(directorioAGuardar, filtros)

    def descargarPorFiltros(self, directorioAGuardar, filtros):
        return self.__peticionPortalCfdi(directorioAGuardar, filtros)
