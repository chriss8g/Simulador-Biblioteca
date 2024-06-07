import simpy
import numpy as np
import csv

# System parameters
MEAN_ARRIVAL_RATE = 8  # mean arrivals per hour
MEAN_SERVICE_TIME = 5  # mean service time in minutes
CONVERGENCE_THRESHOLD = 0.01  # Convergence threshold for stopping criterion
SIMULATION_TIME = 8 * 60  # in minutes, e.g., 8 hours

def customer_arrival(env, server, last_service_time):
    """Customer arrival event generator"""
    global total_customers_served
    while True:
        yield env.timeout(np.random.exponential(60 / MEAN_ARRIVAL_RATE))
        if server.count == 0 and len(server.queue) == 0:
            # If the server is idle and there is no queue, add idle time
            idle_time = env.now - last_service_time[0]
            idle_times.append(idle_time)
        env.process(customer_service(env, server, env.now, last_service_time))
        queue_lengths.append(len(server.queue))
        total_customers_served += 1

def customer_service(env, server, arrival_time, last_service_time):
    """Customer service process"""
    with server.request() as req:
        yield req
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)

        yield env.timeout(np.random.exponential(MEAN_SERVICE_TIME))
        last_service_time[0] = env.now
        print(f"Customer served at {env.now:.2f} minutes")

def run_simulation():
    global wait_times, idle_times, queue_lengths, total_customers_served
    wait_times = []
    idle_times = []
    queue_lengths = []
    total_customers_served = 0

    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)  # Only one server at the desk
    last_service_time = [0]  # Time when the server finished serving the last customer

    # Start the customer arrival generator
    env.process(customer_arrival(env, server, last_service_time))

    # Run the simulation for a defined time (e.g., 8 hours)
    env.run(until=SIMULATION_TIME)

def main():
    all_customers_served = []

    with open('simulation_statistics.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Total Customers Served', 'Max Wait Time', 'Mean Wait Time', 
                         'Max Idle Time', 'Min Idle Time', 'Mean Idle Time', 
                         'Max Queue Length', 'Mean Queue Length'])

        while True:
            run_simulation()
            all_customers_served.append(total_customers_served)

            max_wait_time = round(max(wait_times), 2) if wait_times else 0
            mean_wait_time = round(np.mean(wait_times), 2) if wait_times else 0

            max_idle_time = round(max(idle_times), 2) if idle_times else 0
            min_idle_time = round(min(idle_times), 2) if idle_times else 0
            mean_idle_time = round(np.mean(idle_times), 2) if idle_times else 0

            max_queue_length = max(queue_lengths) if queue_lengths else 0
            mean_queue_length = round(np.mean(queue_lengths), 2) if queue_lengths else 0

            writer.writerow([
                total_customers_served,
                max_wait_time, mean_wait_time,
                max_idle_time, min_idle_time, mean_idle_time,
                max_queue_length, mean_queue_length
            ])

            if len(all_customers_served) > 1:
                mean_served = np.mean(all_customers_served)
                std_dev_served = np.std(all_customers_served, ddof=1)
                relative_error = std_dev_served / np.sqrt(len(all_customers_served)) / mean_served
                if relative_error < CONVERGENCE_THRESHOLD:
                    break

    print("Simulation statistics saved to 'simulation_statistics.csv'")

if __name__ == "__main__":
    main()
