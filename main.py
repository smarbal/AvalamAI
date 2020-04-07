import json
import cherrypy
import sys
import socket
from register import register
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax

register(3001)

class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''
        
        body = cherrypy.request.json
        print(body)
        return {"move": {
            
        'from' : [0,3],
        'to':    [1, 4] 
        
        },
        "message" : "Bien le bonjour"
        }
    
class Avalam(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1    #si joueur 1 commence, à àméliorer si joueur 2 commence, à voir avec le fichier json 
        self.board = body['game'] 
    
    def possible_moves(self):
        for line self.board : 
            for tour in line : 
                if tour != '' : 
                    
                    if othertour != '' : 
                        if othertour != '':
                            if len(tour) + len(othertour) <= 5 : 
                                return othertour.extend(tour)
                                return tour.clear()










if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    #cherrypy.quickstart(Server(),'', 'server.conf')
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())