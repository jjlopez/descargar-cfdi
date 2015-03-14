# Métodos de la clase ServicioCfdi
*descargarPorAnnioYMes
*descargarPorAnnioMesYDia

## descargarPorAnnioYMes
Filtra por año y mes para despues almacenar los xml encontrados en el directorio 
que recibe como parametro.

```python
descargarPorAnnioYMes(directorio, año, mes)
```

*directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
*año: Año a buscar.
*mes: Mes a buscar
    *1=Enero
    *2=Febrero
    *3=Marzo
    *4=Abril
    *5=Mayo
    *6=Junio
    *7=Julio
    *8=Agosto
    *9=Septiembre
    *10=Octubre
    *11=Noviembre
    *12=Diciembre

#### Ejemplo de uso método descargarPorAnnioYMes

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
#Descargar al directorio /home/usuario/xml los xml del mes 03/2015
servicio.descargarPorAnnioYMes('/home/usuario/xml/', '2015', '3')
```
## descargarPorAnnioMesYDia
Filtra por año, mes y dia para despues almacenar los xml encontrados en el directorio 
que recibe como parametro.

```python
descargarPorAnnioMesYDia(directorio, año, mes, dia)
```

*directorio: Indica donde se almacenarán los xml encontrados, es necesario que 
directorio ya exista y termine con / .
*año: Año a buscar
*mes: Mes a buscar
    *1=Enero
    *2=Febrero
    *3=Marzo
    *4=Abril
    *5=Mayo
    *6=Junio
    *7=Julio
    *8=Agosto
    *9=Septiembre
    *10=Octubre
    *11=Noviembre
    *12=Diciembre
dia: Dia a buscar.

#### Ejemplo de uso método descargarPorAnnioMesYDia

```python
from ServicioCfdi import ServicioCfdi

servicio = ServicioCfdi('RFC', 'Contrasena')
#Descargar al directorio /home/usuario/xml los xml de la fecha 14/03/2015
servicio.descargarPorAnnioMesYDia('/home/usuario/xml/', '2015', '3', '14')
```
