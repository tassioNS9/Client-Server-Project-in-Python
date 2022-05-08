
import os, pickle, socket, sys, threading


MB = 64
CACHE_MAXIMA = MB*(1024*1024)

SIZE = 1024

TAMAN_CACHE = 0    # cache inicializa vazia

CACHE = { }
# -----------------

def remover_elemento_cache(tamanho_arq):       #Nessa funcao é uma auxiliar para remover o elemento da cache
   valor_a_remover = 0                          #alem disso ela retorna o tamanho da cache atual
   dado_a_remover = ''
   contador = 0
   for dado in CACHE:
      arquivo = CACHE.get(dado)
      dado_atual = dado
      valor_atual = arquivo['size']
      if(arquivo['size'] >= tamanho_arq):
         valor_a_remover = valor_atual
         dado_a_remover = dado_atual
         break
      else:
         if(valor_a_remover >= contador):
            contador = valor_atual
            valor_a_remover = contador
            dado_a_remover = dado_atual
   CACHE.pop(dado_a_remover)
   return (TAMAN_CACHE - valor_a_remover)

def pegar_arquivos_na_cache():       
   list = []
   for key in CACHE.keys(): 
      list.append(key) 
   return list

def conexao_cliente(directory, connection, address, lock):
   global CACHE
   global TAMAN_CACHE
   
   os.chdir(directory)

   req = connection.recv(SIZE).decode()
   
   print(f'Cliente {address} está solicitando arquivo {req}')      

   if(req == 'list'):
      connection.send(pickle.dumps(pegar_arquivos_na_cache()))  
      connection.close()
      print('Solicitação de cache enviada ao cliente')
   
   else:
      lock.acquire()             # essa parte envia o arquivo ao cliente 
      if(CACHE.get(str(req))):
         print(f'Acerto de cache. Arquivo {req} enviado ao cliente.')
         payload_arq = CACHE.get(str(req))
         data = pickle.loads(payload_arq['data'])
         connection.send(data)
         connection.close()
   
      else:
         if(os.path.isfile(req)):         
            with open(req, 'rb') as arq:
               tamanho_arq = os.path.getsize(req)
               payload_arq = arq.read()
               if(tamanho_arq <= CACHE_MAXIMA):

                  payload_pra_cache = b''
                  while(payload_arq):
                     connection.send(payload_arq)
                     payload_pra_cache += payload_arq
                     payload_arq = arq.read(SIZE)
                  
                  payload_serialize = pickle.dumps(payload_pra_cache)
                  while(TAMAN_CACHE+tamanho_arq > CACHE_MAXIMA):
                     TAMAN_CACHE = remover_elemento_cache(tamanho_arq)
                  
                  to_cache = {str(req): {'size': tamanho_arq, 'data': payload_serialize}}
                  TAMAN_CACHE += tamanho_arq
                  CACHE.update(to_cache)
                  
               else:
                  while(payload_arq):
                     connection.send(payload_arq)
                     payload_arq = arq.read(SIZE)
            arq.close()
            connection.close()
            print(f'Perda de cache. Arquivo {req} enviado ao cliente')
         
         else:
            connection.send(b'Arquivo nao existe!')
            connection.close()
            print(f'Arquivo {req} nao existe!')
   
   lock.release()

if __name__ == "__main__": 

   HOST = 'localhost'    
   PORT = 55555          
   DIRECTORY = sys.argv[2]

   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind((HOST, PORT))
   except:
      print("\nNao foi possivel inicial o servidor!")

   while True:
      s.listen()
      connection, address = s.accept()
      lock = threading.Semaphore()
      novo_cliente = threading.Thread(target=conexao_cliente, args=(DIRECTORY, connection, address, lock))
      novo_cliente.start()
   
   s.close()