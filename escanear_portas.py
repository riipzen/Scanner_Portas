import socket
import threading
from queue import Queue
import sys

q = Queue()

def escanear_porta(porta): #Criando uma função para escanear as porta automaticamente
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) #Tempo limite para receber uma respota das portas
        resultado = s.connect_ex((ip_alvo, porta)) #Definindo o IP e a PORTA alvo
        if resultado == 0:
            print(f"Porta {porta} esta ABERTA!")
        else:
            print(f"Porta {porta} esta FECHADA!")
        s.close()
    except socket.error:
        print(f"ERRO de conexao na porta {porta}")

def worker(): #Adicionando THREADS para agilizar o processo de Scannear portas
    while True:
        porta = q.get() 
        escanear_porta(porta)
        q.task_done()

ip_alvo = sys.argv[1]
print("Iniciando Varredura de Portas...")

portas = sys.argv[2:]
for porta in portas: #Range onde podemos Scannear a porta da 0 até 1001.
    q.put(int(porta))

num_threads = 50 #Quantidade de THREADS que temos para multi-thread

for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

q.join()
print("Fim da Varredura!")


