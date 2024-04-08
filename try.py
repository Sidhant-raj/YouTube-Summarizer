#
# # In[6]:
#
#
# # num_iters = int(len(transcript_text)/1000)
# # summarized_text = []
# # for i in range(0, num_iters + 1):
# #   start = 0
# #   start = i * 1000
# #   end = (i + 1) * 1000
# # #   print("input text \n" + transcript_text[start:end])
# #   out = summarizer(transcript_text[start:end], length_penalty=2.0, max_length=90, min_length=10)
# #   out = out[0]
# #   out = out['summary_text']
# # #   print("Summarized text\n"+out)
# #   summarized_text.append(out)
#
# # print(summarized_text)
#
#
# # In[4]:
#
# # import time
# #
# # for i in summarized_text:
# #     for j in range(len(i)):
# #         print(i[j], end='', flush=True)
# #         time.sleep(0.000001)
#
#
#
# import socket
# import threading
# from bs4 import BeautifulSoup
# import re
# import Server_YouTube_Transcript_Summary
#
#
# def parse_headers(request):
#     headers = request.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
#     header_dict = {}
#     for header in headers:
#         key, value = header.split(': ', 1)
#         header_dict[key] = value
#     return header_dict
#
#
# def handle_request(client_socket, request, Summary_text=None):
#     if "GET" in request:
#         with open("index.html", "r") as file:
#             html_content = file.read()
#
#         response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{html_content}"
#     elif "POST" in request:
#         # headers = parse_headers(request)
#         #
#         # if 'Content-Length' in headers:
#         #     content_length = int(headers['Content-Length'])
#         #     message_body = client_socket.recv(content_length).decode('utf-8')
#
#         response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage received: ".join(Summary_text)
#         # else:
#         #     response = "HTTP/1.1 411 Length Required\r\n\r\n"
#     else:
#         response = "HTTP/1.1 400 Bad Request\r\n\r\n"
#
#     return response.encode()
#
#
# def handle_client(client_socket, client_address):
#     print(f"Connection from {client_address}")
#
#     request_data = client_socket.recv(2000).decode('utf-8')
#     # print(f"Received request:\n{request_data}")
#
#     match = re.search(r'"message"\s*:\s*"(.*?)"', request_data)
#
#     if match:
#         extracted_message = match.group(1)
#         print(extracted_message)
#         Summary_text = Server_YouTube_Transcript_Summary.SummaryOfVideo(str(extracted_message))
#         print(Summary_text[0])
#         response_data = handle_request(client_socket, request_data, Summary_text[0])
#         client_socket.sendall(response_data)
#     else:
#         response_data = handle_request(client_socket, request_data)
#         client_socket.sendall(response_data)
#
#     # print(response_data)
#
#     # Don't close the client socket here
#     print(f"Connection with {client_address} closed")
#
#
# def run_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('localhost', 8080)
#     server_socket.bind(server_address)
#
#     print(f"Web server listening on http://{server_address[0]}:{server_address[1]}")
#
#     server_socket.listen(5)
#
#     while True:
#         print("Waiting for a connection...")
#         client_socket, client_address = server_socket.accept()
#         # Create a new thread to handle the client
#         client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
#         client_handler.start()
#
#
# if __name__ == "__main__":
#     run_server()
#
#
#
# <!--<!DOCTYPE html>-->
# <!--<html lang="en">-->
# <!--<head>-->
# <!--    <meta charset="UTF-8">-->
# <!--    <meta name="viewport" content="width=device-width, initial-scale=1.0">-->
# <!--    <style>-->
# <!--        body {-->
# <!--            font-family: Arial, sans-serif;-->
# <!--            margin: 0;-->
# <!--            padding: 0;-->
# <!--            height: 100vh;-->
# <!--            display: flex;-->
# <!--            align-items: center;-->
# <!--            justify-content: center;-->
# <!--            background-color: #f1cbcb;-->
# <!--        }-->
#
# <!--        .outer-div {-->
# <!--            width: 300px;-->
# <!--            height: 100px;-->
# <!--            padding: 60px;-->
# <!--            border-radius: 40px;-->
# <!--            background-color: rgb(159, 130, 156);-->
# <!--        }-->
#
# <!--        label {-->
# <!--            display: block;-->
# <!--            margin-bottom: 10px;-->
# <!--        }-->
#
# <!--        input {-->
# <!--            width: 100%;-->
# <!--            padding: 8px;-->
# <!--            margin-bottom: 10px;-->
# <!--            border: 1px solid #ccc;-->
# <!--            border-radius: 5px;-->
# <!--            box-sizing: border-box;-->
# <!--        }-->
#
# <!--        button {-->
# <!--            padding: 10px;-->
# <!--            background-color: #2ecc71;-->
# <!--            color: #fff;-->
# <!--            border: none;-->
# <!--            border-radius: 5px;-->
# <!--            cursor: pointer;-->
# <!--        }-->
# <!--    </style>-->
# <!--    <title>Webpage with JavaScript</title>-->
# <!--</head>-->
# <!--<body>-->
# <!--    <div class="outer-div">-->
# <!--        <form id="messageForm">-->
# <!--            <label for="messageInput">Enter Message:</label>-->
# <!--            <input type="text" id="messageInput" name="messageInput" required>-->
# <!--            <button type="submit">Send Message</button>-->
# <!--        </form>-->
# <!--        &lt;!&ndash; Display area for server responses &ndash;&gt;-->
# <!--        <div id="responseOutput"></div>-->
# <!--    </div>-->
#
# <!--    <script>-->
# <!--        document.getElementById('messageForm').addEventListener('submit', function (event) {-->
# <!--            event.preventDefault(); // Prevent the default form submission-->
#
# <!--            // Get the server address and message-->
# <!--            const serverAddress = 'http://10.7.221.128:8080';  // Replace with your server address-->
# <!--            const message = document.getElementById('messageInput').value; // Get input value-->
#
# <!--            // Make an HTTP POST request to the server-->
# <!--            fetch(serverAddress, {-->
# <!--                method: 'POST',-->
# <!--                headers: {-->
# <!--                    'Content-Type': 'application/json',-->
# <!--                },-->
# <!--                body: JSON.stringify({ message: message }),-->
# <!--            })-->
# <!--            .then(response => response.json())  // Assuming server responds with JSON-->
# <!--            .then(data => {-->
# <!--                console.log('Server response:', data);-->
#
# <!--                // Display the server response on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Server response: ' + data.summary_text;-->
# <!--            })-->
# <!--            .catch(error => {-->
# <!--                console.error('Error:', error);-->
#
# <!--                // Display the error on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Error: ' + error.message;-->
# <!--            });-->
# <!--        });-->
# <!--    </script>-->
# <!--</body>-->
# <!--</html>-->
#
#
#
# <!--<!DOCTYPE html>-->
# <!--<html lang="en">-->
# <!--<head>-->
# <!--    <meta charset="UTF-8">-->
# <!--    <meta name="viewport" content="width=device-width, initial-scale=1.0">-->
# <!--    <style>-->
# <!--        body {-->
# <!--            font-family: Arial, sans-serif;-->
# <!--            margin: 0;-->
# <!--            padding: 0;-->
# <!--            height: 100vh;-->
# <!--            display: flex;-->
# <!--            align-items: center;-->
# <!--            justify-content: center;-->
# <!--            background-color: #f1cbcb;-->
# <!--        }-->
#
# <!--        .outer-div {-->
# <!--            width: 1200px;-->
# <!--            height: 500px; /* Increased height to accommodate response */-->
# <!--            padding: 20px;-->
# <!--            border-radius: 20px;-->
# <!--            background-color: rgb(159, 130, 156);-->
# <!--            overflow: hidden; /* Hide content that overflows */-->
# <!--        }-->
#
# <!--        label {-->
# <!--            display: block;-->
# <!--            margin-bottom: 10px;-->
# <!--        }-->
#
# <!--        input {-->
# <!--            width: 100%;-->
# <!--            padding: 8px;-->
# <!--            margin-bottom: 10px;-->
# <!--            border: 1px solid #ccc;-->
# <!--            border-radius: 5px;-->
# <!--            box-sizing: border-box;-->
# <!--        }-->
#
# <!--        button {-->
# <!--            padding: 10px;-->
# <!--            background-color: #2ecc71;-->
# <!--            color: #fff;-->
# <!--            border: none;-->
# <!--            border-radius: 5px;-->
# <!--            cursor: pointer;-->
# <!--        }-->
#
# <!--        #responseOutput {-->
# <!--            margin-top: 10px;-->
# <!--            color: whitesmoke;-->
# <!--            text-align: justify;-->
# <!--        }-->
# <!--    </style>-->
# <!--    <title>Webpage with JavaScript</title>-->
# <!--</head>-->
# <!--<body>-->
# <!--    <div class="outer-div">-->
# <!--        <form id="messageForm">-->
# <!--            <label for="messageInput">Enter Message:</label>-->
# <!--            <input type="text" id="messageInput" name="messageInput" required>-->
# <!--            <button type="submit">Send Message</button>-->
# <!--        </form>-->
# <!--        &lt;!&ndash; Display area for server responses &ndash;&gt;-->
# <!--        <div id="responseOutput"></div>-->
# <!--    </div>-->
#
# <!--    <script>-->
# <!--        document.getElementById('messageForm').addEventListener('submit', function (event) {-->
# <!--            event.preventDefault(); // Prevent the default form submission-->
#
# <!--            // Get the server address and message-->
# <!--            const serverAddress = 'http://10.7.221.128:8080';  // Replace with your server address-->
# <!--            const message = document.getElementById('messageInput').value; // Get input value-->
#
# <!--            // Make an HTTP POST request to the server-->
# <!--            fetch(serverAddress, {-->
# <!--                method: 'POST',-->
# <!--                headers: {-->
# <!--                    'Content-Type': 'application/json',-->
# <!--                },-->
# <!--                body: JSON.stringify({ message: message }),-->
# <!--            })-->
# <!--            .then(response => response.json())  // Assuming server responds with JSON-->
# <!--            .then(data => {-->
# <!--                console.log('Server response:', data);-->
#
# <!--                // Display the server response on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Server response: ' + data.summary_text;-->
# <!--            })-->
# <!--            .catch(error => {-->
# <!--                console.error('Error:', error);-->
#
# <!--                // Display the error on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Error: ' + error.message;-->
# <!--            });-->
# <!--        });-->
# <!--    </script>-->
# <!--</body>-->
# <!--</html>-->
#
#
#
# <!--<!DOCTYPE html>-->
# <!--<html lang="en">-->
# <!--<head>-->
# <!--    <meta charset="UTF-8">-->
# <!--    <meta name="viewport" content="width=device-width, initial-scale=1.0">-->
# <!--    <style>-->
# <!--        /* Add CSS for the loading element */-->
# <!--        #loading {-->
# <!--            display: none;-->
# <!--            position: fixed;-->
# <!--            top: 50%;-->
# <!--            left: 50%;-->
# <!--            transform: translate(-50%, -50%);-->
# <!--            background-color: rgba(255, 255, 255, 0.8);-->
# <!--            padding: 20px;-->
# <!--            border-radius: 10px;-->
# <!--            text-align: center;-->
# <!--        }-->
#
# <!--        body {-->
# <!--            font-family: Arial, sans-serif;-->
# <!--            margin: 0;-->
# <!--            padding: 0;-->
# <!--            height: 100vh;-->
# <!--            display: flex;-->
# <!--            align-items: center;-->
# <!--            justify-content: center;-->
# <!--            background-color: #f1cbcb;-->
# <!--        }-->
#
# <!--        .outer-div {-->
# <!--            width: 1200px;-->
# <!--            height: 500px;-->
# <!--            padding: 20px;-->
# <!--            border-radius: 20px;-->
# <!--            background-color: rgb(159, 130, 156);-->
# <!--            overflow: hidden;-->
# <!--        }-->
#
# <!--        label {-->
# <!--            display: block;-->
# <!--            margin-bottom: 10px;-->
# <!--        }-->
#
# <!--        input {-->
# <!--            width: 100%;-->
# <!--            padding: 8px;-->
# <!--            margin-bottom: 10px;-->
# <!--            border: 1px solid #ccc;-->
# <!--            border-radius: 5px;-->
# <!--            box-sizing: border-box;-->
# <!--        }-->
#
# <!--        button {-->
# <!--            padding: 10px;-->
# <!--            background-color: #2ecc71;-->
# <!--            color: #fff;-->
# <!--            border: none;-->
# <!--            border-radius: 5px;-->
# <!--            cursor: pointer;-->
# <!--        }-->
#
# <!--        #responseOutput {-->
# <!--            margin-top: 10px;-->
# <!--            color: whitesmoke;-->
# <!--            text-align: justify;-->
# <!--        }-->
# <!--    </style>-->
# <!--    <title>Webpage with JavaScript</title>-->
# <!--</head>-->
# <!--<body>-->
# <!--    &lt;!&ndash; Loading element &ndash;&gt;-->
# <!--    <div id="loading">Loading...</div>-->
#
# <!--    <div class="outer-div">-->
# <!--        <form id="messageForm">-->
# <!--            <label for="messageInput">Enter Message:</label>-->
# <!--            <input type="text" id="messageInput" name="messageInput" required>-->
# <!--            <button type="submit">Send Message</button>-->
# <!--        </form>-->
# <!--        &lt;!&ndash; Display area for server responses &ndash;&gt;-->
# <!--        <div id="responseOutput"></div>-->
# <!--    </div>-->
#
# <!--    <script>-->
# <!--        document.getElementById('messageForm').addEventListener('submit', function (event) {-->
# <!--            event.preventDefault();-->
#
# <!--            // Show loading element-->
# <!--            document.getElementById('loading').style.display = 'block';-->
#
# <!--            const serverAddress = 'http://10.7.221.128:8080';-->
# <!--            const message = document.getElementById('messageInput').value;-->
#
# <!--            fetch(serverAddress, {-->
# <!--                method: 'POST',-->
# <!--                headers: {-->
# <!--                    'Content-Type': 'application/json',-->
# <!--                },-->
# <!--                body: JSON.stringify({ message: message }),-->
# <!--            })-->
# <!--            .then(response => response.json())-->
# <!--            .then(data => {-->
# <!--                console.log('Server response:', data);-->
#
# <!--                // Display the server response on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Server response: ' + data.summary_text;-->
# <!--            })-->
# <!--            .catch(error => {-->
# <!--                console.error('Error:', error);-->
#
# <!--                // Display the error on the webpage-->
# <!--                const responseOutput = document.getElementById('responseOutput');-->
# <!--                responseOutput.innerHTML = 'Error: ' + error.message;-->
# <!--            })-->
# <!--            .finally(() => {-->
# <!--                // Hide loading element after response or error-->
# <!--                document.getElementById('loading').style.display = 'none';-->
# <!--            });-->
# <!--        });-->
# <!--    </script>-->
# <!--</body>-->
# <!--</html>-->
#
#
# def parse_headers(request):
#     headers = request.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
#     header_dict = {}
#     for header in headers:
#         key, value = header.split(': ', 1)
#         header_dict[key] = value
#     return header_dict
#
