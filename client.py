
import os, pickle, socket, sys

SIZE = 1024      #tamanho da quantidade de bits

def list_cache_req(client, req):    
    client.send(req.encode())
    arquivos_na_cache = client.recv(SIZE)
    print(pickle.loads(arquivos_na_cache))

def arquivo_req(directory, client, req):
    os.chdir(directory)
    client.send(req.encode())

    with open(req, 'wb') as arq:    
        possui_arq = True;
        while True:
            data = client.recv(SIZE)
            if(data == b'Arquivo nao existe'):
                print('Arquvivo nao existe!')
                os.remove(req)
                possui_arq = False
                break
            if not data:
                break
            arq.write(data)
    arq.close()
    if(possui_arq):
        print(f'Arquivo {req} salvo!')
    client.close()

if __name__ == "__main__":
    
    HOST = 'localhost'   
    PORT = 55555            
    req = sys.argv[3]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except:
        print("\n Não foi possivel conectar ao servidor!\n")
    
    print('Usuario Conectado!')

    if(req == 'list'):
        list_cache_req(client, req)
    else:
        DIRECTORY = sys.argv[4]
        arquivo_req(DIRECTORY, client, req)