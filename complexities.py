import random
import numpy as np

class Complexities:

    def get_random_time(self, distribution, ave):
        if distribution == 'Poisson':
            return np.random.poisson(ave)
        elif distribution == 'Exponential':
            return random.expovariate(1 / ave)
        else:
            raise ValueError("Distribution not supported")
        
    def assign_complexity(self):
        '''
        Assigns a complexity level to a client.
        '''
        complexities = ['Rápido', 'Medio', 'Lento']
        return random.choice(complexities)

    def get_attention_time_based_on_complexity(self, complexity, distribution, ave):
        '''
        Returns attention time based on the complexity level.
        '''
        if complexity == 'Rápido':
            return self.get_random_time(distribution, ave-1)  # Consultas rápidas
        elif complexity == 'Medio':
            return self.get_random_time(distribution, ave)  # Consultas de complejidad media
        elif complexity == 'Lento':
            return self.get_random_time(distribution, ave+1)  # Consultas lentas
