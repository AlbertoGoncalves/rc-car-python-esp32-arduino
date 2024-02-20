import socket


def udpMsg(msg):
    # Inicializando client
    # print("Configurando cliente UDP")
    HOST = '192.168.3.18'
    PORT = 1234
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ADDRESS = (HOST, PORT)
    sock.connect(ADDRESS)
    sock.settimeout(10.0)

    # 4 Enviando arquivos ao servidor
    file_paths = msg
    # print("Enviando nomes dos arquivos...")
    for file in file_paths:
        sock.sendall(file.encode())
    sock.sendall("stop".encode())
