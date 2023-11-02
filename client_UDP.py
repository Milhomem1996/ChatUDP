import socket
import threading

# Endereço IP e porta do servidor
host = '10.113.60.217'  # Endereço IP do servidor
porta = 12345  # Porta do servidor

# Tamanho máximo de dados a serem recebidos de uma vez
tamanho_maximo = 1024

# Função para receber mensagens do servidor
def receber_mensagens(socket_cliente):
    while True:
        try:
            dados, _ = socket_cliente.recvfrom(tamanho_maximo)
            mensagem = dados.decode('utf-8')
            print(f"Recebido do servidor: {mensagem}")
        except UnicodeDecodeError:
            print("Erro de decodificação (não UTF-8)")

# Função para enviar mensagens para o servidor
def enviar_mensagens(socket_cliente):
    while True:
        mensagem = input("Digite a mensagem: ")
        if mensagem == ".contatos":
            # Comando para solicitar a lista de contatos
            socket_cliente.sendto(mensagem.encode('utf-8'), (host, porta))
        elif mensagem.startswith("."):
            # Comando para enviar mensagem para um contato específico
            socket_cliente.sendto(mensagem.encode('utf-8'), (host, porta))
        else:
            # Enviar mensagem normal
            socket_cliente.sendto(mensagem.encode('utf-8'), (host, porta))

# Configuração do cliente UDP
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_cliente.bind(('0.0.0.0', 0))  # Associa o cliente a uma porta local aleatória

# Inicializa threads para receber e enviar mensagens
thread_recebimento = threading.Thread(target=receber_mensagens, args=(socket_cliente,))
thread_envio = threading.Thread(target=enviar_mensagens, args=(socket_cliente,))

thread_recebimento.start()
thread_envio.start()

# Aguarda as threads finalizarem (isso nunca será executado no loop acima)
thread_recebimento.join()
thread_envio.join()

print("Cliente encerrado.")
socket_cliente.close()
