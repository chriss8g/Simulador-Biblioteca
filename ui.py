import os

class QueueRepresentation:
    def print(self, queue, time, max_time, extra):
        os.system('clear')

        print(f'⏰: {int(time)}/{max_time}')
        for _ in range(2):
            print("\n")

        s = "👦📚| "
    
        for _ in queue:
            s = s + '🏃'
        print(s)

        for _ in range(2):
            print("\n")
        print(f'Cola📋: {queue}')

        print(extra)
