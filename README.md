# Métodos de la clase ServicioCfdi
* descargarPorAnnioYMes
* descargarPorAnnioMesYDia
* descargarPorFolioFiscal

## descargarPorAnnioYMes
Filtra por año y mes para despues almacenar los xml encontrados en el directorio 
que recibe como parametro.

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
que recibe como parametro.

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
que recibe como parametro.

```python
descargarPorFolioFiscal(directorioAGuardar, folioFiscal)
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

