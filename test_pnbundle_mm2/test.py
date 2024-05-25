from playsound import playsound



import threading

def k():
    threading.Thread(target=lambda: playsound("beep.wav")).start()

import time

for i in range(5):
    k()
    time.sleep(1)

print(1)