from threading import Thread

def func1():
    print('worker 1')

def func2():
    print("worker 2")

if __name__ == '__main__':
    a = Thread(target = func1)
    b = Thread(target = func2)
    a.start()
    b.start()