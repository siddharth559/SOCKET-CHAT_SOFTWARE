from logging import exception
import socket as sk
import threading as th
import _thread
import tkinter as tk
from trace import Trace

root= tk.Tk()



A = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
PORT = 52345
HOST = "192.168.0.103"
A.connect((HOST,PORT))
OPEN = True
LOCK = th.Lock()

SCROLLBAR = tk.Scrollbar(root)
MESSAGES = tk.Listbox(root, yscrollcommand=SCROLLBAR.set)
SCROLLBAR.config(command=MESSAGES.yview)
ENTRY = tk.Entry(root)
SEND = tk.Button(root, text = 'send')
DISCONNECT = tk.Button(root, text = 'disconnect')

MESSAGES.grid(row = 0,column=0)
SCROLLBAR.grid(row = 0,column=1,sticky=tk.NS)
ENTRY.grid(row = 1,column=0)
SEND.grid(row = 1,column=1)
DISCONNECT.grid(row = 2,column=0)
MESSAGES.insert(tk.END,A.recv(1024).decode())

#A.sendall(input('enter name: ').encode())

def print_recv():
    while OPEN == True:
        data = A.recv(1024)
        if not data or data.decode == '':
            LOCK.release()
            break
        MESSAGES.insert(tk.END,data.decode())
t1 = th.Thread(target=print_recv)

def send_but():
    data = ENTRY.get()
    A.sendall(data.encode())
def discon():
    global OPEN
    OPEN = 0
    A.close()
    

SEND.config(command = send_but)
DISCONNECT.config(command = discon)

LOCK.acquire()
t1.daemon = 1
t1.start()
root.mainloop()
print(OPEN, t1.is_alive())
OPEN = False
try:
    A.close()
except:
    with Exception as e:
        print(e)