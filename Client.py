import socket
import time


def PrintSummary(summary):
    for i in summary:
        for j in range(len(i)):
            print(i[j], end='', flush=True)
            time.sleep(0.000001)


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 1240)

    message = input("Input Link: ")#"https://www.youtube.com/watch?v=5g1LtbCtVhs&ab_channel=AlphaLife"
    client_socket.sendto(message.encode(), server_address)
    print("Waiting for Server...")
    text, server = client_socket.recvfrom(10000)
    # print(f"Summary: {data.decode()}")
    length_of_summary, server1 = client_socket.recvfrom(16)
    length_of_transcript, server2 = client_socket.recvfrom(16)

    print(f"\nLength of Summary: {length_of_summary.decode()}, and Transcript text: {length_of_transcript.decode()}\n")
    PrintSummary(text.decode())


    client_socket.close()
