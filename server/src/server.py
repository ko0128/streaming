#importing libraries
import socket
import cv2
import pickle
import struct
import time
import threading
import sys
#import imutils
def accept_client(client_socket,addr):
    while True:
        if client_socket:
            #vid = cv2.VideoCapture('/dev/video0')
            vid = cv2.VideoCapture('rick.mp4')
            fps = vid.get(cv2.CAP_PROP_FPS)
            print('video captured')
            success, frame = vid.read()
            while success:
                frame = cv2.resize(frame, (640,360))
                #print(frame.shape)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                try:
                    client_socket.sendall(message)
                except:
                    print("Sending Fail")
                    break
                #cv2.imshow('Sending...',frame)
                #print("Sending... ")
                time.sleep(1/fps)
                success, frame = vid.read()
        print(f"Client: {addr} closed")
        client_socket.close()
        break


if __name__=='__main__':
    # Server socket
    # create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '0.0.0.0'
    print('HOST IP:',host_ip)
    port = 7000
    socket_address = (host_ip,port)
    print('Socket created')
    # bind the socket to the host. 
    #The values passed to bind() depend on the address family of the socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(socket_address)
    print('Socket bind complete')
    
    #listen() enables a server to accept() connections
    #listen() has a backlog parameter. 
    #It specifies the number of unaccepted connections that the system will allow before refusing new connections.
    server_socket.listen(5)
    print('Socket now listening')
    try: 
        while True:
            client_socket,addr = server_socket.accept()
            print('Connection from:',addr)
            thread = threading.Thread(target=accept_client, args=(client_socket,addr))
            thread.daemon=True
            thread.start()
            print("TOTAL CLIENTS ",threading.activeCount() - 1)
    except KeyboardInterrupt:
        print("\nSever stop!")
        sys.exit()
