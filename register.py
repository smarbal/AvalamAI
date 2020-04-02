import json 
import socket 
import sys 

if int(sys.argv[1]) < 5000 : 
    with open('inscription.json','r') as file : 
        data = json.load(file)
        data['port'] = int(sys.argv[1])
        d = json.dumps(data)
    with open('inscription.json','w') as file :    
        file.write(d)
    def register(variableport) : 
        host = socket.gethostname()
        port = variableport
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        with open('inscription.json') as file: 
            msg = file.read().encode('utf8')
            total = 0
            while total < len(msg):
                sent = s.send(msg[total:])
                total += sent

if int(sys.argv[1]) > 5000 : 
    with open('inscriptionbis.json','r') as file : 
        data = json.load(file)
        data['port'] = int(sys.argv[1])
        d = json.dumps(data)
    with open('inscriptionbis.json','w') as file :    
        file.write(d)
    def register(variableport) : 
        host = socket.gethostname()
        port = variableport
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
        with open('inscriptionbis.json') as file: 
            msg = file.read().encode('utf8')
            total = 0
            while total < len(msg):
                sent = s.send(msg[total:])
                total += sent