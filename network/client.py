from playsound import playsound

import socket
import pickle

HOST = "127.0.0.1"
PORT = 42069

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    name = input("Enter name: ")

    if name.lower() in ["fabian", "fabs"]:
        playsound('network/poker_face.mp3', block=False)

    s.connect((HOST, PORT))
    s.send(name.encode())

    while True:
        msg = input("Enter msg to send: ")
        packet = {
            "type": "test",
            "msg": msg,
        }
        s.sendall(pickle.dumps(packet))
        data = s.recv(1024)
        print(f"Recieved: {pickle.loads(data)}")
