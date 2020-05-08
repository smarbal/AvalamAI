# Avalam AI
par Sebastien Martinez Balbuena (18360) et Edouard de Schiettere de Lophem (18072)

## Contenu du répositoire 
+  Le dossier AIGameRunner-master contient le serveur qui hébergera la partie. Celui-ci a été pris [ici](https://github.com/ECAM-Brussels/AIGameRunner).
+ *inscription.json* contient les informations concernant nos matricules, noms et port utilisés.  
+ *main.py* contient le code principal, c'est à dire le serveur de l'ia.   
+ *register.py* contient la fonction afin d'inscrire notre serveur au gestionnaire de jeu. Cette fonction est lancée dans main.py  
+ Les fichiers *.pyx* sont des fichiers contenant des fonctions Python qui prennent beacoup de temps à l'exécution, à cause de nombreuses boucles for. Comme le language C gère ce genre de cas de manière bien plus optimale, ces fichiers seront "Cythonisés". 

## Méthode choisie pour l'IA 
Nous avons utilisé [EasyAI](https://zulko.github.io/easyAI/) afin de mettre en place l'algorithme [SSS*](https://en.wikipedia.org/wiki/SSS*). Celui-ci est, grossièrement, une version d'un algorithme Negamax avec élagage Alpha-Beta, où l'élagage se fait de manière bien plus drastique.    
Cet algorithme construit un arbre et l'explore de manière best-first, en explorant les noeuds les plus prometteurs d'abord, au contraire d'un algorithme alpha-bêta qui agit de manière depth-first. La première solution trouvée doit donc, à priori être la meilleure, ce qui le rend dans beaucoup de cas, plus performant que l'algorithme alpha-bêta, si ce dernier n'utilise pas de tables de transposition, chose qui était comliquée à faire dans le cas du jeu *Avalam*.  
  
De manière pratique, il va donc, par une évaluation heuristique, donner une valeur à chaque noeud et seulement ensuite, il explorera chacun des noeuds par ordre d'importance.
Dans notre cas, en raison des nombreux coups possibles dans le jeu Avalam, l'algorithme est très gourmand dès que l'on passe une profondeur de 3 (19s pour SSS(4) avec Cython, 165s sans Cython, pour le premier coup, avec 20 632 056 moves simulés<sup>1</sup>).  
Nous avons donc décidé d'adapter la profondeur au fur et à mesure que le jeu avançait (lignes 103 à 115). En effet, au plus il y a de moves déjà faits, au moins il y a de cas à explorer, au plus l'algorithme va vite.  
  
Cette faible profondeur nous a handicapés car l'algorithme n'arrive à atteindre des states, en début de partie, où le jeu est fini ; il ne sait donc pas utiliser la fonction win() et par conséquent notre fonction scoring ne sait pas donner des valeurs correctes à l'algorithme pour déterminer quelles branches sont les plus favorables. Nous avons donc dû nous même déterminer quelles actions étaient à privilégier en donnant des valeurs à scoring() via la fonction wintower(), qui détermine si des tours sont capturées ou non (plus des tours sont capturées, plus le score fourni à scoring() est grand). Ces fonctions ont du être "Cythonisées" car elles baissaient nos performances de manière non-négligeable.   

Pour résumer, en début de partie notre algorithme préfère capturer des tours assez rapidement quitte à ce que ce soit moins bénéfique sur le long terme, tandis que lorsque des states où le jeu se termine sont atteignables, l'algorithme va viser le fait de "gagner" (win() a un scoring plus grand que wintower()) et donc aura plus une vision long-terme (ce qui est peu utile en fin de partie, on le concède).

Des pistes intéressantes à explorer pour optimiser notre algorithme seraient de : 
+ Négliger une moitié de plateau au début de partie (empiriquement, nos différentes IA testées ont toujours joué la première vingtaine de coups dans la même moitié); cela permettrait de gagner énormément de temps sans perte de performances, à moins de faire face à un joueur humain jouant un coup sous-optimal dans cette seconde partie de plateau.
+ Utiliser des manières plus performantes d'exécuter make_move() et unmake_move() car ces fonctions prennent à elles deux plus d'1/3 du temps nécessaire à l'exécution lorsque la profondeur est relativement grande.  
  
Néanmoins, tout est toujours perfectible, il faut bien s'arrêter à un moment et nous sommes satisfaits du fonctionnement de l'algorithme.

<sup>1</sup>Analysé grâce à [cProfile](https://docs.python.org/2/library/profile.html)  

## Lancement du programme 
###  Installation du module Cython 
Nous utilisons la librairie [Cython](https://cython.org/) afin d'accélerer notre code. En effet, celui-ci s'exécute 6x plus rapidement lorsque nous avons "Cythonisé" nos fonctions les plus gourmandes. 
Il faut dans un premier temps installer Cython :  
`> pip install cython`   

Si ce n'est pas déjà fait, il faudra ensuite **installer les Buildtools C++** pour Visual Studio, [ici](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16),  afin de pouvoir "construire" les fichiers/fonctions nécesssaires. Même lorsque ces fichiers étaient dans le répositoire, pour une raison obscure, une machine téléchargeant ces fichiers devait reconstruire ceux-ci.  
Lorsque le logiciel d'installation vous demandera quels modules installer, sélectionnez uniquement **C++ Build Tools**.

Enfin, il faut **lancer la ligne de commande** qui construira les fichiers .c via Cython :  
`> python setup.py install`

**Si l'installation pose trop de soucis**, une branche *No_Cython* sera disponible dans la partie Branches de ce repositoire où l'utilisation de Cython est évitée, mais où l'algorithme est forcément moins performant. 

### AIGameRunner-master
Il faut d'abord lancer le serveur accueillant la partie, celui-ci se retrouve dans [ce dossier](https://github.com/Seb1903/AvalamAI/tree/master/AIGameRunner-master), en précisant le jeu joué.  
La ligne de commande ressemblera donc à :  
`PS C:\...\AIGameRunner-master>python server.py avalam`

### AvalamAI
Il faut ensuite lancer le serveur "joueur". 
Il faut pour cela lancer *main.py* en donnant le port de communication ; ce dernier peut-être au choix, l'inscription s'adapte. 
La ligne de commande ressemblera donc à :  
`PS C:\...\AvalamAI>python main.py 1234`

Il suffit ensuite d'ouvrir http://localhost:3000/ dans un navigateur afin d'observer la partie.

NB : Si vous souhaitez lancer une partie pour tester l'IA, la branche *testing-br* permettra de vous faciliter la tâche dans le lancement de 2 IA, puisqu'elle permettra de gérer l'inscription de 2 IA directement à partir de ce repositoire.
