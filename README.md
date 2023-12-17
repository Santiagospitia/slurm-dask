#  Slurm + Dask

Este repositorio permite ejecutar un cluster de SLURM con el fin de poder ejecutar algún programa que requiera dividir sus tareas entre nodos, de esta forma haciendo más eficiente su ejecución

## Interactuando con el entorno

Para ejecutar el entorno correr el comando

     $ docker-compose up -d

Una vez ejecutado el docker compose dirigirse al http://localhost:8888/ ya que allí se encuentra corriendo el Jupyter. Estando aquí crear un entorno virtual python e instalar las siguientes dependencias:

     $ pip install dask
	  python -m pip install "dask[distributed]"
	  pip install dask_jobqueue


Una vez hecho esto se debe configurar un archivo llamado job.sh

     $ #!/bin/bash
     #
     #SBATCH --job-name=test
     #SBATCH --output=result.out
     #SBATCH --ntasks=2
     #
     source /home/admin/myenv/bin/activate
     sbcast -f daskEasy.py /tmp/daskEasy.py
     srun python3 /tmp/daskEasy.py
     deactivate

Con --job-name=test lo que se hace es darle un nombre a la ejecución que será realizada.
Con --output=result.out se guarda la salida de la ejecución en dicho archivo result.out
Con ntasks=2 se ejecuta 2 veces el archivo que será ejecutado.

Luego con source se activa el entorno virtual que contiene las dependencias.
Una vez activado el entorno virtual se hace una copia, mediante el comando sbcast, del archivo daskEasy.py y se pega en la carpeta tmp.
Luego dicha copia se ejecuta con el comando srun.
Para finalizar, se desactiva el entorno virtual.

Cabe recalcar que el archivo daskEasy.py tiene una configuración interna que le permite reconocer que se está ejecutando sobre un cluster de SLURM y definir cuántos workers tendrá (4 en este caso) . Esto se logra con el comando:
     
     $ cluster = SLURMCluster(cores = 1, memory = '1GB') 
       cluster.scale(4)

Luego este cluster se le pasa al cliente de Dask:

     $ client = Client(cluster)

De esta forma ya estaría configurado tanto SLURM como Dask para el archivo. Respecto a realizar operaciones, con la función map se pueden enviar las operaciones a realizar a una cola donde cada worker disponible realizará una de las operaciones en cola. simple_task es una función y range(10) es la lista de parámetros que recibirá:

     $ futures = client.map(simple_task, range(10))

Con las tareas enviadas a cola y los workers trabajando en ellas se pueden agrupar los resultados de dichas operaciones mediante el siguiente comando:

     $ results = client.gather(futures)

Con el job.sh configurado se debe dirigir al Slurm Manager Queue, el cuál es una herramienta brindada por el Jupyter en ejecución, y dentro del Manager dirigirse a la pestaña "Submit Jobs", en esta pestaña seleccionar el archivo job.sh, luego clic en "Submit Job" y esperar que el archivo se ejecute y produzca las salidas en el archivo result.out.
