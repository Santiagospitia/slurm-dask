Antes de ejecutar el docker compose se deben crear las imágenes en local, cada componente del cluster tiene su respectivo Dockerfile.

Para crear la imagen de Jupyter ejecutar:
     $ cd jupyter/
     $ docker build -t jupyter:vlocal .

Para crear la imagen del Master ejecutar:
     $ cd master/
     $ docker build -t master:vlocal .

Para crear la imagen del Node ejecutar:
     $ cd master/
     $ docker build -t node:vlocal .

Una vez creadas las imágenes se puede ejecutar el docker compose.

Para ejecutar el docker compose:

     $ docker-compose up -d

