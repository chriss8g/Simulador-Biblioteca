import threading
import time
import random
import numpy as np
import csv

# Variables a modificar en la simulación

max_time = 30
'''Tiempo que debe durar la simulación'''
ave_clients_distribution = 3
'''Tiempo promedio en que los clientes llegan'''
ave_student_distribution = 3
'''Tiempo promedio en que el bibliotecario atiende a los clientes'''
clients_distribution = 'Poisson'
'''Distribución con la que llegan los clientes a la biblioteca'''
student_distribution = 'Exponential'
'''Distribución con la que los clientes son atendidos'''


# Variables útiles en la simulación
acum_time = 0
'''Tiempo acumulado'''
client_id = 0
'''Identificador del cliente'''
clients_waiting = [] 
'''Clientes que quedan en espera'''
sizes_queue = []
'''Tamaños de la cola al terminar de atender a un cliente'''


def client_arrive():
    '''
    Simula la llegada con media = `ave_clients_distribution` de los clientes a la biblioteca
    '''

    global client_id
    global clients_waiting
    global ave_clients_distribution
    global clients_distribution

    while acum_time < max_time:
        # Genera un número aleatorio que sigue una distribución y con la media especificada
        arrive_time = getRandomTime(clients_distribution, ave_clients_distribution)
        time.sleep(arrive_time)
        
        client_id += 1
        clients_waiting.append(client_id)

        # Imprime "Llegó" después de un tiempo aleatorio que sigue la distribución exponencial
        print(f'Llegó el ciente {client_id}. Cola: {clients_waiting}')
        
def client_atention():
    '''
    Simula la atención de los clientes de uno en uno por parte de un bibliotecario
    '''

    global clients_waiting
    global ave_student_distribution
    global acum_time
    global sizes_queue
    global student_distribution
    
    while acum_time < max_time or len(clients_waiting) > 0:

        # Se requiere esta verificación para no salir del while
        if len(clients_waiting) == 0:
            continue
    
        # Genera un número aleatorio que sigue una distribución exponencial con la media especificada
        atention_time = getRandomTime(student_distribution, ave_student_distribution)
        # Actualiza el tiempo acumulado y el cliente que está llegando
        acum_time += atention_time

        print(f'El ciente {clients_waiting[0]} está siendo atendido')
        time.sleep(atention_time)
        print(f'El ciente {clients_waiting[0]} fue atendido')

        # Extraer el cliente atendido de la cola
        clients_waiting.pop(0)

        # Añadir el tamaño actual de la cola al array de los tamaños
        sizes_queue.append(len(clients_waiting))
        
def getRandomTime(distribution, ave):
    if distribution == 'Poisson':
        return np.random.poisson(ave)
    elif distribution == 'Exponential':
        return random.expovariate(1/ave)


if __name__ == '__main__':
    hilo_tarea_1 = threading.Thread(target=client_arrive)
    hilo_tarea_2 = threading.Thread(target=client_atention)

    hilo_tarea_1.start()
    hilo_tarea_2.start()

    hilo_tarea_1.join()
    print(f'El tiempo de llegada de clientes terminó con {len(clients_waiting)} clientes en la cola')
    hilo_tarea_2.join()

    # Datos para analizar
    max_size_queue = max(sizes_queue)
    min_size_queue = min(sizes_queue)
    ave_size_queue = sum(sizes_queue)/len(sizes_queue)

    print(f'\n\nEl tamaño máximo que tuvo la cola fue: {max_size_queue}')
    print(f'El tamaño mínimo que tuvo la cola fue: {min_size_queue}')
    print(f'El tamaño promedio que tuvo la cola fue: {ave_size_queue}')

    data = [clients_distribution, ave_clients_distribution, student_distribution, ave_student_distribution, max_size_queue, min_size_queue, ave_size_queue]

    # Modo de apertura del archivo: 'w' para escritura, 'a' para anexar
    modo_apertura = 'a'

    # Abre el archivo CSV en el modo especificado
    with open('data.csv', mode=modo_apertura, newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        
        # Agrega una nueva fila al final del archivo CSV
        writer.writerow(data)

    print("Fila agregada exitosamente.")