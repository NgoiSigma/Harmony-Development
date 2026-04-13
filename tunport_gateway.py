# tunport_gateway.py

import ssl
import socket
import threading
from avatarus_core import process_resonance

HOST = '0.0.0.0'
PORT = 5555
CERTFILE = 'certs/server.crt'
KEYFILE = 'certs/server.key'

def handle_client(conn, addr):
    print(f"[+] Подключение: {addr}")
    try:
        while data := conn.recv(4096):
            message = data.decode('utf-8')
            response = process_resonance(message)
            conn.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[-] Ошибка клиента {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Отключение: {addr}")

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"[~] TunPort Gateway активен на {HOST}:{PORT}")

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                conn, addr = ssock.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
