import json
import cherrypy
import sys
import socket

from register import sendJSON 

host = socket.gethostname()
port = 1888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(host, port))

with open('inscription.json') as file : 
    sendJSON(host, file)