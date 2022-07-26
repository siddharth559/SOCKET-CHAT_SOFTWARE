from email.headerregistry import Address
import socket as sk
import _thread
import threading as th

A = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
PORT = 52345

HOST = "192.168.0.103"#"103.197.36.6"#for connecting in local "192.168.1.110"  "" for all connection
A.bind((HOST,PORT))
A.listen(5)


io_threads = []
connections = []

LOCK = th.Lock()


def IO(CONNECTION,index):
    print("thread started with",connections[-1][-1])
    CONNECTION.sendall("WELCOME".encode())
    name = CONNECTION.recv(1024).decode()
    while 1:
        data = CONNECTION.recv(1024)

        try: print(name,":",data.decode())
        except: print("some error")

        if not data:
            CONNECTION.sendall(''.encode())
            #LOCK.release()
            break
        for i in connections:
            i[0].sendall((name+': ').encode()+data)
    io_threads.pop(index)
    connections.pop(index)

count = 0
while count <=5:
    CONNECTION,ADDRESS = A.accept()
    print("connected by {}".format(ADDRESS))
    connections.append([CONNECTION,ADDRESS])
    io_threads.append(th.Thread(target=IO,args=(CONNECTION,len(io_threads))))
    #LOCK.acquire()
    io_threads[-1].start()

    count+=1
    print("count is",count)


print("max connections reached\nserver closing\n",connections)

A.close()

print('server closed')

