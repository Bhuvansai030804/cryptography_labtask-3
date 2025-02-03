# client.py
from cryptography.fernet import Fernet
import socket

class SecureClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.key = input("Enter the encryption key: ").encode()
        self.cipher_suite = Fernet(self.key)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            
            while True:
                message = input("Enter message (or 'quit' to exit): ")
                if message.lower() == 'quit':
                    break
                
                encrypted_message = self.cipher_suite.encrypt(message.encode())
                self.client_socket.send(encrypted_message)
                
                encrypted_response = self.client_socket.recv(2048)
                decrypted_response = self.cipher_suite.decrypt(encrypted_response).decode()
                print(f"Server response: {decrypted_response}")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = SecureClient()
    client.start()