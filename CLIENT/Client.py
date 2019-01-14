import socket


HOST = '10.0.0.5'
PORT = 55555

def locSend(message):
    
    
    c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST,PORT)
    try:
        c_sock.connect(server_address)
        c_sock.sendall(message.encode('UTF-8'))
    
        c_sock.close()
    except:
        print("Szerver nem elérhető!")
    
    
# locSend("TEST")