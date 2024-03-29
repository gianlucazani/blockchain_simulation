import _pickle
import threading
import socket

HOST = "127.0.0.1"


class BlockchainClient(threading.Thread):
    def __init__(self, server_port_no, port_dict):
        super().__init__()
        self.server_port_no = server_port_no  # peer port number (server role)
        self.port_dict = port_dict  # dictionary of all the neighbours with their port
        self.alive = True

    def run(self):

        # KEEP ASKING FOR USER INPUT UNTIL THE PEER IS ALIVE
        while self.alive:
            # ask for user input
            print("Which action do you want to perform? (type the command)")
            print("tx) Transaction [tx|{sender}|{content}]")
            print("pb) Print Blockchain [pb]")
            print("cc) Close Connection [cc]")
            choice = input()
            match choice:
                case "tx":
                    self.send_transaction()
                case "pb":
                    print_blockchain_thread = threading.Thread(target=self.print_blockchain)
                    print_blockchain_thread.start()
                case "cc":
                    # CLIENT DIES
                    self.alive = False
                    close_connection_thread = threading.Thread(target=self.close_connection)
                    close_connection_thread.start()

    def send_transaction(self):
        """
        Manages the sending of a new trnasaction to all the peers in the network, including to the server ole that resides in the same peer as the client
        """
        print("Write the transaction in the format tx|{sender}|{content}")
        transaction = input()
        if transaction[0:2] == "tx":
            # BROADCAST TO MY SERVER ROLE
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # CONNECT TO SERVER
                try:
                    s.connect((HOST, int(self.server_port_no)))
                except socket.error as e:
                    pass
                    # print(f"Client {self.server_port_no} error CONNECTING with server {self.server_port_no}")
                    # print(f"ERROR {e}")

                # SEND TRANSACTION TO SERVER
                try:
                    s.sendall(bytes(transaction, encoding="utf-8"))
                except socket.error as e:
                    pass
                    # print(f"Client {self.server_port_no} error SENDING TRANSACTION to server {self.server_port_no}")
                    # print(f"ERROR {e}")

                # PRINT RESPONSE FROM SERVER ABOUT VALID TRANSACTION
                try:
                    received = s.recv(4096)
                    print(received.decode("utf-8"))
                except socket.error as e:
                    pass
                    # print(f"Client {self.server_port_no} error RECEIVING TRANSACTION VALIDATION from server {self.server_port_no}")
                    # print(f"ERROR {e}")

            # BROADCAST TO OTHER SERVERS THE TRANSACTION
            for ID, PORT in self.port_dict.items():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.connect((HOST, int(PORT)))
                    except socket.error as e:
                        pass
                        # print(f"error CONNECTING with PEER {ID} at PORT: {PORT}")
                        # print(f"ERROR {e}")
                    try:
                        s.sendall(bytes(transaction, encoding="utf-8"))
                    except socket.error as e:
                        pass
                        # print(f"error SENDING TRANSACTION with PEER {ID} at PORT: {PORT}")
                        # print(f"ERROR {e}")
        else: 
            print("Rejected")

    def print_blockchain(self):
        """
        Asks the server the blockchain as json and prints it at terminal
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # CONNECT TO SERVER
            try:
                s.connect((HOST, int(self.server_port_no)))
            except socket.error as e:
                pass
                # print(f"Client {self.server_port_no} error CONNECTING with server {self.server_port_no}")
                # print(f"ERROR {e}")

            # SEND PB REQUEST TO SERVER
            try:
                message = "pb"
                s.sendall(bytes(message, encoding="utf-8"))
            except socket.error as e:
                pass
                # print(f"Client {self.server_port_no} error SENDING PB REQUEST to server {self.server_port_no}")
                # print(f"ERROR {e}")

            # RECEIVE BLOCKCHAIN AS JSON FROM SERVER
            try:
                received = s.recv(4096)
                blockchain = _pickle.loads(received)
                print(f"{blockchain.blockchain_string()}")
            except socket.error as e:
                pass
                # print(f"Client {self.server_port_no} error RECEIVING BLOCKCHAIN from server {self.server_port_no}")
                # print(f"ERROR {e}")

    def close_connection(self):
        """
        Sends "cc" to the server and kill itself
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # CONNECT TO SERVER
            try:
                s.connect((HOST, int(self.server_port_no)))
            except socket.error as e:
                pass
                # print(f"Client {self.server_port_no} error CONNECTING with server {self.server_port_no}")
                # print(f"ERROR {e}")

            # SEND PB REQUEST TO SERVER
            try:
                message = "cc"
                s.sendall(bytes(message, encoding="utf-8"))
            except socket.error as e:
                pass
                # print(f"Client {self.server_port_no} error SENDING CC REQUEST to server {self.server_port_no}")
                # print(f"ERROR {e}")
