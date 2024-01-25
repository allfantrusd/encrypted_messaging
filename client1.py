import Casercipher
import socket
import time
import hashlib
import optparse

reader = optparse.OptionParser()
reader.add_option("-i", "--host", dest='host')
(values, keys) = reader.parse_args()
host_ip = values.host


def find_spec_points(long_msg: str):
    a1 = long_msg.find("™")
    a2 = long_msg.find("©")
    a3 = long_msg.find("®")
    a4 = long_msg.find("é")
    msg = long_msg[a1 + 1:a2 - 7]
    key1 = long_msg[a2 + 1:a3]
    key2 = long_msg[a4 + 1:]
    return (msg, key1, key2)


def decrypt_key(key: str, key2: str):
    c = 0
    c2 = 0
    while True:
        x = hashlib.sha256(str(c).encode('utf-8')).hexdigest()
        if x == key:
            break
        else:
            c += 1
    while True:
        x = hashlib.sha256(str(c2).encode('utf-8')).hexdigest()
        if x == key2:
            break
        else:
            c2 += 1

    return (c, c2)


def client(host: str, port: int):
    client_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (host, port)
    client_soc.connect(server_addr)
    print(f"[*] Successfully connected to the server ...")

    try:
        while True:
            time.sleep(2)

            user_input = input()

            if user_input.lower() == "g":
                print("\033[91m{}\033[0m".format("Receiving ...."))
                # Receive the response from the server
                recv_data = client_soc.recv(1024)
                messages = f"[*] Received data: {recv_data.decode('utf-8')}"
                print(f"[*] Received data: {recv_data.decode('utf-8')}")
                user_input2 = input()

                if user_input2 == "k".lower():
                    (msg, key1, key2) = find_spec_points(messages)
                    (keyone, keytwo) = decrypt_key(key1, key2)
                    orignal_message = msg[:keyone + 1] + msg[keytwo:]
                    decrypted = Casercipher.caesarCipher(orignal_message, mode="decrypt")
                    print(f"decrypted message: {decrypted}")

                else:
                    print(f"Warning! Wrong prompt")




            elif user_input.lower() == "d":
                data = input("\033[91m{}\033[0m".format("Enter the data to send (or type 'exit' to quit): ")) or "N/A"
                if data.lower() == "exit":
                    break
                # Send data to the server
                client_soc.sendall(data.encode('utf-8'))

            elif user_input.lower() == "exit":
                break

    finally:
        client_soc.close()


if __name__ == "__main__":
    host = host_ip
    port = 8080
    client(host, port)
