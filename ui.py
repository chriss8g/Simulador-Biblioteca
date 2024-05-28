import os

class QueueRepresentation:
    def print(self, queue):
        os.system('clear')

        for _ in range(3):
            print("\n")

        s = "               # "
        for _ in queue:
            s = s + "$"
        print(s)

        for _ in range(2):
            print("\n")