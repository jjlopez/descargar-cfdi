# Métodos de la clase ServicioCfdi
* descargar_anniomes
* descargar_fecha
* descargar_folio
* descargar

## descargar_anniomes
Filtra por año y mes para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargar_anniomes(directorio, año, mes)
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

#### Ejemplo de uso método descargar_anniomes

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
# Descargar al directorio /home/usuario/xml los xml del mes 03/2015
if servicio.descargar_anniomes('/home/usuario/xml/', '2015', '3'):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())

```
## descargar_fecha
Filtra por año, mes y dia para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargar_fecha(directorio, año, mes, dia)
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

#### Ejemplo de uso método descargar_fecha

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
# Descargar al directorio /home/usuario/xml los xml de la fecha 14/03/2015
if servicio.descargar_fecha('/home/usuario/xml/', '2015', '3', '14'):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())

```
## descargar_folio
Filtra por folio fiscal para despues almacenar el xml encontrado en el directorio 
que recibe como parámetro.

```python
descargar_folio(directorio, folioFiscal)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
folioFiscal: UUID a buscar

#### Ejemplo de uso descargar_folio

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
# Descargar al directorio /home/usuario/xml el xml del UUID
if servicio.descargar_folio('/home/usuario/xml/', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX'):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())
```
## descargar
Filtra por los datos establecidos para despues almacenar los xml encontrados en el directorio 
que recibe como parámetro.

```python
descargar(directorio, filtros)
```

* directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
filtros: Filtros personalizados

#### Ejemplo de uso descargar

* Descargar los xml del emisor xxxxxxxxxxxxx con fecha del 14/03/2015

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
# Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio = '2015'
filtros.mes = '3'
filtros.dia = '14'
filtros.rfc_emisor = 'xxxxxxxxxxxxx'

if servicio.descargar('/home/usuario/xml/', filtros):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())
```
* Descargar los xml del emisor xxxxxxxxxxxxx del mes de febrero

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
# Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio = '2015'
filtros.mes = '2'
filtros.rfc_emisor = 'xxxxxxxxxxxxx'

if servicio.descargar('/home/usuario/xml/', filtros):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())
```
* Descargar los xml del día 16/02/2015 que tengan la hora de creación entre las
15:10:07 y las 22:14:10 horas

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
# Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio = '2015'
filtros.mes = '2'
filtros.dia = '16'
filtros.horaInicial = '15'
filtros.minutoInicial = '10'
filtros.segundoInicial='7'
filtros.horaFinal = '22'
filtros.minutoFinal = '14'
filtros.segundoFinal = '10'

if servicio.descargar('/home/usuario/xml/', filtros):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())
```
* Descargar los xml del mes de enero del 2015 que sean del tipo "Vales de Despensa"

```python
from ServicioCfdi import ServicioCfdi
from FiltrosRecibidos import FiltrosRecibidos

servicio = ServicioCfdi('RFC', 'Contrasena')
# Definir filtros personalizados
filtros = FiltrosRecibidos()
filtros.annio = '2015'
filtros.mes = '1'
filtros.tipo = '33554432'

if servicio.descargar('/home/usuario/xml/', filtros):
    descargados = servicio.lista_cfdis()
    print("XML Descargados: " + str(len(descargados)))
else:
    print("Ha ocurrido el siguiente error: " + servicio.error())
```
#FiltrosRecibidos
* annio
* mes
* dia
* hora_inicial
* minuto_inicial
* segundo_inicial
* hora_final
* minuto_final
* segundo_final
* rfc_emisor
* tipo
* folio_fiscal

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
