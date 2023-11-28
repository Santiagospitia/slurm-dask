#!/usr/bin/env python3
from dask.distributed import Client, get_worker
from dask_jobqueue import SLURMCluster
import time

# Configura el clúster SLURM y el cliente Dask
cluster = SLURMCluster(cores=1, memory='1GB')
client = Client(cluster)

# Escala el clúster
cluster.scale(4)

# Definir una función simple que realiza una tarea y muestra en qué nodo se está ejecutando
def simple_task(id):
    time.sleep(2)
    import socket
    worker = get_worker()
    node_name = socket.gethostname()
    return f"Hello from node {node_name}, worker {worker.id}"

# Crea una lista de futuros para ejecutar la tarea en diferentes nodos
futures = client.map(simple_task, range(10))

# Espera a que se completen las tareas
results = client.gather(futures)

# Imprime los resultados
for result in results:
    print(result)