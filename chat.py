import sys
import socket
import json
import threading
import time

#python3 chat.py Alice 127.0.0.1:3000 127.0.0.1:3001
#python3 chat.py Bob 127.0.0.1:3001 127.0.0.1:3000

def chat():
    if len(sys.argv) != 4:
        print("Usage: python chat.py <username> <source_ip:port> <destination_ip:port>")
        sys.exit(1)
    

    username = sys.argv[1]
    # address to send messages to, parse address
    src_ip, src_port = sys.argv[2].split(":")

    # address that listening for messages from, parse address
    dst_ip, dst_port = sys.argv[3].split(":")
    src_port = int(src_port)
    dst_port = int(dst_port)

    buffer = 1024

    # socket for sending messages
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # socket for receiving messages
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # binds socket to source address - where sending messages
    server_sock.bind((src_ip, src_port))

    print(f"{username}, you are ready to chat with UDP listening on {sys.argv[3]}")



    def send():
        seq_num = 0
        while True:
            content = input(f"{username}: ")

            # actual message to send, converts message to json key-value pairs
            message = json.dumps({
                "Version": "v1",
                "Seq. num": seq_num,
                "UID": username,
                "DID": sys.argv[3],
                "Content": content
            })

            seq_num += 1
            # send message from client to server
            client_sock.sendto(message.encode(), (dst_ip, dst_port))
    
    def receive():
        expected_seq = 0
        while True:
            receive_messages, sender_address = server_sock.recvfrom(buffer)
            message = json.loads(receive_messages.decode())

            # make sure seq num is correct 
            if message['Seq. num'] == expected_seq:
                print(f"\n{message['UID']} >> {message['Content']}")
                expected_seq += 1
            else:
                print(f"\nMessage received with unexpected sequence number. Expected {expected_seq} but received {message['Seq. num']}")
                
            # reset
            print(f"{username}: ", end="", flush=True)

    # threads allow send and receive to run simultaneously
    threadSend = threading.Thread(target=send, daemon=True).start()
    threadReceive = threading.Thread(target=receive, daemon=True).start()

    # keeps main running
    while True:
        time.sleep(1)


if __name__ == "__main__":
    chat()