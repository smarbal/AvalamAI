import json
import cherrypy
import sys
import socket
from register import register
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax
from Algorythm import Avalam

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
        
        if len(body['moves']) < 6  :
            ai_algo = Negamax(3)
            ai_algo2 = Negamax(3)
        
        if len(body['moves']) > 6  :
            ai_algo = Negamax(8)
            ai_algo2 = Negamax(8)
        game =  Avalam([AI_Player(ai_algo), AI_Player(ai_algo2)])
        game.play(1) 
        movelist = [[5,6],[5,7]]
        return {"move": {
            
        'from' : [5,6],
        'to':    [5,7]
        
        },
        "message" : "Bien le bonjour"
        }
        
    @cherrypy.expose
    def ping(self):
        return "pong"


class Avalam(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1    #si joueur 1 commence, à àméliorer si joueur 2 commence, à voir avec le fichier json 
        self.board = body['game']
        self.playerwon = False
        self.thegameisover = False


    def possible_moves(self):
        self.moves = []
        for a in range(9): 
            for b in range(9) :
                tower = self.board[a][b]
                if tower != [] : 
                    for c in range(-1,2) : 
                        for d in range(-1,2) : 
                            if a+c >= 0 and a+c < 9: 
                                if b+d >= 0 and b+d <9: 
                                    othertower = self.board[a+c][b+d] 
                                    if othertower != [] :
                                        if c == d == 0 : 
                                            pass
                                        elif len(tower) + len(othertower) <= 5 : 
                                            self.moves.append([[a,b],[a+c,b+d], len(tower)])  
                                                # on ajoute aux moves possibles les coordonées de respectivement la première et deuxième tour. exemple de move : [[0, 3], [0, 4]]
        return self.moves
        print(self.moves)



    def make_move(self,move) : 
        self.board[move[1][0]][move[1][1]].extend(self.board[move[0][0]][move[0][1]]) #on verse ce qui se trouve dans la premiere tour dans la deuxieme
        self.board[move[0][0]][move[0][1]].clear() #on vide la première tour

    def unmake_move(self, move):
        i = 0
        oldtower = []
        while i < move[2] :
            lastpiece = self.board[move[1][0]][move[1][1]].pop()
            self.board[move[0][0]][move[0][1]].append(lastpiece)
            i += 1
        


    def win(self):
        playerpiece = body['players'].index('LUR')
        opponentlist = []  
        playerlist = []
        if self.thegameisover() is True :  
            for a in range(9): 
                for b in range(9) :
                    tower = self.board[a][b]
                    if tower != [] :
                        piece = tower.pop()
                        if piece == playerpiece : 
                            playerlist.append(piece)
                        else : 
                            opponentlist.append(piece)
        return len(playerlist) > len(opponentlist)
        self.playerwon = len(playerlist) > len(opponentlist)

    def is_over(self) : 
        return self.possible_moves() == []
        self.thegameisover = self.possible_moves() == []
            
    
    def scoring(self):
            if self.playerwon is True : 
                return 100 
            else : 
                return 0 
        
    def show(self) :
        print(self.board) 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080
    #cherrypy.quickstart(Server(),'', 'server.conf')
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())

    
     #adapter pour renvoyer le move vers le serveur
    #à tester, l'avantage c'est que comme on joue du tour par tour, on va pouvoir adapter Negamax()