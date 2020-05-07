import json
import cherrypy
import sys
import socket
import c_possible_moves
import c_win_tower 
import c_is_alone
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

        class Avalam(TwoPlayersGame):   #permet de décrire la classe "jeu", tout ce qui servira à l'algorithme est ici 
            def __init__(self, players):
                self.players = players
                self.nplayer = 1    
                self.board = body['game']
                self.playerwon = False
                self.thegameisover = False
                self.player.piece = body['players'].index('2 algos 1 cup')
                if self.player.piece == 0 :     # permet d'assigner quels pions appartiennent à notre joueur et à l'opposant
                    self.opponent.piece = 1
                else : 
                    self.opponent.piece = 0
                self.player.list = []  
                self.opponent.list = []
    


            def possible_moves(self):   #va déterminer tous les moves possibles. l'IA ne peut que faire des moves présents dans cette liste. Comme les règles sont bien établies, on est sûrs de jamais avoir de bad move
                moves = c_possible_moves.possible_moves(self.board)     #aller voir le code de c_possible-moves.pyx pour voir comment la recherche se fait
                self.thegameisover = moves == [] 
                return moves




            def make_move(self,move) : 
                self.board[move[1][0]][move[1][1]].extend(self.board[move[0][0]][move[0][1]]) #on verse ce qui se trouve dans la premiere tour dans la deuxieme
                self.board[move[0][0]][move[0][1]].clear() #on vide la première tour

            def unmake_move(self, move):   #sert à accélérer l'IA car permet de retrouver un état précédent en défaisant un move (plutôt qu'utiliser la mémoire). 
                i = 0
                cache = []
                while i < move[2] :
                    lastpiece = self.board[move[1][0]][move[1][1]].pop()    #on enlève le même nombre de pièces qui ont été déplacées par le move, 1 à 1, puis on inverse le sens de la liste pour retrouver l'état initial 
                    cache.append(lastpiece)
                    i += 1
                cache.reverse()
                self.board[move[0][0]][move[0][1]].extend(cache)
                

            def wintower(self) : #détermine combien de tours appatiennent à un joueur, sert pour la fonction scoring()
                return c_win_tower.wintower(self.board, self.player.piece)  + c_is_alone.is_alone(self.board, self.player.piece)



            def win(self):  #détermine le gagnant. L'IA optimise évidemment pour que player > opponent
                if self.thegameisover is True : 
                    self.player.list.clear()                        #sinon à chaque fois qu'il simule une possibilité, il rajoute dans la liste de pions totale, qui a gardé les pions de la simulation précédente
                    self.opponent.list.clear()
                    for a in range(9): 
                        for b in range(9) :
                            tower = self.board[a][b]
                            if tower != [] :
                                piece = tower[-1]     #avec pop il retire à chaque unmake move sur la fin vu qu'il lance la fonction pour faire la simulation, donc utilisaton du [-1] 
                                if piece == self.player.piece : 
                                    self.player.list.append(piece)
                                else : 
                                    self.opponent.list.append(piece)
                    return len(self.player.list) > len(self.opponent.list)

            def is_over(self) : 
                return self.possible_moves() == []
                    
            
            def scoring(self): #on donne ici les scores, pour qu'il prilégie l'une ou l'autre action, plus de détails dans le README 
                if self.wintower() != 0 : 
                    return 3*self.wintower()
                elif self.win() is True : 
                    return 100 
                else : 
                    return 0 
                
            def show(self) : #nous permet de voir le board quand on lance une partie (un peu inutile ici avec le serveur)
                print(self.board) 
                
     
        if len(body['moves']) <= 25 :  #sert à déterminer la profondeur de recherche, SSS pourrait être remplacé par Negamax mais c'est moins performant
            ai_algo = SSS(3)
            ai_algo2 = SSS(3)
            
        if 25 < len(body['moves']) <= 40 :
            ai_algo = SSS(5)
            ai_algo2 = SSS(3)
        
        if  40 < len(body['moves']) <= 150  :
            ai_algo = SSS(6)
            ai_algo2 = SSS(3)


        game =  Avalam([AI_Player(ai_algo), AI_Player(ai_algo2)])    #dit que game est de classe Avalam et détermine les algorithmes à utiliser
        #game.play(1)
        movelist = game.get_move()   #permet de prendre en une liste le move fait.[[postion initiale],[position finale],[nombre de pions déplacés]]
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
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())

    
