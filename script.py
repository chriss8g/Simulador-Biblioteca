import simpy
import numpy as np

def usuario(env):
    # Simula el tiempo que un usuario pasa en la biblioteca
    yield env.timeout(np.random.exponential(5))  # Tiempo de servicio de 5 minutos

def llegada(env, biblioteca):
    i = 0
    j = 0
    while True:
        # Genera el tiempo hasta la próxima llegada según una distribución de Poisson
        tiempo_hasta_llegada = np.random.poisson(8)  # Media de 8 llegadas por hora
        yield env.timeout(tiempo_hasta_llegada)
        print(f'{env.now} Llega un nuevo usuario ',i)
        i=i+1
        with biblioteca.request() as req:
            yield req
            print(f'{env.now} El usuario empieza a ser atendido ',j)
            j = j+1
            yield env.process(usuario(env))
            print(f'{env.now} El usuario fue atendido a ser atendido')

def setup():
    # Configura el entorno de simulación
    env = simpy.Environment()
    
    # Define la capacidad del mostrador
    capacidad_mostrador = 1
    
    # Crea el recurso 'biblioteca'
    biblioteca = simpy.Resource(env, capacity=capacidad_mostrador)
    
    # Inicia la llegada de usuarios
    env.process(llegada(env, biblioteca))
    
    return env, biblioteca

if __name__ == '__main__':
    env, biblioteca = setup()
    env.run(until=5*60)  # Ejecuta la simulación durante 24 horas