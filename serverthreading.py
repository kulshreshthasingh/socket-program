import socket
import threading
import random

def handle_client(conn, addr, server_name, server_number):
    print(f"\n[+] Connected by {addr}")

    try:
        data = conn.recv(1024).decode()
        if not data:
            return

        client_name, client_num_str = data.split(",")
        client_num = int(client_num_str.strip())

        # Check valid range
        if client_num < 1 or client_num > 100:
            print(f"[-] {addr} sent invalid number {client_num}. Terminating server.")
            conn.close()
            exit(0)  # Kill the whole server as per requirement

        total = client_num + server_number

        # Display on server side
        print("\n--- Server Side ---")
        print(f"Client Name: {client_name}")
        print(f"Server Name: {server_name}")
        print(f"Client Integer: {client_num}")
        print(f"Server Integer: {server_number}")
        print(f"Sum: {total}")

        # Send reply back to client
        reply = f"{server_name},{server_number}"
        conn.send(reply.encode())

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection closed: {addr}")

def main():
    host = "0.0.0.0"
    port = 6000

    server_name = "Server of John Q. Smith"
    server_number = random.randint(1, 100)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow backlog of connections

    print(f"[STARTED] Concurrent Server listening on port {port}...")

    while True:
        conn, addr = server_socket.accept()
        # Start a new thread for each client
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, server_name, server_number)
        )
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
