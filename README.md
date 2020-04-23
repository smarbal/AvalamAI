# Avalam AI
par Sebastien Martinez Balbuena et Edouard de Schiettere de Lophem

## Contenu du répositoire 
+  Le dossier AIGameRunner-master contient le server qui hébergera la partie. Celui-ci a été pris [ici](https://github.com/ECAM-Brussels/AIGameRunner)
+ *inscription.json* contient les informations concernant nos matricules, nom et port utilisé.  
+ *main.py* contient le code principal, c'est à dire le serveur de l'ia.   
+ *register.py* contient la fonction afin d'inscrire notre serveur au gestionnaire de jeu. Cette fonction est lancée dans main.py  

## Méthode choisie pour l'IA 
Nous avons utilisé [EasyAI](https://zulko.github.io/easyAI/) afin de mettre en place. Nous utilisons l'algorythme [SSS*](https://en.wikipedia.org/wiki/SSS*). Celui-ci est, grosso modo, une version d'un algorithme Negamax avec élagage Alpha-Beta, où l'élagage se fait de manière bien plus drastique.  

## Lancement du programme 
### AIGameRunner-master
Il faut d'abord lancer le serveur accueillant la partie, celui-ci se retrouve dans [ce dossier](https://github.com/Seb1903/AvalamAI/tree/master/AIGameRunner-master), en précisant le jeu joué.  
La ligne de commande ressemblera donc à :
PS C:\...\AIGameRunner-master> server.py avalam

### AvalamAI
Il faut ensuite lancer le serveur "joueur". 
Il faut pour cela lancer *main.py* en donnant le port de communication ; ce dernier peut-être au choix, l'inscription s'adapte. 
La ligne de commande ressemblera donc à : 
PS C:\...\AvalamAI> main.py 1234

Il suffit ensuite d'ouvrir http://localhost:3000/ dans un navigateur afin d'observer la partie.
