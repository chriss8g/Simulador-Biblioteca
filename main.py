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

        self.wait_times = []
        self.attention_times = []
        self.total_clients_attended = 0

    def client_arrive(self):
        '''
        Simulates client arrival with an average time specified by `ave_clients_distribution`.
        '''
        while time.time() - self.start_time < self.max_time:
            arrive_time = self.get_random_time(self.clients_distribution, self.ave_clients_distribution)
            time.sleep(arrive_time)

            with self.lock:
                self.client_id += 1
                arrival_time = time.time() - self.start_time
                complexity = self.assign_complexity()
                self.clients_waiting.append((self.client_id, arrival_time, complexity))

                self.interface.print([client[0] for client in self.clients_waiting], time.time() - self.start_time, self.max_time)

        self.simulation_running = False

    def assign_complexity(self):
        '''
        Assigns a complexity level to a client.
        '''
        complexities = ['rápido', 'medio', 'lento']
        return random.choice(complexities)

    def get_attention_time_based_on_complexity(self, complexity):
        '''
        Returns attention time based on the complexity level.
        '''
        if complexity == 'rápido':
            return random.uniform(1, 2)  # Consultas rápidas
        elif complexity == 'medio':
            return random.uniform(3, 5)  # Consultas de complejidad media
        elif complexity == 'lento':
            return random.uniform(6, 10)  # Consultas lentas

    def client_attention(self, librarian_id):
        '''
        Simulates client attention one by one by a librarian.
        '''
        while time.time() - self.start_time < self.max_time:
            if len(self.clients_waiting) == 0:
                continue

            with self.lock:
                if len(self.clients_waiting) != 0:
                    client_id, arrival_time, complexity = self.clients_waiting.pop(0)
                    wait_time = time.time() - self.start_time - arrival_time
                    self.wait_times.append(wait_time)
                    self.total_clients_attended += 1
                    print(f'Cliente {client_id} tipo {complexity} atendido por {librarian_id}')
                    self.sizes_queue.append(len(self.clients_waiting))

            attention_time = self.get_attention_time_based_on_complexity(complexity)
            time.sleep(attention_time)
            self.attention_times.append(attention_time)

            self.interface.print([client[0] for client in self.clients_waiting], time.time() - self.start_time, self.max_time)
            
    def get_random_time(self, distribution, ave):
        if distribution == 'Poisson':
            return np.random.poisson(ave)
        elif distribution == 'Exponential':
            return random.expovariate(1 / ave)
        elif distribution == 'Normal':
            return max(0, np.random.normal(ave, ave / 3))  # Evitar tiempos negativos
        elif distribution == 'Uniform':
            return np.random.uniform(ave / 2, ave * 2)
        elif distribution == 'Gamma':
            shape = 2
            scale = ave / shape
            return np.random.gamma(shape, scale)
        elif distribution == 'Triangular':
            return np.random.triangular(ave / 2, ave, ave * 2)
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

        total_wait_time = sum(self.wait_times)
        total_attention_time = sum(self.attention_times)
        ave_wait_time = total_wait_time / self.total_clients_attended if self.total_clients_attended > 0 else 0
        ave_attention_time = total_attention_time / self.total_clients_attended if self.total_clients_attended > 0 else 0

        print(f'El tiempo de espera promedio fue: {ave_wait_time}')
        print(f'El tiempo de atención promedio fue: {ave_attention_time}')
        print(f'Número total de clientes atendidos: {self.total_clients_attended}')

        data = [
            self.clients_distribution, self.ave_clients_distribution, self.student_distribution,
            self.ave_student_distribution, max_size_queue, min_size_queue, ave_size_queue,
            ave_wait_time, ave_attention_time, self.total_clients_attended
        ]

        with open('data.csv', mode='a', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(data)

        print("Fila agregada exitosamente.")


if __name__ == '__main__':
    simulation = LibrarySimulation(max_time=30, 
        ave_clients_distribution=2, 
        ave_student_distribution=3,  
        clients_distribution='Gamma', 
        student_distribution='Uniform' 
    )

    simulation.run_simulation()