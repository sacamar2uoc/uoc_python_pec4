# ES-PEC4 Samuel Campo Martínez
Este conjuntos de archivos continen una serie de funciones que permiten realizar la tarea requerida. Algunas de estas funciones tienen un gran valor por su reciclaje en diferentes puntos del desarrollo. Otras ayudan a una mejor lectura del funcionamiento lógico del conjunto.

## _Run_
Para realizar todo el ejercicio:
1. Abrir un terminal y colocarse en el directorio donde se alojan los scripts.
2. Correr el script con python 3, se puede usar este comando:

```
python3 main.py
```

## _Output_
Tras esto, por pantalla aparece el texto informativo sobre:
* La frecuencia de los patrones.
* El número de personas que han participado en las entrevistas de concienciación.

Además en el mismo directorio debe haber generado 6 imágenes:

* Ejercicio 3
	* people_approve_disapprove.png: Gráfica que muestra el número de personas que aprueba versus los que no aprueba las políticas de Trump según su alineación política. 

* Ejercicio 4
	* poll_per_grade.png: Número de entrevistas agrupadas por la nota del agente entrevistador.
	* people_economy_concern.png: Comparativa en el número de personas que son conscientes y las que no de los efectos del coronavirus en la economía.
	* people_infected_concern.png: Comparativa en el número de personas que son conscientes y las que no de los efectos del coronavirus en la salud.

* Ejercicio 5
	* people_distr_date_poll_abs.png: Comparativa del número absoluto de personas por nivel de concienciación sobre los efectos de la pandemia en su entorno.
	* people_distr_date_poll_perc.png: Comparativa del número porcentual de personas por nivel de concienciación sobre los efectos de la pandemia en su entorno.

## Código y estándares

### Nomenclatura funciones
Existe un estándar común de nomenclatura de las funciones, su primera palabra es un verbo que indica qué hace:

* get: Significa que recoge datos, en nuestro caso solamente recoge datos de los archivos en el local.
* build: Indica que construye una variable de forma que recibe una variable y devuelve otra de similares dimensiones.
* do_plot: Se encargará de hacer _plots_, en nuestro caso todas las gráficas serán guardadas y no mostradas.
* check: Recibe un input y devuelve un valor tipo bool.
* main: Se trata de la función main del ejercicio. Se encargará de llamar a todas las funciones para terminar dando toda la información o gráficas necesarias para responder las cuestiones del apartado.

Es decir, que ejecutando la función main de cada ejercicio se debe obtener lo que se pide en cada uno de ellos. Sin embargo, para la ejecucción completa ya existe el archivo main. Cabe descatar que la función main del ejercicio 2 es llamada por las funciones del ejercicio 3, 4 y 5. Y ya que solamente ha de devolver datos, el usuario no podrá tener ningún output de por sí. Para ello estarían los tests.

### Estructura del código
Las funciones están ordenadas por orden de aparición en la función main de cada archivo, siendo esta siempre la primera.


## Nota
Para una investigación más cómoda del código aconsejo abrir el archivo html que se ha generado automáticamente a través del código.

No se ha empleado el estándar de utils para encapsular todas las funciones para una evaluación más sencilla del código.

## Licencia
[Este código está bajo la licencia Apace License 2.0]: https://github.com/sacamar2uoc/uoc_python_pec4/blob/main/LICENSE
