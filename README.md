# Métodos de la clase ServicioCfdi
* descargarPorAnnioYMes
* descargarPorAnnioMesYDia
* descargarPorFolioFiscal
* descargarPorFiltros

## descargarPorAnnioYMes
Filtra por año y mes para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargarPorAnnioYMes(directorio, año, mes)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
* año: Año a buscar.
* mes: Mes a buscar
    * 1=Enero
    * 2=Febrero
    * 3=Marzo
    * 4=Abril
    * 5=Mayo
    * 6=Junio
    * 7=Julio
    * 8=Agosto
    * 9=Septiembre
    * 10=Octubre
    * 11=Noviembre
    * 12=Diciembre

#### Ejemplo de uso método descargarPorAnnioYMes

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
#Descargar al directorio /home/usuario/xml los xml del mes 03/2015
if not servicio.descargarPorAnnioYMes('/home/usuario/xml/', '2015', '3'):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))

```
## descargarPorAnnioMesYDia
Filtra por año, mes y dia para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargarPorAnnioMesYDia(directorio, año, mes, dia)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
* año: Año a buscar
* mes: Mes a buscar
    * 1=Enero
    * 2=Febrero
    * 3=Marzo
    * 4=Abril
    * 5=Mayo
    * 6=Junio
    * 7=Julio
    * 8=Agosto
    * 9=Septiembre
    * 10=Octubre
    * 11=Noviembre
    * 12=Diciembre
* dia: Dia a buscar.

#### Ejemplo de uso método descargarPorAnnioMesYDia

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
#Descargar al directorio /home/usuario/xml los xml de la fecha 14/03/2015
if not servicio.descargarPorAnnioMesYDia('/home/usuario/xml/', '2015', '3', '14'):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))

```
## descargarPorFolioFiscal
Filtra por folio fiscal para despues almacenar el xml encontrado en el directorio 
que recibe como parámetro.

```python
descargarPorFolioFiscal(directorio, folioFiscal)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
folioFiscal: UUID a buscar

#### Ejemplo de uso descargarPorFolioFiscal

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
#Descargar al directorio /home/usuario/xml el xml del UUID
if not servicio.descargarPorFolioFiscal('/home/usuario/xml/', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX'):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))
```
## descargarPorFiltros
Filtra por los datos establecidos para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargarPorFiltros(directorio, filtros)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
filtros: Filtros personalizados

#### Ejemplo de uso descargarPorFiltros

* Descargar los xml del emisor xxxxxxxxxxxxx con fecha del 14/03/2015

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
#Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio='2015'
filtros.mes='3'
filtros.dia='14'
filtros.rfcEmisor='xxxxxxxxxxxxx'

if not servicio.descargarPorFiltros('/home/usuario/xml/', filtros):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))
```
* Descargar los xml del emisor xxxxxxxxxxxxx del mes de febrero

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
#Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio='2015'
filtros.mes='2'
filtros.rfcEmisor='xxxxxxxxxxxxx'

if not servicio.descargarPorFiltros('/home/usuario/xml/', filtros):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))
```
* Descargar los xml del día 16/02/2015 que tengan la hora de creación entre las
15:10:07 y las 22:14:10 horas

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
#Definir filtros personalizados
filtros=FiltrosRecibidos()
filtros.annio='2015'
filtros.mes='2'
filtros.dia='16'
filtros.horaInicial='15'
filtros.minutoInicial='10'
filtros.segundoInicial='7'
filtros.horaFinal='22'
filtros.minutoFinal='14'
filtros.segundoFinal='10'

if not servicio.descargarPorFiltros('/home/usuario/xml/', filtros):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))
```
* Descargar los xml del mes de enero del 2015 que sean del tipo "Vales de Despensa"

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
#Definir filtros personalizados
filtros=FiltrosRecibidos()
filtros.annio='2015'
filtros.mes='1'
filtros.tipo='33554432'

if not servicio.descargarPorFiltros('/home/usuario/xml/', filtros):
    print("Ha ocurrido el siguiente error: " + servicio.obtieneMensajeError())
else:
    descargados = servicio.obtieneListaDocumentosDescargados()
    print("XML Descargados: " + str(len(descargados)))
```
#FiltrosRecibidos
* annio
* mes
* dia
* horaInicial
* minutoInicial
* segundoInicial
* horaFinal
* minutoFinal
* segundoFinal
* rfcEmisor
* tipo
* folioFiscal

#Tipos
* 8=Estándar (sin complemento)
* 8388608=Aerolíneas
* 4=Compra Venta de Divisas
* 16777216=Consumo de Combustibles
* 64=Donatarias
* 256=Estado De Cuenta Bancario
* 512=Estado de Cuenta de Combustibles de Monederos Electrónicos
* 1024=Instituciones Educativas Privadas (Pago de colegiatura)
* 4096=Leyendas Fiscales
* 524288=Mis Cuentas
* 67108864=Notarios Públicos
* 2048=Otros Derechos e Impuestos
* 4194304=Pago en Especie
* 8192=Persona Física Integrante de Coordinado
* 128=Recibo de donativo
* 1048576=Recibo de Pago de Salarios
* 32=Sector de Ventas al Detalle (Detallista)
* 16384=SPEI de Tercero a Tercero
* 32768=Terceros
* 65536=Terceros
* 16=Turista o Pasajero Extranjero
* 33554432=Vales de Despensa
* 134217728=Vehículo Usado
* 2097152=Venta de Vehiculos
