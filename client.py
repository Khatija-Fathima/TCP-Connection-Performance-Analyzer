import socket
import time

SERVER_IP = "10.0.0.1"
PORT = 5000

MESSAGE_SIZES = [128, 512, 1024]

for mode in ["persistent", "new_connection"]:

    print(f"\n===== MODE: {mode} =====")

    for size in MESSAGE_SIZES:

        print(f"\nTesting {size} bytes")

        total_time = 0
        total_bytes = 0

        if mode == "persistent":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, PORT))

        for msg_num in range(1, 11):

            if mode == "new_connection":
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((SERVER_IP, PORT))

            data = "A" * size

            message = f"{msg_num}|{size}|{data}"

            start = time.time()

            client.send(message.encode())

            ack = client.recv(2048)

            end = time.time()

            response_time = end - start

            total_time += response_time
            total_bytes += len(message)

            print(
                f"Msg {msg_num} "
                f"Response Time = {response_time:.6f} sec"
            )

            if mode == "new_connection":
                client.close()

        if mode == "persistent":
            client.close()

        average_response_time = total_time / 10

        throughput = total_bytes / total_time

        print(
            f"\nAverage Response Time: "
            f"{average_response_time:.6f}"
        )

        print(
            f"Throughput: "
            f"{throughput:.2f} bytes/sec"
        )

