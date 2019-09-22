#!/usr/bin/env python3

from socket import *
from threading import Thread
import sys
import os
import server_http

# Define o host (já que não temos DNS)
HOST =  '127.0.0.1'
# Define a porta
port = 55555

# Cria o socket
socket = socket(AF_INET, SOCK_STREAM)

# Associa o socket criado com nosso host e porta
socket.bind((HOST, port))

# Coloca o socket para ouvir
socket.listen(1)

print("Web server: \n Host: " + str(HOST) + "\n Port: " + str(port))


# tratamento de erro ?


while True:
    # Aguarda uma conexão
    connection, address = socket.accept()

    # Inicia uma thread quando uma conexão é aceita
    Thread.start_new_thread(server_http.newThread, tuple([connection, address]))

tcp.close()
