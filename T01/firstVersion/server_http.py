#!/usr/bin/env python3

from socket import *
from threading import Thread
import sys
import os

# Tratamento da thread
def newThread(connection, address):
    while True:
        # Armazena dados da conexão recebidos (em um buffer com 2048 de tamanho)
        request = connection.recv(2048)

        # Definições do server
        html = "index.html"
        notFound = "ERROR.html"
        image_1 = "cat.jpg"
        image_2 = "2_cat.jpg"
        image_3 = "3_cat.jpg"

        # Se existir a palavra GET, é uma requisição
        if("GET" in request):
            print("Inicio do request: ", request)
            request = request.split("/")

            print("request[1]: ", request[1])

            header = "HTTP/1.1 200 OK\r\n"

            if(request[1] == " HTTP"):
                file = open(html, 'rb')
                response = file.read()
                file.close()
            # elif structure here

            # Completa a resposta HTTP
            full_response = header.encode('utf-8')
            full_response += response

            # Envia a resposta HTTP
            connection.send(full_response)
            print("\n\n -- \n\n")
            print("HTTP Response: " + full_response)

            # Finaliza a conexão
            print("Finalizing connection with the client: " + address)
            connection.close()

            Thread.exit()
