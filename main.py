import json
import cherrypy
import sys
import socket
from register import register
from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax, SSS
import random 


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

        class Avalam(TwoPlayersGame):
            def __init__(self, players):
                self.players = players
                self.nplayer = 1    #si joueur 1 commence, à àméliorer si joueur 2 commence, à voir avec le fichier json 
                self.board = body['game']
                self.playerwon = False
                self.thegameisover = False
                self.player.piece = body['players'].index('Ton IA va faire Aie')
                if self.player.piece == 0 :
                    self.opponent.piece = 1
                else : 
                    self.opponent.piece = 0
                self.player.list = []  
                self.opponent.list = []
    


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
                cache = []
                while i < move[2] :
                    lastpiece = self.board[move[1][0]][move[1][1]].pop()     #checker, peut etre une erreur dans ces lignes 
                    cache.append(lastpiece)
                    i += 1
                cache.reverse()
                self.board[move[0][0]][move[0][1]].extend(cache)
                

            def wintower(self) : 
                for a in range(9): 
                    for b in range(9) :
                        tower = self.board[a][b]
                        if len(tower) == 5 :
                            piece = tower[4]     
                            if piece == self.player.piece : 
                                return True 
            
            def win(self):
                if self.thegameisover is True : 
                    self.player.list.clear()                        #sinon à chaque fois qu'il lance une possibilité, il rajoute dans la liste, qui a gardé les pions de la simulation précédente
                    self.opponent.list.clear()
                    for a in range(9): 
                        for b in range(9) :
                            tower = self.board[a][b]
                            if tower != [] :
                                piece = tower[len(tower)-1]     #avec pop il retire à chaque unmake move sur la fin vu qu'il lance la fonction 
                                if piece == self.player.piece : 
                                
                                    self.player.list.append(piece)
                                else : 
                                    self.opponent.list.append(piece)
                    return len(self.player.list) > len(self.opponent.list)

            def is_over(self) : 
                self.thegameisover = self.possible_moves() == []   #inverser l'ordre ?
                return self.possible_moves() == []
                    
            
            def scoring(self):
                if self.wintower() is True : 
                    return 10
                elif self.win() is True : 
                    return 100 
                else : 
                    return 0 
                
            def show(self) :
                print(self.board) 
                
     
        if len(body['moves']) <= 30 :
            ai_algo = SSS(3)
            ai_algo2 = SSS(3)
            
        if len(body['moves']) > 30 :
            ai_algo = SSS(4)
            ai_algo2 = SSS(4)
        

        game =  Avalam([AI_Player(ai_algo), AI_Player(ai_algo2)])
        #game.play(1)
        movelist = game.get_move()

        messagelist = ["Ton IA va faire aïe","On va tellement te défoncer que tu vas finir sur Giteub","C'est une IA qui joue là ou c'est aléatoire ?",
        "Tu feras mieux la prochaine fois"," T'aurais mieux fait d'étudier mécaflotte que de coder ça", "Souriez, vous êtes cernés", "Elle est où ma limonaaaaaaaade ?", 
        "Cython AI marche pas, reviens l'année prochaine","On me dit à l'oreillette que t'auras pas les 2.5 points bonus","  J’adore l’odeur de la victoire au petit matin",
        " Tu vois, le monde se divise en deux catégories: ceux qui ont une IA chargée et ceux qui creusent. Toi tu creuses.","Trois syllabes, huit lettres et un seul sens : T'as perdu.",
        " Figurez-vous que votre IA n’est pas moche, elle n’a pas un physique facile… c’est différent.","C’est pas ton IA qui va voler nos jobs",
        "C'est quand même bien mieux une IA propre, non ? À l'occasion, je vous mettrai un petit coup de polish.","23-0 ! C'est la piquette Jack !!! Tu sais pas jouer, Jack ! T'es mauvais hahahahaha !!!",
        "On est en 1955 les gars, faut se réveiller. Les boucles for partout, ne pas utiliser Cython, l'écriture illisible, ça va hein ! S'agirait de grandir ! S'agirait de grandir...",
        "Une défaite c'est quand les IA sont communistes, déjà. Qu'elles ont froid, avec des chapeaux gris et des chaussures à fermeture éclair. C'est ça, une défaite, Dolorès",
        "Ça fait un peu Jacadi a dit : « Pas de bon move !","Chou blanc donc…","J'appelle ça l'IA, mademoiselle. Et pas n'importe laquelle ; l'IA du général de Gaulle.","Ou tu sors ou je te sors...","Je ne crois pas qu'il y ait de bonne ou de mauvaise IA...ah bah si, la tienne",
        "Alors, on n'attend pas Patrick ?","Cassé !!!","J'ai glissé chef...","Les IA connes ça ose tout. C’est même à ça qu’on les reconnait",
        "Une grande IA implique de grandes responsabilités","Faut arrêter ces conneries de nord et de sud ! Une fois pour toutes, le nord, suivant comment on est tourné, ça change tout !",
        "Ah ! oui... j' l'ai fait trop fulgurant, là. Ça va ?","Une fois, à une exécution, je m'approche d'une fille. Pour rigoler, je lui fais : « Vous êtes de la famille de l'IA ? »... C'était sa sœur. Bonjour l'approche !","On en a gros !",
        "PAYS DE GALLES INDÉPENDAAAAANT !","SI VOUS VOULEZ QU'ON SORTE LES PIEDS DEVANT, FAUDRA NOUS PASSER SUR L'COOOORPS !",
        "Je vu ton IA une fois dans une carriole, tirée par un cheval. Enfin, la carriole tirée par un cheval.","Mais cherchez pas à faire des phrases pourries... On en a gros, c'est tout !","Vous, vous avez une idée derrière la main, j'en mettrais ma tête au feu!",
        "Faut pas respirer la compote, ça fait tousser."," Et deux jus de pomme qui piquent !","Nouvelle technique : on passe pour des cons, les autres se marrent, et on frappe. C’est nouveau."]  #répliques librement inspirées d'OSS 117, Kaamelott, Rap Contenders,... et notre imagination. 
        return {"move": {
            
        'from' : movelist[0],
        'to':    movelist[1]
        
        },
        "message" : messagelist[random.randint(0, len(messagelist)-1)]
        }
        
    @cherrypy.expose
    def ping(self):
        return "pong"
    





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
