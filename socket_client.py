from tkinter import filedialog
from tkinter import ttk
import time
import os
import sys 
import socket as sk
import threading as th
import _thread
import tkinter as tk
from trace import Trace

root= tk.Tk()

OSs={
    'darwin' : ('Mac','/'),
     'linux': ('Linux','/'),
     'win' : ('Windows','\\')
     }

OS_NAME = sys.platform
for i in OSs:
    if i in OS_NAME:
        OS_NAME,sepr = OSs[i][0],OSs[i][1]

A = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
PORT = 52345
HOST = "192.168.1.100"
A.connect((HOST,PORT))
OPEN = True
LOCK = th.Lock()
FLAG = 1

SCROLLBAR = tk.Scrollbar(root)
MESSAGES = tk.Canvas(root, bg='white', width=130, yscrollcommand=SCROLLBAR.set)
SCROLLBAR.config(command=MESSAGES.yview)
MESSAGES.bind_all('<MouseWheel>', lambda event: MESSAGES.yview_scroll(int(-1*(event.delta/120)), "units")) 
PROGRESS = ttk.Progressbar(root)
#MESSAGES = tk.Listbox(root, yscrollcommand=SCROLLBAR.set,width = 90)
#SCROLLBAR.config(command=MESSAGES.yview)
ENTRY = tk.Entry(root , width = 70)
SEND = tk.Button(root, text = 'send')
DISCONNECT = tk.Button(root, text = 'disconnect')
ATTACH = tk.Button(root,text = 'attach')

SCROLLBAR.grid(row = 0,column=2,sticky=tk.NS)
MESSAGES.grid(row = 0,column=0,columnspan=2,sticky=tk.NSEW)
ENTRY.grid(row = 1,column=0,sticky=tk.NSEW)
SEND.grid(row = 1,column=1,columnspan=2,sticky=tk.NSEW)
DISCONNECT.grid(row = 2,column=0,sticky=tk.NSEW)
ATTACH.grid(row = 2,column = 1,columnspan=2,sticky=tk.NSEW)

FRAME=tk.Frame(MESSAGES,bg='white')            
rt=MESSAGES.create_window(0,0,anchor=tk.N+tk.W,window=FRAME)
MESSAGES.update()
MESSAGES.config(scrollregion=MESSAGES.bbox('all'))
welcome = tk.Label(FRAME,text = A.recv(1024).decode()).pack()

#A.sendall(input('enter name: ').encode())

def REQUEST():
    pass
def print_recv():
    while OPEN == True:
        data = A.recv(1024)
        if not data or data.decode == '':
            LOCK.release()
            break
        try:
            tk.Button(FRAME,text = eval(data.decode())['file']).pack()
            MESSAGES.update()
            MESSAGES.config(scrollregion=MESSAGES.bbox('all'))
        except:
            l = tk.Label(FRAME,text = data.decode(),relief='flat',fg = 'grey',bg='white')
            l.pack()
            MESSAGES.update()
            MESSAGES.config(scrollregion=MESSAGES.bbox('all'))

t1 = th.Thread(target=print_recv)

username = ''

def send_but():
    data = ENTRY.get()
    ENTRY.delete(0,tk.END)
    A.sendall(data.encode())

def FTP():
    global A
    
    BUFFER = 4096
    file = filedialog.askopenfile(title='OPEN',mode='rb',initialdir='/home/siddharth/simplecpp/',filetypes=(
        ('pdf files', '*.pdf'),
        ('image files', '*.png'),
        ('All files', '*.*')
    ))
    name_of_file = file.name.split(sepr)[-1]
    size_of_file = os.path.getsize(file.name)
    PROGRESS.grid(row=3,sticky=tk.EW)
    PROGRESS['value'] = 0
    dictn = {'file':name_of_file,'size':size_of_file}
    print(dictn)
    A.sendall(str(dictn).encode())
    
    
    print(BUFFER)
    #-------------------------------------------------------------
    for i in range(int(size_of_file)//BUFFER):
        bytes_read = file.read(BUFFER)
        A.sendall(bytes_read)
        PROGRESS['value'] += len(bytes_read)/size_of_file*100
        time.sleep(0.1)
    bytes_read = file.read(size_of_file%BUFFER)
    A.sendall(bytes_read)
    PROGRESS['value'] += len(bytes_read)/size_of_file*100  
    #------------------------------------------------------------- 
    print(1.2)  
    PROGRESS.grid_forget() 
    file.close()
    time.sleep(1)
    A.close()
    time.sleep(1)
    A.close()
    time.sleep(2)
    A = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    A.connect((HOST,PORT))
    wel = A.recv(1024).decode()#welcome
    print(username)
    A.sendall(username.encode())
    A.sendall('file sent'.encode() )




def discon():
    global OPEN
    OPEN = 0
    A.close()
    root.destroy()
    



SEND.config(command = send_but)
DISCONNECT.config(command = discon)
ATTACH.config(command = FTP)

LOCK.acquire()
t1.daemon = 1
t1.start()

root.withdraw()
#__________________________________

def but_command():
    global username
    username += (entry_.get())
    A.sendall(entry_.get().encode())
    name_win.destroy()
    root.deiconify()
name_win = tk.Toplevel(root)
name_ = tk.Label(name_win,text = 'enter name')
entry_ = tk.Entry(name_win)
but_ = tk.Button(name_win, text = 'send',command = but_command)

name_.pack(side='left')
entry_.pack(side = 'right')
but_.pack()
name_win.wm_attributes('-topmost',1)
#__________________________________

root.mainloop()
print(OPEN, t1.is_alive())
OPEN = False
try:
    A.close()
except:
    with Exception as e:
        print(e)

sys.exit()