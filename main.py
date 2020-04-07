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
        moves = []
        for a in range(9): 
            for b in range(9) :
                tower = self.board[a][b]
                if tour != [] : 
                    for c in range(-1,1) : 
                        for d in range(-1,1) : 
                            if a+c > 0 : 
                                if b+d > 0 : 
                                    othertower = self.board[a+c][b+d] 
                                    if othertower != [] :
                                        if c == d == 0 : 
                                            pass
                                        elif len(tower) + len(othertower) <= 5 : 
                                            moves.append([[a,b],[a+c,a+d]])      # on ajoute aux moves possibles les coordonées de respectivement la première et deuxième tour.
        return moves             
 #va falloir tout inclure en un return, donc trouver une manière d'expliciter un mouvement d'une tour à l'autre (faire comme le prof p-e ? sauf que string ), ou alors une liste comme dans le quick example 
 # possiblement créer une liste vide dans possible, à la fin de la fonction faire append dans cette liste des coord, faire un return de toute la liste à la toute fin, en dehors des boucles                                    
    def make_move(self,move) : 
        othertower.extend(tower)
        tower.clear()









if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    #cherrypy.quickstart(Server(),'', 'server.conf')
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())