# Avalam AI
par Sebastien Martinez Balbuena et Edouard de Schiettere de Lophem

## Contenu du répositoire 
+  Le dossier AIGameRunner-master contient le server qui hébergera la partie. Celui-ci a été pris [ici](https://github.com/ECAM-Brussels/AIGameRunner).
+ *inscription.json* contient les informations concernant nos matricules, noms et port utilisés.  
+ *main.py* contient le code principal, c'est à dire le serveur de l'ia.   
+ *register.py* contient la fonction afin d'inscrire notre serveur au gestionnaire de jeu. Cette fonction est lancée dans main.py  

## Méthode choisie pour l'IA 
Nous avons utilisé [EasyAI](https://zulko.github.io/easyAI/) afin de mettre en place l'algorithme [SSS*](https://en.wikipedia.org/wiki/SSS*). Celui-ci est, grosso modo, une version d'un algorithme Negamax avec élagage Alpha-Beta, où l'élagage se fait de manière bien plus drastique.  




## Lancement du programme 
###  Installation du module Cython 
Nous utilisons la librairie [Cython](https://cython.org/) afin d'accélerer notre code. En effet, celui-ci s'excute 6x plus rapidement lorsque nous avons "Cythonisé" nos fonctions les plus gourmandes. 
Il faut dans un premier temps installer Cython :  
`> pip install cython`  
Si ce n'est pas déjà le cas, il faudra ensuite installer les Buildtools C++ pour Visual Studio, [ici](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16),  afin de pouvoir "construire" les fonctions nécesssaires. Ces fichiers sont quand même dans le répositoire, mais il semble, pour une raison obscure, qu'une machine téléchargeant les fichiers doit reconstruire ceux-ci. 

Enfin, il faut lancer la ligne de commande qui installera les modules Cython : 
`> python setup.py install`

Si l'installation pose trop de soucis, une branche *No_Cython* sera disponible dans la partie Branches de ce repositoire où l'utilisation de Cython est évitée, mais où l'algorithme est forcément moins performant. 

### AIGameRunner-master
Il faut d'abord lancer le serveur accueillant la partie, celui-ci se retrouve dans [ce dossier](https://github.com/Seb1903/AvalamAI/tree/master/AIGameRunner-master), en précisant le jeu joué.  
La ligne de commande ressemblera donc à :  
`PS C:\...\AIGameRunner-master>python server.py avalam`

### AvalamAI
Il faut ensuite lancer le serveur "joueur". 
Il faut pour cela lancer *main.py* en donnant le port de communication ; ce dernier peut-être au choix tant qu'il est **< 5000**, l'inscription s'adapte. 
La ligne de commande ressemblera donc à :  
`PS C:\...\AvalamAI>python main.py 1234`
**ici, tout est fait pour lancer une deuxième IA. Pour cela lancez une commande analogue à celle ci-dessus, en assignant un port >5000.**
`PS C:\...\AvalamAI>python main2.py 5678`

Il suffit ensuite d'ouvrir http://localhost:3000/ dans un navigateur afin d'observer la partie.


