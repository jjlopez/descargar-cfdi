from PortalCfdi import PortalCfdi
from FiltrosRecibidos import FiltrosRecibidos

class ServicioCfdi:
    def __init__(self, rfc, contrasena):
        self.rfc = rfc
        self.contrasena = contrasena

    def __peticionPortalCfdi(self, directorioAGuardar, filtros):
        self.portalCfdi = PortalCfdi(self.rfc, self.contrasena)
        self.portalCfdi.logueoDeUsuarioConCIEC()
        self.portalCfdi.consultar(directorioAGuardar, filtros)


    def descargarPorAnnioMesYDia(self, directorioAGuardar,  annio, mes, dia):
        filtros = FiltrosRecibidos()
        filtros.annio = annio
        filtros.mes = mes
        filtros.dia = dia
        self.__peticionPortalCfdi(directorioAGuardar, filtros)

    def descargarPorAnnioYMes(self, directorioAGuardar, annio, mes):
        filtros=FiltrosRecibidos()
        filtros.annio=annio
        filtros.mes=mes
        self.__peticionPortalCfdi(directorioAGuardar, filtros)
