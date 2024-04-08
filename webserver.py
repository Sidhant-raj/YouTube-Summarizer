import socket
import threading
import re
import Server_YouTube_Transcript_Summary
import json


def handle_request(client_socket, request, Summary_text=None):
    if "GET" in request:
        with open("index.html", "r") as file:
            html_content = file.read()

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
    elif "POST" in request:
        response_data = json.dumps({'summary_text': Summary_text})

        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{response_data}"
    else:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"

    return response.encode()


def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    request_data = client_socket.recv(2000).decode('utf-8')
    print(f"Received request:\n{request_data}")

    match = re.search(r'"message"\s*:\s*"(.*?)"', request_data)

    if match:
        extracted_message = match.group(1)
        print(extracted_message)
        Summary_text = Server_YouTube_Transcript_Summary.SummaryOfVideo(str(extracted_message))
        print("".join(Summary_text[0]))
        Summary_text = "".join(Summary_text[0])
        response_data = handle_request(client_socket, request_data, Summary_text)
        # print(response_data)
        client_socket.sendall(response_data)
    else:
        response_data = handle_request(client_socket, request_data)
        client_socket.sendall(response_data)

    print(f"Connection with {client_address} closed")
    client_socket.close()

exit_flag = False


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 8080)
    server_socket.bind(server_address)

    print(f"Web server listening on http://{server_address[0]}:{server_address[1]}")
    server_socket.listen(5)

    while not exit_flag:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()

        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()


if __name__ == "__main__":
    run_server()
