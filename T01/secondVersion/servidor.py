#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# Matheus Fonseca Alexandre de Oliveira
# 1794027

# Bibliotecas
from socket import *
import threading as th

# Definição das classes:

class HTTPRequest:
    # Carriage Return e Line Feed Character
    CLRF = '\r\n'

    # Cria um socket interno a classe, de mesmas especificações
    c_Socket = socket(AF_INET, SOCK_STREAM)

    # Define o construtor da classe
    def __init__(self, e_socket):
        # Associa socket externo (e_socket) com socket interno
        self.c_Socket = e_socket

        # Cria uma thread para tratar essa conexão, que tem o método "execute"
        th.Thread(target = self.execute, args=()).start()

    # Executa a requisição
    def execute(self):
        # Chama a função de processamento
        try:
            print("Entering processing part")
            self.process()
        except Exception as error:
            print("DEU ERRO NO PROCESS!")
            print(error)
        
    # Processa a requisição    
    def process(self):
        # Cria um buffer de 1024 para colocar a requisição recebida
        request = self.c_Socket.recv(1024)
        print("\nRequest: \n")
        print(request)

        # Quebra a string nos pedaços que nos importa
        print("tentando quebrar string")
        # Request line: tudo antes do primeiro \r
        request_line = request[:request.find(self.CLRF)]
        print("Request line: ")
        print(request_line)
        # Header line: tudo depois do \r\n (ai precisa deslocar um pouquinho)
        request_header = request[request.find(self.CLRF)+2:]
        print("Request Header: ")
        print(request_header)
        # File: tudo depois do GET / e antes de HTTP/1.1
        file_name = request_line[5:request_line.find(" HTTP/1.1")]
        print("File name: ")
        print(file_name)
        print("string parser complete")
        # Verifica se o arquivo requisitado existe
        
        file_exist = False
        try:
            # Se o try funcionar, é porque dá pra "abrir" o arquivo. Assim sendo
            # seta a flag para true. Caso contrário, mantem falso, e printa o erro no terminal
            print("Opening file...")
            with open(file_name, 'r') as d_file:
                data = d_file.read()
            file_exist = True
        except Exception as error:
            print("DEU ERRO NO FILE OPEN")
            print(error)
        # Constroi mensagem resposta
        if(file_exist):
            # Se o arquivo existir:
            status_line = "HTTP/1.1 200 OK" + self.CLRF
            # Dois CLRF para indicar o fim do header
            contentType_line = "Content-type: " + self.file_type(file_name) + self.CLRF + self.CLRF
            # data já tá com o valor

        else:
            # Se o arquivo não existir
            status_line = "HTTP/1.1 404 Not Found" + self.CLRF
            
            # São necessários dois CLRF para indificar fim de header
            contentType_line = "Content-type: text/html" + self.CLRF + self.CLRF
            
            # Lê o html com a resposta de erro
            d_file = open("404notfound.html", 'rb')
            data = d_file.read()
            d_file.close()
            
        # Reune todas as informações em um única string
        response = status_line + contentType_line + data
        print("Response: ")
        print(response)
        # Envia por socket a resposta
        self.c_Socket.send(response)

        # Fecha o socket
        self.c_Socket.close()

    # Determina qual arquivo / tipo de arquivo que o Request pediu
    def file_type(self, file):
        f_data = file.split(".")
        f_name = f_data[0]
        f_type = f_data[1]

        if(f_type == "jpg"):
            # Se for imagem jpg
            return("image/jpeg")

        elif(f_type == "html" or "htm"):
            # Se for arquivo html
            return("text/html")
        
        else:
            # Extensões desconhecidas
            return("application/octet-stream")    



# =============================================================
# Main
serverPort = 6996
print("Initializing server...")
print("Port defined: " + str(serverPort))

# Configurações iniciais para o socket
# AF_INET = Usamos configuração IPv4
# SOCK_STREAM = Socket do tipo TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Associa o socket com a porta definida anteriormente
serverSocket.bind(('', serverPort))

# Coloca o socket para "ouvir"
serverSocket.listen(1)
print("Server is up")

while(True):
    # Espera alguma conexão acontecer /  quando nosso socket "aceitar"
    connectionSocket, addr = serverSocket.accept()		
    print("Connection Accepted")
    # Associa o socket com a classe HTTPRequest
    request = HTTPRequest(connectionSocket)

