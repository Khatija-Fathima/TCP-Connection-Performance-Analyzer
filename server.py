import socket
import datetime

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"TCP Server listening on {HOST}:{PORT}")

log_file = open("server_log.txt", "a")

while True:
    conn, addr = server.accept()

    while True:
        data = conn.recv(2048)

        if not data:
            break

        message = data.decode()

        parts = message.split("|", 2)

        if len(parts) < 3:
            continue

        msg_id = parts[0]
        msg_size = parts[1]

        ack = f"ACK|{msg_id}|{msg_size}"

        conn.send(ack.encode())

        timestamp = datetime.datetime.now()

        log_line = (
            f"{timestamp},"
            f"{addr[0]},"
            f"unknown,"
            f"{msg_id},"
            f"{msg_size},"
            f"YES\n"
        )

        log_file.write(log_line)
        log_file.flush()

        print(f"Received MSG {msg_id} Size {msg_size}")

    conn.close()



