import threading
import time

num = 1
arr = []
total_time = 20
acum_time = 0

def add():
    global num
    global arr

    while acum_time < total_time:
        time.sleep(2)
        print('')
        print(f'add {num} a {arr}')
        arr.append(num)
        num+=1

def remove():
    global num
    global arr
    global acum_time

    while acum_time < total_time:
        if len(arr) == 0:
            continue
        time.sleep(4)
        acum_time += 4

        print('')
        print(f'remove {arr[0]}')
        arr.pop(0)

hilo_tarea_1 = threading.Thread(target=add)
hilo_tarea_2 = threading.Thread(target=remove)

hilo_tarea_1.start()
hilo_tarea_2.start()

hilo_tarea_1.join()
hilo_tarea_2.join()