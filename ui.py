import os

class QueueRepresentation:
    def print(self, queue, time, maxtime):
        os.system('clear')

        print(f'{int(time)}/{maxtime}')
        for _ in range(2):
            print("\n")

        s = "               # "
        for _ in queue:
            s = s + "$"
        print(s)

        for _ in range(2):
            print("\n")
        print(f'Cola: {queue}')
