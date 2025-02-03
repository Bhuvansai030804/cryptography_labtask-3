# server.py
from cryptography.fernet import Fernet
import socket
import threading

class SecureServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []

    def start(self):
        self.server_socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        print(f"Encryption key: {self.key.decode()}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connected with {address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            while True:
                encrypted_message = client_socket.recv(2048)
                if not encrypted_message:
                    break
                
                decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
                print(f"Received: {decrypted_message}")
                
                response = f"Server received: {decrypted_message}"
                encrypted_response = self.cipher_suite.encrypt(response.encode())
                client_socket.send(encrypted_response)
                
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)

    def stop(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = SecureServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop()