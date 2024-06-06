import threading
import time
import random
import numpy as np
import csv
from ui import QueueRepresentation
from complexities import Complexities
import os


class LibrarySimulation:
    def __init__(self, max_time=30, ave_clients_distribution=1, ave_student_distribution=3,
                 clients_distribution='Poisson', student_distribution='Exponential', libraries_count=3, sjf=False):
        self.max_time = max_time
        self.ave_clients_distribution = ave_clients_distribution
        self.ave_student_distribution = ave_student_distribution
        self.clients_distribution = clients_distribution
        self.student_distribution = student_distribution
        self.libraries_count = libraries_count
        self.sjf = sjf
        self.threads = []

        self.start_time = time.time()
        self.clients_waiting = []
        self.sizes_queue = []
        self.client_id = 0
        self.extra_info = ""

        self.lock = threading.Lock()
        self.complexities = Complexities()

        self.interface = QueueRepresentation()

        self.wait_times = []
        self.attention_times = []
        self.total_clients_attended = 0
        self.total_client_lose = 0

    def client_arrive(self):
        '''
        Simulates client arrival with an average time specified by `ave_clients_distribution`.
        '''
        while time.time() - self.start_time < self.max_time:
            arrive_time = self.complexities.get_random_time(self.clients_distribution, self.ave_clients_distribution)
            time.sleep(arrive_time)

            with self.lock:
                self.client_id += 1
                arrival_time = time.time() - self.start_time
                complexity = self.complexities.assign_complexity()
                self.clients_waiting.append((self.client_id, arrival_time, complexity))

                self.interface.print([client[0] for client in self.clients_waiting], time.time() - self.start_time, self.max_time, self.extra_info)

    def client_attention(self, librarian_id):
        '''
        Simulates client attention one by one by a librarian.
        '''
        while time.time() - self.start_time < self.max_time:
            with self.lock:

                if len(self.clients_waiting) == 0:
                    continue

                self.check_long_wait()

                n = 0
                if self.sjf:
                    flag = False
                    for number, i in enumerate(self.clients_waiting):
                        if(i[2] == "Rápido"):
                            n = number
                            break
                        if(i[2] == "Medio" and not flag):
                            n = number
                            flag = True
                client_id, arrival_time, complexity = self.clients_waiting.pop(n)
                
                wait_time = time.time() - self.start_time - arrival_time
                self.wait_times.append(wait_time)

                self.extra_info += '\n'
                self.extra_info += f'⏩ Cliente {client_id}\n'
                self.extra_info += f'⏩ Tipo {complexity}\n'
                self.extra_info += f'⏩ Atendido por {librarian_id}\n'

                attention_time = self.complexities.get_attention_time_based_on_complexity(complexity, self.student_distribution, self.ave_student_distribution)
                self.attention_times.append(attention_time)

            time.sleep(attention_time)
            
            with self.lock:   
                self.sizes_queue.append(len(self.clients_waiting))
                self.total_clients_attended += 1


            self.extra_info = ""

            self.interface.print([client[0] for client in self.clients_waiting], time.time() - self.start_time, self.max_time, self.extra_info)

    def check_long_wait(self):

        i = 0
        while i < len(self.clients_waiting):
            client_id, arrival_time, complexity = self.clients_waiting[i]
            wait_time = time.time() - self.start_time - arrival_time
            if(wait_time >= 5):
                self.clients_waiting.pop(i)
                self.total_client_lose += 1
                i -= 1
                print(f'{client_id} is left ')
            
            i+=1

        self.interface.print([client[0] for client in self.clients_waiting], time.time() - self.start_time, self.max_time, self.extra_info)

    def run_simulation(self):
        arrive_thread = threading.Thread(target=self.client_arrive)

        for i in range(self.libraries_count):
            self.threads.append(threading.Thread(target=self.client_attention, args=(i,)))

        arrive_thread.start()
        for i in range(self.libraries_count):
            self.threads[i].start()

        arrive_thread.join()
        
        for i in range(self.libraries_count):
            self.threads[i].join()

        if self.sizes_queue:
            max_size_queue = max(self.sizes_queue)
            ave_size_queue = sum(self.sizes_queue) / len(self.sizes_queue)
        else:
            max_size_queue = ave_size_queue = 0

        os.system('clear')
        print(f'\n\n📌El tamaño máximo que tuvo la cola fue: {max_size_queue}')
        print(f'📌El tamaño promedio que tuvo la cola fue: {ave_size_queue}')

        total_wait_time = sum(self.wait_times) + 5 * self.total_client_lose
        total_attention_time = sum(self.attention_times)
        ave_wait_time = total_wait_time / (self.total_clients_attended + self.total_client_lose) if self.total_clients_attended > 0 else 0
        ave_attention_time = total_attention_time / self.total_clients_attended if self.total_clients_attended > 0 else 0

        print(f'📌El tiempo de espera promedio fue: {ave_wait_time}')
        print(f'📌El tiempo de atención promedio fue: {ave_attention_time}')
        print(f'📌Número total de clientes atendidos: {self.total_clients_attended}')
        print(f'📌Número total de clientes perdidos: {self.total_client_lose}')

        data = [
            round(self.ave_clients_distribution, 2),
            round(self.ave_student_distribution, 2),
            max_size_queue,
            round(ave_size_queue,2),
            round(ave_wait_time, 2),
            round(ave_attention_time, 2),
            self.total_clients_attended,
            self.libraries_count,
            self.sjf,
            self.total_client_lose
        ]

        with open('data.csv', mode='a', newline='') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(data)

        print("✅Fila agregada exitosamente.")


if __name__ == '__main__':

    
    libraries_count_distribution = [i+1 for i in range(8)]
    weights = [0.3, 0.2, 0.2, 0.1, 0.05, 0.05, 0.05, 0.05]

    for i in range(50):
        x = random.choices(libraries_count_distribution, weights)[0]
        simulation = LibrarySimulation(libraries_count=x, sjf=(np.random.uniform(0,1)>0.5), ave_clients_distribution=np.random.uniform(0.5, 1.5), ave_student_distribution=np.random.uniform(1,5))
        simulation.run_simulation()
