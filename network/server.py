from typing import Dict, List, Tuple
from game.game import PokerGame

import socket
import pickle
from select import select

class Server:
    HOST = "127.0.0.1"
    PORT = 42069
    MAX_CONNS = 20
    TIMEOUT = 1

    def __init__(self) -> None:
        self.id_counter = 0

        self.client_to_id: Dict[socket.socket, id] = {}
        self.id_to_game: Dict[int, PokerGame] = {}
        self.games: List[PokerGame] = []

        self.data_to_send: Dict[socket.socket, Dict] = {}

    def setup(self) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(self.MAX_CONNS)
        print(f"[Server] established server on port {self.HOST}:{self.PORT}")
        return s
    
    def new_connection(self, conn: socket.socket, addr: Tuple[str, int]):
        self.id_counter += 1

        print(f"[Server] recieved now connection from addr {addr}, assigning id {self.id_counter} to this client.")
        self.client_to_id[conn] = self.id_counter
    
        name = conn.recv(1024).decode()
        
        for game in self.games:
            if not game.is_full:
                chosen_game = game
                break
        else:
            chosen_game = PokerGame()
            self.games.append(chosen_game)

        chosen_game.add_player(name, self.id_counter)
        self.id_to_game[self.id_counter] = chosen_game
        print(f"[Server] assigned player {self.id_counter} to new game")

    def handle_request(self, conn: socket.socket):
        data = conn.recv(1024)
        id = self.client_to_id[conn]

        if data == b"":
            print("[Server] empty packet: client disconnected")
            self.id_to_game[id].remove_player(id)
            del self.id_to_game[id]
            del self.client_to_id[conn]
            conn.close()
            return

        req = pickle.loads(data)
        result = self.id_to_game[id].process_request(req, id)
        if conn in self.data_to_send:
            print("[Server] this socket already has unsent data")
        self.data_to_send[conn] = result   

    def run(self) -> None:
        server_socket = self.setup()

        try:
            while True:
                readable, writable, _ = select([server_socket] + list(self.client_to_id.keys()), self.client_to_id.keys(), [], self.TIMEOUT)

                # read sockets
                for sock in readable:
                    if sock is server_socket:  # new connection
                        conn, addr = server_socket.accept()
                        self.new_connection(conn, addr)
                    
                    else:  # new request
                        self.handle_request(sock)
                
                # write sockets
                for sock in writable:
                    if sock in self.data_to_send:
                        sock.sendall(pickle.dumps(self.data_to_send[sock]))
                        del self.data_to_send[sock]

        except KeyboardInterrupt:
            print(f"[Server] detected keyboard interrupt, shutting down")

        finally:
            for sock in self.client_to_id.keys():
                sock.close()
            server_socket.close()
            print("[Server] closed all sockets")
            

if __name__ == "__main__":
    Server().run()