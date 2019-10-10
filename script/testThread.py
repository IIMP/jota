from datetime import datetime
import threading
import time
def subThread(is_stop):
    while not is_stop.is_set():
        print("subThread is running")
        time.sleep(10)
        print("subThread ended correctly")

def controlThread(main_control):
    print("controlThread is running")
    is_stop=threading.Event()
    t=threading.Thread(target=subThread,args=(is_stop,),daemon=True)
    t.start()
    while not main_control.is_set():
        time.sleep(1)
    is_stop.set()

if __name__ == '__main__':
    for i in range(5):
        main_control=threading.Event()
        a=threading.Thread(target=controlThread,args=(main_control,))
        a.start()
        time.sleep(5)
        main_control.set()



