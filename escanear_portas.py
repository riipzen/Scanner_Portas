import socket
import threading
from queue import Queue

q = Queue()

def escanear_porta(porta): #Criando uma função para escanear as porta automaticamente
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) #Tempo limite para receber uma respota das portas
        resultado = s.connect_ex((ip_alvo, porta)) #Definindo o IP e a PORTA alvo
        if resultado == 0:
            print(f"Porta {porta} esta ABERTA!")
        s.close()
    except socket.error:
        print(f"ERRO de conexao na porta {porta}")

def worker(): #Adicionando THREADS para agilizar o processo de Scannear portas
    while True:
        porta = q.get() 
        escanear_porta(porta)
        q.task_done()

ip_alvo = "192.168.1.19"
print("Iniciando Varredura de Portas...")

for porta in range (0, 1001): #Range onde podemos Scannear a porta da 0 até 1001.
    q.put(porta)

num_threads = 50 #Quantidade de THREADS que temos para multi-thread

for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

q.join()
print("Fim da Varredura!")


