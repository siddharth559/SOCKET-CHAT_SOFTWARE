from email.headerregistry import Address
import socket as sk
import _thread
import threading as th
import os

A = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
PORT = 52345

HOST = ""#"103.197.36.6"#for connecting in local "192.168.1.110"  "" for all connection
A.bind((HOST,PORT))
A.listen(10)


io_threads = []
connections = []

LOCK = th.Lock()


def IO(CONNECTION,index):
    BUFFER = 4096
    print("thread started with",connections[-1][-1])
    CONNECTION.sendall("WELCOME".encode())
    name = CONNECTION.recv(1024).decode()
    while 1:
        data = CONNECTION.recv(1024)
        try:
            #print(data.decode())
            given_file = eval(data.decode())
            print(2.1)
            file = open(given_file['file'],'wb')
            print(2.2)
            while 1:
                
                received_bytes = CONNECTION.recv(4096)

                if not received_bytes:
                    break
                
                file.write(received_bytes)
            print(2.3)

            print(2.4)

            file.close()
            print(1.5)
            print(os.path.getsize(file.name) == given_file['size'])
            print(1.6)

            CONNECTION.sendall('recieved'.encode())
            
            for i in connections:
                i[0].sendall(data)

        except Exception as emp:
            print(emp)
            try: print(name,":",data.decode())
            except: print("some error")

            if not data:
                #CONNECTION.sendall(''.encode())
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

