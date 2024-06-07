import simpy
import numpy as np
import csv
import random

class LibrarySimulator:
    def __init__(self, mean_arrival_rate, mean_service_time, convergence_threshold, simulation_time, num_librarians, max_wait_time, scheduling_policy='FIFO'):
        self.mean_arrival_rate = mean_arrival_rate
        self.mean_service_time = mean_service_time
        self.convergence_threshold = convergence_threshold
        self.simulation_time = simulation_time
        self.num_librarians = num_librarians
        self.max_wait_time = max_wait_time
        self.scheduling_policy = scheduling_policy

        # Initialize statistics
        self.wait_times = []
        self.idle_times = []
        self.queue_lengths = []
        self.total_customers_served = 0
        self.customers_left = 0
        self.customers_in_queue = []

    def customer_arrival(self, env, server, last_service_time):
        """Customer arrival event generator"""
        while True:
            yield env.timeout(np.random.exponential(60 / self.mean_arrival_rate))
            arrival_time = env.now
            customer_type = random.choice(['Slow', 'Normal', 'Fast'])  # Randomly assign customer type

            if server.count == 0 and len(server.queue) == 0:
                # If all servers are idle and there is no queue, add idle time
                idle_time = env.now - last_service_time[0]
                self.idle_times.append(idle_time)

            self.customers_in_queue.append((arrival_time, customer_type))
            env.process(self.customer_service(env, server, last_service_time))
            env.process(self.check_wait_time(env, arrival_time, server))
            self.queue_lengths.append(len(server.queue))
            self.total_customers_served += 1

    def customer_service(self, env, server, last_service_time):
        """Customer service process"""
        if self.scheduling_policy == 'SJF':
            # Prioritize Fast customers first, then Normal, then Slow
            self.customers_in_queue.sort(key=lambda x: (x[1] != 'Fast', x[1] != 'Normal', x[0]))  # Sort by type and then by arrival time

        with server.request() as req:
            yield req

            if self.customers_in_queue:
                arrival_time, customer_type = self.customers_in_queue.pop(0)
                wait_time = env.now - arrival_time
                self.wait_times.append(wait_time)

                if customer_type == 'Slow':
                    service_time = np.random.exponential(self.mean_service_time + 1)
                elif customer_type == 'Fast':
                    service_time = np.random.exponential(self.mean_service_time - 1)
                else:
                    service_time = np.random.exponential(self.mean_service_time)

                yield env.timeout(service_time)
                last_service_time[0] = env.now
                print(f"Customer ({customer_type}) served at {env.now:.2f} minutes")

    def check_wait_time(self, env, arrival_time, server):
        """Check if a customer leaves after waiting too long"""
        while True:
            yield env.timeout(1)  # Check every minute
            if env.now - arrival_time > self.max_wait_time:
                for t, c in self.customers_in_queue:
                    if t == arrival_time:
                        self.customers_left += 1
                        print(f"Customer ({c}) left at {env.now:.2f} minutes after waiting too long")
                        # Remove the customer from the queue
                        self.customers_in_queue.remove((t, c))
                break

    def run_simulation(self):
        self.wait_times = []
        self.idle_times = []
        self.queue_lengths = []
        self.total_customers_served = 0
        self.customers_left = 0
        self.customers_in_queue = []

        env = simpy.Environment()
        server = simpy.Resource(env, capacity=self.num_librarians)  # Multiple servers at the desk
        last_service_time = [0]  # Time when the last server finished serving a customer

        # Start the customer arrival generator
        env.process(self.customer_arrival(env, server, last_service_time))

        # Run the simulation for a defined time (e.g., 8 hours)
        env.run(until=self.simulation_time)

    def get_statistics(self):
        max_wait_time = round(max(self.wait_times), 2) if self.wait_times else 0
        mean_wait_time = round(np.mean(self.wait_times), 2) if self.wait_times else 0

        max_idle_time = round(max(self.idle_times), 2) if self.idle_times else 0
        min_idle_time = round(min(self.idle_times), 2) if self.idle_times else 0
        mean_idle_time = round(np.mean(self.idle_times), 2) if self.idle_times else 0

        max_queue_length = max(self.queue_lengths) if self.queue_lengths else 0
        mean_queue_length = round(np.mean(self.queue_lengths), 2) if self.queue_lengths else 0

        return [
            self.total_customers_served,
            max_wait_time, mean_wait_time,
            max_idle_time, min_idle_time, mean_idle_time,
            max_queue_length, mean_queue_length,
            self.customers_left
        ]

def run_simulations():
    scheduling_policies = ['FIFO', 'SJF']
    num_librarians_options = [1, 2, 3]

    for policy in scheduling_policies:
        for num_librarians in num_librarians_options:
            # Vary parameters slightly for each simulation
            mean_arrival_rate = 8 + np.random.uniform(-1, 1)
            mean_service_time = 5 + np.random.uniform(-1, 1)
            max_wait_time = 5 + np.random.uniform(-1, 1)

            simulator = LibrarySimulator(
                mean_arrival_rate=mean_arrival_rate,
                mean_service_time=mean_service_time,
                convergence_threshold=0.01,
                simulation_time=8 * 60,  # in minutes, e.g., 8 hours
                num_librarians=num_librarians,
                max_wait_time=max_wait_time,  # Maximum wait time in minutes before a customer leaves
                scheduling_policy=policy  # FIFO or SJF
            )

            all_customers_served = []

            filename = f'simulation_statistics_{policy}_{num_librarians}_librarians.csv'
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Total Customers Served', 'Max Wait Time', 'Mean Wait Time', 
                                 'Max Idle Time', 'Min Idle Time', 'Mean Idle Time', 
                                 'Max Queue Length', 'Mean Queue Length', 'Customers Left'])

                while True:
                    simulator.run_simulation()
                    all_customers_served.append(simulator.total_customers_served)
                    stats = simulator.get_statistics()
                    writer.writerow(stats)

                    if len(all_customers_served) > 1:
                        mean_served = np.mean(all_customers_served)
                        std_dev_served = np.std(all_customers_served, ddof=1)
                        relative_error = std_dev_served / np.sqrt(len(all_customers_served)) / mean_served
                        if relative_error < simulator.convergence_threshold:
                            break

            print(f"Simulation statistics saved to '{filename}'")

if __name__ == "__main__":
    run_simulations()
