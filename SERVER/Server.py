import socket

IP = '10.0.0.5'
PORT = 55555

server_address = (IP,PORT)

s_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s_sock.bind(server_address)

s_sock.listen()

while True:
    c_sock, c_addr = s_sock.accept()
    message = ""
    
    while True:
        data = c_sock.recv(1024)
        if not data:
            break;
        else:
            message = data.decode('UTF-8')
            print("Parancs: ", message)
            
    c_sock.close
