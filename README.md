# MusicPro API

Este proyecto consta de 2 API's que deben ser ejecutadas, una de Django y otra de NodeJs, la primera se encarga del manejo de datos mientras que la de NodeJs se encarga de la implementación de WebPay.

Deben estar ambas activas al momento de ejecutar nuestro código.

## Configuración Django

Para ejecutar la API de django debes seguir los siguientes pasos:

1. Crea un entorno virtual con `python -m venv env` desde la terminal donde clonaste el repositorio.
2. Activa el entorno virtual entrando a `env/script` y ejecuta `./activate`.
3. Ingresa a la carpeta "MusicProApi" y ejecuta en la terminal `pip install -r requirements.txt`.
4. Ejecuta la API con `python manage.py runserver`.

Con esto listo, entrando a `[enlace]/swagger` podrás acceder a la documentación de la API de Django.

---

## Configuracion NodeJs

Para ejecutar la API de NodeJs debes:

1. Ingresar a la carpeta "MusicPro-webpay" y ejecuta el comando `npm i`.
2. Desde la misma carpeta, ejecuta el comando `node .`;

---

# Documentacion MusicPro-webpay

La API de NodeJs "**MusicPro-webpay**" posee 3 End-Points, siendo estos:

* GET(`/`): Esta nos permite traer los pedidos que se encuentran en la base de datos (Principalmente para ayudar a la hora de seleccionar un pedido a comprar).

  * Parámetros: N/A.
  * Retorno: Listado de pedidos. 

  ---

* POST(`/comprar`): Este nos permite "Llevar a cabo una compra/iniciar una transacción en webpay".

  * Parámetros: Objeto con un "id" de producto valido. 

    *por ejemplo:*

     ~~~json
     {
         "id":3
     }
     ~~~

    (El `id` debe existir en la tabla `pedidos`)

  * Retorno: Enlace para realizar compra (este debe ser ingresado en el buscador web de tu preferencia).

  ---

* GET(`/confirmacion`): Este nos permite "revisar el estado final de la transacción" y en base a este retornara un mensaje de confirmación, el mismo envía el id del pedido al api de Django, donde se actualiza en la base de datos.

  * Parámetros: Token de la compra (se ingresa automáticamente cuando la compra se realiza).
  * Retorno: Mensaje de confirmación de compra.