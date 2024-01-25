import socket
import threading
import Casercipher
import string
import hashlib
import optparse

reader = optparse.OptionParser()
reader.add_option("-i", "--host", dest='host')
(values, keys) = reader.parse_args()
host = values.host

def key2(data: str, key1: int):
    c = key1 + len(string.hexdigits) + len(string.punctuation)
    for key in range(len(data)):
        if key == key1 + len(string.hexdigits) + len(string.punctuation):
            c += 1
    return str(c)

def handle_client(client_socket, address, clients):
    try:
        while True:
            data_recv = client_socket.recv(1024)
            data_decode = data_recv.decode('utf-8')
            data_enc = Casercipher.caesarCipher(data_decode)
            mid = (len(data_enc) // 2) - 1
            data = data_enc[:mid + 1] + string.hexdigits + string.punctuation + data_enc[mid + 1:]
            if not data:
                break

            message = f"{address[0]}:{address[1]} says:™{data}"
            print(message)
            key_2 = key2(data, mid)
            key__2 = hashlib.sha256(key_2.encode('utf-8')).hexdigest()
            mid_enc = hashlib.sha256(str(mid).encode('utf-8')).hexdigest()
            send_msg = f"key[1]:©{mid_enc}® and key[2]:é{key__2}"
            print(f"key[1]:{mid_enc} and key[2]:{key__2}")

            # Broadcast the message to all clients except the sender
            for c in clients:
                if c != client_socket:  # except the sender condition
                    try:
                        c.sendall(message.encode('utf-8'))
                        c.sendall(send_msg.encode('utf-8'))
                    except:
                        # Remove broken connections
                        clients.remove(c)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the client from the list
        clients.remove(client_socket)
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, 8080)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print(f"Server listening on {server_address}")

    clients = []

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            clients.append(client_socket)

            # Create a thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    main()
