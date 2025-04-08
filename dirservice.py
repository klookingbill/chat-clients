import socket
import json
import threading

# dictionary to store user mappings
user_directory = {}

# registration & look up of incoming clients
def handle_client(conn, addr):
    try:
        # get data from client
        data = conn.recv(1024).decode()
        if not data:
            return

        request = json.loads(data)

        # registration request
        if "UID" in request and "user IP" in request and "user PORT" in request:
            user_directory[request["UID"]] = {
                "IP": request["user IP"],
                "PORT": request["user PORT"]
            }

            # response to request
            response = {"error code": 400}  # success
            print(f"Registered {request['UID']} at {request['user IP']}:{request['user PORT']}")

        # look up - see if target_user exists in directory 
        elif "target user" in request:
            target_user = request["target user"]
            if target_user in user_directory:
                response = {
                    "error code": 400,  # success
                    "destination IP": user_directory[target_user]["IP"],
                    "destination port": user_directory[target_user]["PORT"]
                }
                
            else:
                response = {"error code": 600}  # fail - user not in directory
                
                

        else:
            response = {"error code": 600}  # fail - invalid request

        # response back to client of the failure/success
        conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

# starts TCP directory server
def start_dir_server(host, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(5)

    while True:
        # allow incoming connections
        conn, addr = server_sock.accept()
        # new thread for each client - can all run at same time due to threading
        threading.Thread(target=handle_client, daemon=True, args=(conn, addr)).start()

if __name__ == "__main__":
    start_dir_server("", 5000)
