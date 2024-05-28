import threading
import time
import random
import numpy as np
import csv
from ui import QueueRepresentation
import os


class LibrarySimulation:
    def __init__(self, max_time=30, ave_clients_distribution=2, ave_student_distribution=3,
                 clients_distribution='Poisson', student_distribution='Exponential'):
        self.max_time = max_time
        self.ave_clients_distribution = ave_clients_distribution
        self.ave_student_distribution = ave_student_distribution
        self.clients_distribution = clients_distribution
        self.student_distribution = student_distribution

        self.start_time = time.time()
        self.clients_waiting = []
        self.sizes_queue = []
        self.client_id = 0

        self.simulation_running = True
        self.lock = threading.Lock()

        self.interface = QueueRepresentation()

    def client_arrive(self):
        '''
        Simulates client arrival with an average time specified by `ave_clients_distribution`.
        '''
        while time.time() - self.start_time < self.max_time:
            arrive_time = self.get_random_time(
                self.clients_distribution, self.ave_clients_distribution)
            time.sleep(arrive_time)

            with self.lock:
                self.client_id += 1
                self.clients_waiting.append(self.client_id)

                self.interface.print(self.clients_waiting, time.time() - self.start_time, self.max_time)
                print(f'Llegó el cliente {self.client_id}.')

        self.simulation_running = False

    def client_attention(self, librarian_id):
        '''
        Simulates client attention one by one by a librarian.
        '''
        while time.time() - self.start_time < self.max_time:# or len(self.clients_waiting) != 0:
            if len(self.clients_waiting) == 0:
                continue

            atention_time = self.get_random_time(
                self.student_distribution, self.ave_student_distribution)

            with self.lock:
                if len(self.clients_waiting) != 0:
                    client = self.clients_waiting.pop(0)
                    print(f'Cliente {client} siendo atendido por bibliotecario {librarian_id}')
                    self.sizes_queue.append(len(self.clients_waiting))

            time.sleep(atention_time)

            self.interface.print(self.clients_waiting, time.time() - self.start_time, self.max_time)


    def get_random_time(self, distribution, ave):
        if distribution == 'Poisson':
            return np.random.poisson(ave)
        elif distribution == 'Exponential':
            return random.expovariate(1/ave)
        else:
            raise ValueError("Distribution not supported")

    def run_simulation(self):
        arrive_thread = threading.Thread(target=self.client_arrive)
        attention_thread = threading.Thread(target=self.client_attention, args=(1,))
        # attention2_thread = threading.Thread(target=self.client_attention, args=(2,))
        # attention3_thread = threading.Thread(target=self.client_attention, args=(3,))

        arrive_thread.start()
        attention_thread.start()
        # attention2_thread.start()
        # attention3_thread.start()

        arrive_thread.join()
        attention_thread.join()
        # attention2_thread.join()
        # attention3_thread.join()

        if self.sizes_queue:
            max_size_queue = max(self.sizes_queue)
            min_size_queue = min(self.sizes_queue)
            ave_size_queue = sum(self.sizes_queue) / len(self.sizes_queue)
        else:
            max_size_queue = min_size_queue = ave_size_queue = 0

        os.system('clear')
        print(f'\n\nEl tamaño máximo que tuvo la cola fue: {max_size_queue}')
        print(f'El tamaño mínimo que tuvo la cola fue: {min_size_queue}')
        print(f'El tamaño promedio que tuvo la cola fue: {ave_size_queue}')

        data = [self.clients_distribution, self.ave_clients_distribution, self.student_distribution,
                self.ave_student_distribution, max_size_queue, min_size_queue, ave_size_queue]

        with open('data.csv', mode='a', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(data)

        print("Fila agregada exitosamente.")


if __name__ == '__main__':
    simulation = LibrarySimulation()
    simulation.run_simulation()
