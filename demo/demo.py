import argparse
import socket
import time
def getAudioData(client):
    data = client.recv(1365 * 2)
    length = len(data)
    return (length//2, 1, data)
def passAudioData(client):
    (samplesPerChannel, channels, data) = getAudioData(client)
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--socketport", type=int, default=12345,
                        help="socket port")
    args = parser.parse_args()
    HOST = args.ip
    PORT = args.socketport
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(b'1')
    time.sleep(1)
    client_socket.sendall(b'2')
    count=1
    while True:
        passAudioData(client_socket)
        if count > 10000:
            break
    time.sleep(1)
    client_socket.sendall(b'3')
