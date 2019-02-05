# server.py 
import socket                                         
import time
import os

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '0.0.0.0'                        

port = 9999                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))
    while True:
	try:
		cs,a = serversocket.accept()
		if (str(addr) != str(a)):
			cs.close()
			break
	except:
		continue
    clientsocket.send('Authenticated')
    clientsocket.close()
