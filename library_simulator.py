import simpy
import numpy as np
import csv

class LibrarySimulator:
    def __init__(self, mean_arrival_rate, mean_service_time, convergence_threshold, simulation_time, num_librarians, max_wait_time):
        self.mean_arrival_rate = mean_arrival_rate
        self.mean_service_time = mean_service_time
        self.convergence_threshold = convergence_threshold
        self.simulation_time = simulation_time
        self.num_librarians = num_librarians
        self.max_wait_time = max_wait_time

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
            if server.count == 0 and len(server.queue) == 0:
                # If all servers are idle and there is no queue, add idle time
                idle_time = env.now - last_service_time[0]
                self.idle_times.append(idle_time)
            self.customers_in_queue.append(arrival_time)
            env.process(self.customer_service(env, server, arrival_time, last_service_time))
            env.process(self.check_wait_time(env, arrival_time))
            self.queue_lengths.append(len(server.queue))
            self.total_customers_served += 1

    def customer_service(self, env, server, arrival_time, last_service_time):
        """Customer service process"""
        with server.request() as req:
            yield req
            wait_time = env.now - arrival_time
            self.wait_times.append(wait_time)

            yield env.timeout(np.random.exponential(self.mean_service_time))
            last_service_time[0] = env.now
            print(f"Customer served at {env.now:.2f} minutes")

            # Remove customer from the queue tracking list
            if arrival_time in self.customers_in_queue:
                self.customers_in_queue.remove(arrival_time)

    def check_wait_time(self, env, arrival_time):
        """Check if a customer leaves after waiting too long"""
        while True:
            yield env.timeout(1)  # Check every minute
            if env.now - arrival_time > self.max_wait_time:
                if arrival_time in self.customers_in_queue:
                    self.customers_left += 1
                    self.customers_in_queue.remove(arrival_time)
                    print(f"Customer left at {env.now:.2f} minutes after waiting too long")
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

def main():
    num_librarians = 2  # Number of librarians

    simulator = LibrarySimulator(
        mean_arrival_rate=8,
        mean_service_time=5,
        convergence_threshold=0.01,
        simulation_time=8 * 60,  # in minutes, e.g., 8 hours
        num_librarians=num_librarians,
        max_wait_time=5  # Maximum wait time in minutes before a customer leaves
    )

    all_customers_served = []

    with open('simulation_statistics.csv', mode='w', newline='') as file:
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

    print("Simulation statistics saved to 'simulation_statistics.csv'")

if __name__ == "__main__":
    main()
