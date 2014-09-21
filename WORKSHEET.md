![](images/FWW_Centenary__Led_By_IWM_Red-web.png)

# Introduction: Qu'est-ce que le Morse ?

![](images/qst_may_1942.png)

Inventé par [Samuel Morse](http://en.wikipedia.org/wiki/Samuel_F._B._Morse) durant les années 1836, le Code Morse set une méthode pour envoyer et recevoir des messages textuels en utilisant des impulsions longues ou courtes. Conventionnellement, une impulsion courte est appelée un *Point* et une impulsion longue est appelée un *Trait* (Aussi connus comme *Ti* et *Taah*). À chaque lettre de l'alphabet correspond une unique suite de points et traits.

En se référant à l'image suivante, la lettre **A** est Bip Biiiiip et la lettre **B** est Biiiiip Bip Bip Bip.

![](images/morse.png)

- L'unité temporelle est le point
- Un trait à une durée de trois points
- Chaque point ou trait est séparé d'un silence (Généralement d'une durée d'un point)
- Les lettres dans un mots sont séparées d'un silence un peu plus long (généralement 3 points)
- Les mots sont séparés d'un silence encore plus long (généralement 7 points)

Il n'est pas nécessaire d'utiliser de son pour transmettre du morse, bien que ça soit le moyen le plus utilisé.
Il est possible de transmettre du morse avec tout ce qui peut être allumé et éteint : comme une lampe torche, un drapeau que l'on monte et descend, ou même juste en clignant des yeux rapidement ou lentement. C'est ce qui fait du Morse la forme de communication la plus polyvalente. Il y a même une convention internationale qui utilise le Morse pour le SOS `... --- ...` ("Save Our Souls") comme un signal universel de détresse.

Durant les années 1890, le Morse a été adapté pour être utilisé sur les premières [radio](http://fr.wikipedia.org/wiki/Radiodiffusion) avant même qu'il soit possible d'émettre et recevoir de la voix. Ça a été simplement réalisé en envoyé des impulsions sur une onde porteuse à une fréquence normalisée. La radio réceptrice était conçue pour jouer une note lorsqu'elle captait la porteuse. Il a été beaucoup utilisé durant les Guerres Mondiales, et est toujours utilisé de nos jours par des amateurs de radio.

Ainsi, voici les trois éléments pour maîtriser le Morse :
   - Connaitre le code
   - Être capable de le taper
   - Être capable de le décoder en l'écoutant

Le choix des suites de points et traits pour chaque lettre n'a pas été choisi au hasard. Samuel Morse les a déterminé à partir de la fréquence d'utilisation des lettres dans la presse locale anglaise. Plus la lettre était utilisée, plus sa séquence serait courte, pour la taper rapidement.

Le graphique ce dessous est l'arbre de codage Morse, et est particulièrement utile lorsque l'on écoute et décode : il est alors utile de l'imprimer et l'avoir systématiquement à portée d'yeux. Vous pouvez remarquer que **E** et **T** sont les lettre les plus utilisées. Ainsi, on débute en haut de l'arbre, et si l'on entend un point, on se déplace sur la branche de gauche, et si l'on entend un trait, on se déplace sur la branche de droite. Vous pouvez vérifier le code des caractères avec le premier document : essayez avec les lettres **A** et **B**.

![listening](images/morse_listening.png)

Prenez un papier et un crayon et regardez comment vous vous débrouillez avec ceci : [Écouter "Code Morse Lent"](./sounds/slow_morse.mp3). Ne soyez pas rebuté si vous trouvez ceci difficile : c'est toujours difficile au début. Comme avec beaucoup de choses, plus vous pratiquez, plus ça vous semble simple. Dans ce document, nous allons programmer un Raspberry Pi pour vous aider à apprendre le Morse.
Vous allez fabriquer votre propre outil d'apprentissage qui vous dira si vous avez réussi ou non. Installons tout ça !

## Étape 0 : Préparation du Pi

Tout d'abord, vérifions que vous avez toutes les pièces nécessaires pour installer votre Rapsberry Pi :

- Un Raspberry Pi
- Une alimentation Micro USB
- Une carte SD avec Raspbian configurée avec NOOBS
- Un clavier USB
- Une souris USB
- Un câble HDMI
- Un écran ou une TV

### Procédure :

1. Insérer la carte SD dans l'emplacement dédié du Raspberry Pi
1. Ensuite, connecter le câble HDMI à l'écran/TV.
1. Brancher le clavier et la souris.
1. Brancher l'alimentation Micro USB.
1. Lors de la demande d'authentification, renseigner :

    ```bash
    Login: pi
    Password: raspberry
    ```

## Étape 1 : jouer un Bip de test

Il est conseillé d'utiliser des écouteurs si vous êtes dans une salle de classe, afin d'éviter une cacophonie. Si vous avez *branché* des écouteurs ou des haut-parleurs sur le Raspberry Pi, vous pouvez lancer la commande suivante pour rediriger le son sur la prise écouteurs :

`sudo amixer cset numid=3 1`

Ensuite, nous allons utiliser la bibliothèque Python `pygame` pour jouer quelques notes.
Tout d'abord, vérifions que la librairie est bien installée grâce à la commande suivante :

`sudo apt-get install python-pygame -y`

Si votre carte SD est à jour, vous devriez lire :

`python-pygame is already the newest version`

Bien, maintenant, passons à la programmation. Je vais vous fournir un peu de code pour jouer une note, il n'est pas nécessaire de se pencher sur son fonctionnement interne. Cependant, pour ceux qui sont intéressés, le code hérite de la classe son de `pygame`, et génère automatiquement les données de l'onde pour jouer une note à une fréquence précise.

Entrez la commande suivante pour éditer un fichier vierge :

`nano morse-code.py`

Maintenant, copiez-collez ou recopiez le code suivant :

```python
#!/usr/bin/python
import pygame, time
from array import array
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

class ToneSound(pygame.mixer.Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples
```

Si vous n'avez jamais vu une [classe](http://fr.wikipedia.org/wiki/Classe_(informatique)) Python auparavant, pas de panique. Une classe est comme un "patron" de code que vous pouvez réutiliser plusieurs fois. Une instance de classe s'appelle un [Objet](http://fr.wikipedia.org/wiki/Programmation_orient%C3%A9e_objet).

La fréquence typique du code Morse est entre 400 Hz et 1000 Hz, donc nous allons utiliser 800 Hz. Dans ce code `tone_obj` est l'objet qui a été créé depuis le patron `ToneSound`.

Ajoutez le code suivant à la toute fin du fichier :

```python
tone_obj = ToneSound(frequency = 800, volume = .5)

tone_obj.play(-1) #the -1 means to loop the sound
time.sleep(2)
tone_obj.stop()
```

Appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer, suivi de `Ctrl + X` pour quitter.

Ensuite, marquons le fichier comme exécutable via la commande suivante :

`chmod +x morse-code.py`

Maintenant, nous pouvons lancer le code. Lorsque vous le faites, vous devriez entendre un agréable Bip de deux secondes :

`./morse-code.py`

Si vous n'avez rien entendu, revérifiez que tout est bien branché. Si vous utilisez la sortie écouteurs du Pi, vous devez utiliser la commande `sudo amixer cset numid=3 1` pour rediriger le son. Vous pouvez remarquer que la note semble tremblotante au début : c'est simplement un artefact de `pygame`, qui lors de son démarrage nécessite quelques cycles de CPU en plus. Les notes suivantes sonneront plus juste.

## Étape 2 : Connecter la clé Télégraphique aux ports GPIO

![](images/p1.png)

### La théorie

Toutes les clés télégraphiques fonctionnent comme un bouton poussoir ou un interrupteur. Elles ont deux vis terminales pour y connecter un fil positif, et un négatif. Lorsque vous appuyez sur la clé, deux pièces de métal se touchent, causant la fermeture du circuit. L'effet serait le même si vous connectiez simplement les deux fils ensemble.

Pour connecter la clé télégraphique aux pins GPIO, il faut un peu de réflexion physique. Les pins GPIO peuvent être définis comme entrée ou sortie. La sortie est utilisée lorsque l'on veut fournir de la tension à un périphérique, comme une LED ou un buzzer. Si l'on l'utilise en mode entrée, le pin GPIO va alors être doté d'une valeur, qu'il sera possible de lire dans notre code. Si le pin est soumis à une tension, alors sa valeur sera `1` (*HIGH*), si le pin est connecté directement à la masse (tension nulle), alors sa valeur sera `0` (*LOW*).

Ainsi, le but est d'utiliser la clé télégraphique pour permettre ou non le passage de la tension jusqu'au pin GPIO, et ainsi faire changer la lecture de la valeur du pin *dans notre code* lorsque l'on appuie sur la clé.

Lorsqu'un pin GPIO est en mode entrée, alors le pin est dit *flottant*, ce qui signifie qu'il n'a pas de tension fixe. Ce n'est pas pratique pour ce que l'on veut, puisque le pin navigue aléatoirement entre HIGH et LOW. On a expressément besoin de savoir si la clé est pressée ou non. Donc on doit fixer la tension du pin GPIO à HIGH ou LOW, et le changer *uniquement* lorsque la clé est pressée.

On peut faire ceci de deux manières :

- Un circuit avec une résistance de tirage (*Pull up*)

  Brancher le pin GPIO au 3,3 volts via une résistance de 10kΩ, de sorte qu'on lise toujours HIGH. Puis l'on peut court-circuiter le pin à la masse via la clé télégraphique, pour que le pin vaille LOW lorsqu'on la presse.

  ![](images/pull_up.png)

- Un circuit avec une résistance de rappel (*Pull down*)
  Brancher le pin GPIO à la masse via une résistance de 10kΩ de sorte qu'on lise toujours LOW. Puis l'on peut court-circuiter le pin au 3,3 volts via la clé télégraphique, pour que ça vaille HIGH lorsqu'on la presse. Lorsque la clé est appuyée, il y a une résistance plus faible pour le chemin vers 3,3 vols, et ainsi le pin sera à HIGH.

  ![](images/pull_down.png)
  
  *Note: La résistance R2 de 10kΩ est présente dans les deux circuits pour donner aux pin GPIO une protection au cas où l'on configure par erreur le pin en mode sortie.*

### La pratique

Heureusement, le Raspberry Pi a tous les circuits précédents *embarqués* et l'on peut sélectionner le mode pull up ou pull down au *sein de notre code* pour chaque pin GPIO. Cetùte configuration paramètre des circuits qui sont bien trop petits pour que l'on puisse les voir. Ainsi vous pouvez vous en sortir avec simplement deux fils, mais vous pouvez le brancher de la manière vue au-dessus si vous le souhaitez. Par exemple, utilisons le pin numéro 7 :

- Configuration Pull up

  Le pin GPIO n°7 va être branché au 3,3 volts en utilisant une résistance interne de pull up, pour que l'on lise toujours HIGH. Ensuite on peut court-circuiter le pin à la masse via la clé télégraphique, pour que le pin vaille toujours LOW lorsque l'on appuie sur la clé.

  ![](images/pull_up_key.png) 

- Configuration Pull down

  Le pin GPIO n°7 va être branché à la masse en utilisant une résistance interne de pull down, pour que l'on lise toujours LOW. Ensuite on peut court-circuiter le pin au 3,3 volts via la clé télégraphique, pour que le pin vaille toujours HIGH lorsque l'on appuie sur la clé.

  ![](images/pull_down_key.png) 

Chaque méthode fonctionne aussi bien, la solution adoptée par chacun est souvent due à une préférence personnelle. Prenez les deux fils et vissez une extrémité sur les vis de la clé. Sur certaines très vielles clés, cela peut être très délicat.

![](images/jumper_wires_key.png) 

Choisissez la configuration pull up ou pull down que vous voulez utiliser et connectez l'autre extrémité de chaque fils sur les pins GPIO appropriés de votre Raspberry Pi, vous pouvez utiliser l'image ce-dessus comme guide. *Prenez note de la configuration que vous utilisez, car vous allez devoir la renseigner lors de la programmation*

## Étape 3 : Détecter l'état de la clé via la valeur du pin GPIO

Entrez la commande suivante pour éditer notre programme précédent :

`nano morse-code.py`

Pour avoir accès aux pins GPIO depuis notre code, il faut importer la librairie `RPi.GPIO`.
Ajoutez `RPi.GPIO as GPIO` au début du fichier, dans les `import` pour que ça devienne :

`import pygame, time, RPi.GPIO as GPIO`

À la fin, supprimez ces lignes (on les réajoutera plus tard) :

```python
tone_obj.play(-1)
time.sleep(2)
tone_obj.stop()
```
Copiez-Collez ou recopiez le code suivant. La commande `GPIO.setup` est importante. Cette ligne a deux fonctions : configurer le pin 7 en mode entrée, *et* configurer une résistance interne de pull up pour ce pin. Si vous souhaitez utiliser une résistance de pull down, vous devez utiliser `GPIO.PUD_DOWN` à la place.

Ensuite, il y a une boucle `while`, qui lit en continu l'état du pin 7 et écrit HIGH ou LOW à l'écran à chaque seconde.

```python
pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    reading = GPIO.input(pin)
    print "HIGH" if reading else "LOW"
    time.sleep(1)
```

Appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer, suivi de `Ctrl + X` pour quitter.

Les fonctions GPIO nécessitent un accès root à votre Pi, donc à partir de maintenant, vous devez utiliser la commande sudo lorsque vous exécutez votre code. Si vous n'utilisez pas sudo, vous aurez alors l'erreur suivante : `No access to dev/mem. Try running as root!`

`sudo ./morse-code.py`

Si vous utilisez une pull up, le programme devrait afficher HIGH quand la clé est haute. Appuyez sur la clé quelques secondes, et vous devriez lire LOW. C'est l'inverse lorsque vous utilisez une pull down. La sortie du programme devrait ressembler à quelque chose comme ceci :

```bash
HIGH
HIGH
HIGH
LOW
LOW
LOW
HIGH
HIGH
HIGH
```

Appuyez sur `Ctrl + C` pour quitter.

## Étape 4 : Jouer une note lorsque la clé est appuyée

Nous avons prouvé que la valeur du pin GPIO change bien lorsque l'on presse la clé télégraphique, donc l'électronique est maintenant faite. Mais notre code est encore très simple. Tout ce que l'on a c'est une boucle qui sonde perpétuellement le pin, le code ne réagit pas à une pression ou relâchement de la clé. Vous remarquerez que nous pouvez appuyer et relâcher la clé plusieurs fois en une seconde sans que le code ne le détecte.

Pour le code Morse, nous devons répondre à chaque pression/relâchement de la clé en jouant ou stoppant la note.

**Remarque** : Les personnes les plus expérimentée lisant ce guide penseront à utiliser des interruptions matérielles ici. C'est pris en charge par la librairie `RPi.GPIO` avec les fonctions `add_event_detect` et `wait_for_edge`. **Ne vous précipitez pas sur cette solution.** L'utilisation des interruptions matérielles est problématique ici. Vous remarquerez qu'après quelques frénétiques tapotements, il n'est plus capable de distinguer un front montant d'un front descendant, et votre note sera jouée aux mauvais moments.

La façons la plus fiable de faire ceci en utilisant la librairie `RPi.GPIO` est d'écrire quelques fonctions qui suspendent l'exécution de votre code tant que la clé est pressée ou relâchée. Le principe général ici serait l'algorithme suivant :

- Boucle
  - Attendre que la clé soit pressée
  - Commencer à jouer la note
  - Attendre que la clé soit relâchée
  - Arrêter de jouer la note

Ceci est réalisable en définissant deux fonctions `wait_for_keyup` et `wait_for_keydown`. Ces fonctions utiliseront une boucle `while` qui fera patienter votre Pi jusqu'à ce que l'état du pin change. Vous devez être attentif à la configuration pull up ou down que vous utilisez. Par exemple, si vous utilisez une pull up, la logique dans la fonction `wait_for_keydown` sera *tant que le pin 7 est HIGH, attendre*, donc tant que la clé est relâchée, le pin sera HIGH. Quand la clé est pressée, la pin deviendra LOW, et on peut arrêter d'attendre et commencer à jouer la note. En revanche, pour une pull down, la logique sera *tant que le pin 7 est LOW, attendre*. De manière à avoir un bon temps de réponse, nous avons besoin d'attendre un très court moment entre chaque itération de boucle. Un centième de seconde est idéal (0,01 seconde).

La fonction `wait_for_keyup` sera donc la même, mais avec la logique opposée de ce qu'il y aura dans `wait_for_keydown`.

Jetez un œil au code ci-dessous. C'est pour une configuration pull-up, si vous utilisez une pull down, votre ligne contenant `GPIO.setup` aura alors `GPIO.PUD_DOWN` et il vous faut simplement déplacer le `not` du `wait_for_keyup` au même endroit dans le `wait_for_keydown`.

```python
def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)
	
def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print "Ready"

while True:
    wait_for_keydown(pin)
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    tone_obj.stop()
```
Entrez la comande suivante pour éditer notre programme précédent :

`nano morse-code.py`

Laissez la classe `ToneSound` en haut de notre programme, descendez en bas, supprimez la boucle `while` présente, et ajoutez le code ci-dessus. Si nécessaire, modifiez le pour une configuration pull down.

Appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer, suivi de `Ctrl + X` pour quitter.

Vous pouvez maintenant tester votre code. N'oubliez pas d'utiliser la commande `sudo`.

`sudo ./morse-code.py`

Après que vous ayez lu le message `Ready`, vous devriez être capables de commencer à taper vos premiers messages en Morse. Testez bien la clé pour vérifier que la note n'est jouée que lorsque la clé est pressée, et que la note n'est pas jouée lorsque la clé est relâchée. Si c'est inversé, vérifiez la logique dans les fonctions `wait_for_keyup` et `wait_for_keydown`. Vous devriez juste avoir besoin de déplacer le `not`.

Ensuite, vous pouvez essayer de taper quelques mots. Les premiers Nokias utilisaient le Morse pour notifiez qu'un SMS était arrivé. C'est un mot très facile à taper : le Morse pour SMS est `... -- ...`, et vous êtes libres de rechercher *sonnerie sms nokia* pour vérifier. Essayez d'autres mots en vous aidants des images précédentes.

Appuez sur `Ctrl + C` pour quitter.

## Étape 5 : Décoder le Morse au fil du taper

Ce qui va vous aider à apprendre, c'est de savoir lorsque vous taper la bonne lettre ou non. On peut programmer le Pi pour décoder ce que vous taper et afficher les lettres à l'écran au fur et à mesure que vous tapez. Grâce à ce système, vous pouvez prendre un message, le taper et immédiatement vérifier si le texte qui s'affiche est correct. Si le texte affiché est faux, il y a alors des chances que vous ayez tapé une phrase Morse fausse. C'est en forgeant qu'on devient forgeron !

Voici un exemple [video](https://www.youtube.com/watch?v=P7BT7aI1BPg).

Pour programmer ceci, vous devez avoir en tête les règles du code Morse International :

- L'unité temporelle est le point
- Un trait à une durée de trois points
- Chaque point ou trait est séparé d'un silence (Généralement d'une durée d'un point)
- Les lettres dans un mots sont séparées d'un silence un peu plus long (généralement 3 points)
- Les mots sont séparés d'un silence encore plus long (généralement 7 points)

Ainsi, pour commencer, nous avons besoin de déterminer la différence entre un point et un trait. C'est possible en mesurant combien de temps la clé est pressée pour nous donner la longueur de la note. Ensuite, il faut déterminer la différence entre les points et traits qui constituent un mot, et ceux appartenant à un autre. Pour ce faire, on peut mesurer le temps durant lequel la clé est relâchée, donc le silence entre les notes. La même mesure de temps permettra de différencier les lettres constituant un mot et séparer les mots.

### Distinguer les points et les traits

Tout d'abord, programmons le Pi pour différencier les points et les traits.

Le but est de mesurer le temps durant lequel la clé est pressée. De manière générale, un point dure 0,15 secondes ou moins, et tout ce qui est plus long est un trait. Vous pouvez librement utiliser une valeur différente, mais je recommande 0,15. La façon de mesurer le temps consiste à enregistrer l'heure précise à un instant, attendre que quelque chose survienne, puis soustraire à l'heure actuelle l'heure enregistrée auparavant.

Jetez un œil au code suivant : observez l'utilisation des variables `key_down_time` et `key_down_length`.

```python
def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)
	
def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_down_length = time.time() - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    
    if key_down_length > 0.15:
        print DASH
    else:
        print DOT
```

Entrez la comande suivante pour éditer notre programme précédent :

`nano morse-code.py`

Allez à la fin du fichier, et ajoutez les lignes ci-dessus. Si nécessaire, modifiez les pour les adapter à une configuration pull down. Lorsque vous avez fini d'éditer, appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer, suivi de `Ctrl + X` pour quitter. Vous pouvez maintenant tester votre code. N'oubliez pas d'utiliser la commande `sudo`.

`sudo ./morse-code.py`

Utilisez la clé télégraphique pour faire quelques notes longues et courtes. Vous devriez voir apparaître des points et des tirets au moment où vous relâchez la clé. La sortie devrait ressembler à quelque chose comme ceci :

```
.
.
.
-
-
.
.
.
```

Appuez sur `Ctrl + C` pour quitter.

### Transcription en texte

Maintenant, il nous faut un moyen de convertir les points et traits en lettres et mots. C'est en fait un peu plus compliqué que ce qu'il n'y paraît. Il faut déjà savoir lorsque l'utilisateur a fini une lettre ou un mot. Le comportement serait alors :

- Lorsqu'il fini une lettre, afficher une *lettre*
- Lorsqu'il a fini un mot, afficher un *espace*

Je vais pour faciliter la tâche vous fournir un peu de code. Ce code vous permettra de saisir une phrase de points et traits et chercher les lettres correspondantes. Entrez la commande suivante pour télécharger ce code:

`wget https://raw.githubusercontent.com/raspberrypilearning/morse-code/master/morse_lookup.py --no-check-certificate`

Maintenant, jetons-y un coup d'œil rapide. Entrez la commande suivante pour éditer le fichier.

`nano morse_lookup.py`

La variable `morse_code_lookup` est un objet Python, un *dictionnaire* . Un dictionnaire fonctionne avec des clés et des valeurs. À chaque clé correspond une valeur. Vous pourriez créer un dictionnaire pour traduire par exemple de l'anglais au français. La clé serait *Hello* et la valeur *Bonjour*. Regardez le code suivant comme exemple :

```python
english_to_french = {
    "Hello": "Bonjour",
    "Yes": "Oui",
    "No": "Non"
    }
    
print english_to_french["Hello"]
```

La sortie du code ci-dessus serait : `Bonjour`.

Nous allons utiliser cette technique pour traduire une suite de points et traits en suite de lettres correspondantes. Par exemple, `-.-.` est la lettre `C`. La fonction `try_decode` à la fin du fichier peut être utilisée pour vérifier qu'une suite de points-traits est valide et, dans ce cas, la traduire en lettres.

Appuyez sur `Ctrl + X` pour quitter l'édition sans enregistrer.

### Le Multithreading

Pour continuer, je dois vous présenter un nouveau concept de programmation appelé [Multithreading](http://fr.wikipedia.org/wiki/Multithreading). Un *thread* est un programme qui ne possède qu'une suite d'instructions qui sont exécutée par l'ordinateur à n'importe quel moment. Dans la plupart des programmes simples, il n'y a qu'un thread, qui est le principal (*main*). Mais il est possible d'avoir plusieurs threads actif au même moment, c'est comme demander au programme de se tapoter le crâne et de se frotter le ventre, en même temps.

Comme notre thread principal est continuellement maintenu en attente par les fonctions `wait_for_keydown` et `wait_for_keyup`, on a besoin d'un autre thread qui peut à n'importe quel moment effectuer le travail de décoder ce que l'utilisateur tape.

Le principe général ici est de modifier le *thread* principal pour qu'il stocke chaque point et trait dans une liste tampon (un *buffer*). Le *thread* décodeur surveillera indépendamment du thread principal le contenu de la liste, en faisant attention à la durée des silences. Si c'est un petit silence, alors c'est que c'était une lettre, et il utilisera alors la fonction `try_decode` pour vérifier si le contenu du tampon correspond bien à une lettre, et il vide le tampon, pour être prêt à accueillir le prochain mot. Si le silence est long, alors c'est un mot, et il affiche alors un espace.

### Ajout du code

Retournons donc éditer notre programme. Entrez la commande suivante :

`nano morse-code.py`

Premièrement, nous devons ajouter deux variables. `key_up_time` permet d'enregistrer le moment où la clé a été relâchée afin de mesurer le silence qui suit. L'autre variable s'appelle `buffer` : C'est une liste qui va temporairement contenir les points et traits avant que le mot soit complet.

```python
key_up_time = 0
buffer = []
```
Ajoutez ces variables à votre code comme ci-dessous. Il y a aussi deux lignes supplémentaires à ajouter à la boucle `while` principale : une ligne qui initialise `key_up_time`, ainsi qu'une autre qui ajoute ce qui est tapé à la liste `buffer`. Faites attention à bien ajouter les deux.

```python
key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_up_time = time.time() #record the time when the key was released
    key_down_length = time.time() - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```

Vérifiez que votre code est bien identique au code ci-dessus. Lorsque vous avez fini, appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer. Nous n'avons pas fini l'édition, ne lancez pas le code maintenant. Il faut encore ajouter le code du nouveau *thread*.

D'abord, il faut importer quelques nouvelles librairies. Remontez en haut du fichier et trouvez les `import`. On doit ajouter la librairie `thread` pour supporter le multithreading et `from morse_lookup import *` pour nous permettre d'accéder au code téléchargé précédemment. Le code devrait maintenant ressembler à ceci :

```python
#!/usr/bin/python
import pygame, time, RPi.GPIO as GPIO, thread
from array import array
from pygame.locals import *
from morse_lookup import *
```

Ensuite, ajoutons le code qui devra être exécuté par notre *thread* séparé. Pour ce faire, il suffit de définir une fonction, qui sera exécutée *dans* ce thread. Ajoutez cette fonction à votre code sous la fonction `wait_for_keyup` :

```python
def decoder_thread():
    global key_up_time
    global buffer
    new_word = False
    while True:
        time.sleep(.01)
        key_up_length = time.time() - key_up_time
        if len(buffer) > 0 and key_up_length >= 1.5:
            new_word = True
            bit_string = "".join(buffer)
            try_decode(bit_string)
            del buffer[:]
        elif new_word and key_up_length >= 4.5:
            new_word = False
            sys.stdout.write(" ")
            sys.stdout.flush()
```

Examinons ce code. La première chose que vous remarquerez est l'utilisation du mot-clé `global`. Il donne au thread l'accès aux variables `key_up_time` et `buffer` qui appartiennent au thread principal, de sorte qu'elles puissent être utilisée dans ce thread. Ensuite, nous avons une variable appelée `new_word`. Lorsque la fin d'un mot est détectée, on place `new_word` à `False`, pour savoir qu'il ne faut pas ajouter d'espaces en plus.
Ensuite, il y a une boucle infinie `While True`, le but principal est de surveiller en continu les silences entre les notes. Vous trouverez également une commande `sleep`, qui permet d'éviter de surcharger le CPU, puis on calcule le `key_up_length`, qui est la `key_up_time` du thread principal qui soustrait l'heure précies actuelle. À chaque itération de la boucle, soit toutes les 0,01 secondes, la valeur de `key_up_length`augmente tant que la clé est relâchée.

Ensuite, il y a une condition `if`. Ici, il y a deux conditions selon lesquelles il faut agir :

1. La première condition est lorsqu'il y a quelque chose dans le `buffer` et que le silence est suffisamment long pour signifier qu'il y a une nouvelle lettre. On définit ce temps à `1,5` secondes. Si cette situation arrive, on sait qu'un nouveau mot vient d'être entré, donc on définit `new_word` à `True`. La ligne `bit_string = "".join(buffer)` rassemble les points et les traits présents dans la liste `buffer`, et en forme une chaîne de caractères, comme `.-..`. On peut alors vérifier si ça correspond à une clé dans le dictionnaire de transcription Morse via la fonction `try_decode`. La fonction `try_decode` affiche alors le résultat. On peut alors vider le buffer, qui est donc prêt pour accueillir le prochain mot, avec la fonction `del buffer[:]`. Si jamais on ne vide pas le buffer, il grossirait continuellement, et ne correspondrait alors à aucune lettre du dictionnaire `morse_lookup.py`.

1. La seconde condition est lorsque le silence a duré jusqu'à `4,5` secondes. Souvenez vous que la règle du Morse est qu'un silence pour un nouveau mot doit être trois fois la longueur du silence d'une nouvelle lettre, ainsi : `1,5 x 3 = 4,5`. Donc on définit `new_word` à `False`, de sorte que `else if` ne soit pas exécuté, et on ajoute alors un espace.

*Note :* L'utilisation de `sys.stdout` est telle que l'on peut écrire à l'écran sans avoir à écrire une nouvelle ligne, comme la commande `print` par défaut.

Le choix de `1,5` et `4,5` secondes est principalement arbitraire, mais il sera relativement bon pour des personnes qui sont débutantes en Morse et qui iront par conséquent assez lentement. Lorsque vous gagnez de l'expérience, vous pourriez souhaiter réduire ces nombres dans le code. Ceci devrait vous permettre de taper alors plus rapidement, mais demande plus d'expérience. Je peux me débrouiller avec 0,75 et 2,25, et je suis convaincu que les ex-opérateurs télégraphes auraient des valeurs bien inférieures !

Appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer. Il y a une dernière chose que l'on faire avant d'exécuter notre code, il s'agit d'ajouter une ligne de code qui *lance* le nouveau thread. Ceci doit être fait depuis le *thread principal*, donc allez à la fin et trouvez la ligne du `print "Ready"`. Ajoutez la ligne suivante juste avant cette ligne.

`thread.start_new_thread(decoder_thread, ())`

Le **code final** devrait ressembler à ceci, n'oubliez pas de faire les adaptations nécessaires si vous utilisez une pull down au lieu d'une pull up. Vérifiez une dernière fois :

```python
#!/usr/bin/python
import pygame, time, RPi.GPIO as GPIO, thread
from array import array
from pygame.locals import *
from morse_lookup import *

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

class ToneSound(pygame.mixer.Sound):
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(pygame.mixer.get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)

def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

def decoder_thread():
    global key_up_time
    global buffer
    new_word = False
    while True:
        time.sleep(.01)
        key_up_length = time.time() - key_up_time
        if len(buffer) > 0 and key_up_length >= 1.5:
            new_word = True
            bit_string = "".join(buffer)
            try_decode(bit_string)
            del buffer[:]
        elif new_word and key_up_length >= 4.5:
            new_word = False
            sys.stdout.write(" ")
            sys.stdout.flush()

tone_obj = ToneSound(frequency = 800, volume = .5)

pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DOT = "."
DASH = "-"

key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

thread.start_new_thread(decoder_thread, ())

print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() #record the time when the key went down
    tone_obj.play(-1) #the -1 means to loop the sound
    wait_for_keyup(pin)
    key_up_time = time.time() #record the time when the key was released
    key_down_length = key_up_time - key_down_time #get the length of time it was held down for
    tone_obj.stop()
    buffer.append(DASH if key_down_length > 0.15 else DOT)
```
Lorsque vous être fin prêts, appuyez sur `Ctrl + O` puis `Entrer` pour enregistrer, suivi de `Ctrl + X` pour quitter. Vous pouvez alors tester votre code. N'oubliez pas d'utiliser la commande `sudo`.

`sudo ./morse-code.py`

Attendez le `Ready`, puis commencez. *Conseil* Je conseille de regarder l'écran et d'attendre qu'une lettre apparaisse avant que vous tapiez la suivante. Vous pouvez vous aider des deux images vues précédemment pour vous aider.

SOS est `...` `---` `...`

Bonjour est `-...` `---` `-.` `.---` `---` `..-` `.-.`

La sortie devrait ressembler à ceci :

`SOS BONJOUR `

Appuyez sur `CTRL + C` pour quitter.

Vous pouvez ignorer le message `Unhandled exception in thread`, il s'agit simplement d'un thread enfant étant terminé lorsque vous envoyez un `KeyboardInterrupt` avec le `CTRL + C`.

## Étape 6 : Jouer à un jeu de reconnaissance avec un ami

![](images/decoding.png)

Maintenant que vous avez un outil pour vérifier l'exactitude de votre tapé, vous pouvez jouer à un jeu de reconnaissance avec un ami.

L'autre personne doit :
 - Avoir une impression de l'arbre Morse
 - Du papier, crayon, gomme
 - Être capable d'écouter votre tapé
 - Ne pas pouvoir voir votre écran

Le but de ce jeu est de taper un message et de voir si l'autre personne réussi à le décoder uniquement avec ses oreilles. C'est comme cela que c'était fait durant les Guerre Mondiales. Et c'est plus compliqué qu'il n'y paraît, alors commencez lentement, avec simplement des lettres, puis des mots, puis ensuite des messages. L'autre personne doit écrire sur du papier qu'il pense qui a été tapé, lorsque le message est fini, vous pouvez alors comparer ce qu'il a écrit et ce qui est écrit à l'écran.

*Conseil : * Essayez de ne pas écrire de points et traits, mais plutôt d'écouter, et suivre l'arbre du Morse pour arriver à la lettre. Écrivez des lettres !

*Conseil : * Si le message ressemble à du charabia lorsque vous le décodez, continuez, la personne derrière l'écran peut se tromper. Le but pour vous est d'avoir exactement ce qui est écrit à l'écran, même si c'est faux !

Bonne chance !

## Pour aller plus loin avec le Code Morse

Une des choses que vous pourriez souhaiter serait d'étendre la capacité de décodage de ce projet en incluant les caractères de ponctuation, comme le STOP `.-.-.-` (Full Stop), la virgule `--..--`, le point d'interrogation `..--..`. Vous pourriez également souhaiter décoder le morse dans d'autres langues. Vous pouvez faire ceci en éditant `morse_lookup.py` et ajouter les entrées appropriées au dictionnaire.

Une référence complète pour le Morse International peut être trouvée [ici](https://www.itu.int/rec/R-REC-M.1677-1-200910-I/fr), elle est valable pour le Français, l'Anglais, l'Arabe, le Chinois et le Russe.

Il y a également des caractères spéciaux de traitement qui ont des sens conventionnés comme une fin de transmission, un caractère invitant à attendre, un séparateur pour différencier les parties d'un message. Ils auraient certainement trouvé une utilisé 100 ans auparavant durant 1914. Certain sont mentionnés dans la référence précédente, mais un document plus exhaustif sur les Extensions du Code Morse peut être trouvée [ici (en)](http://ke1g.org/media/uploads/files/MorseExtension.pdf).

Si vous êtes intéressés par l'apprentissage du Morse, je vous suggère de lire [ce document (en)](http://www.qsl.net/n1irz/finley.morse.html) à propos de la **Méthode Koch** comme entraînement au Morse. C'est une méthode testée et approuvée d'apprentissage du Morse, par l'écoute de 15 à 20 mots par minute. Il éxiste aussi un [Package Python](https://pypi.python.org/pypi/KochMorse/0.99.7) qui fournit une interface GTK2 que vous pouvez installer et utiliser.

Si vous souhaitez utiliser votre projet `morse-code.py` pour *taper* à 15 à 20 mots à la minute, vous devriez modifier les temps définis dans le code. Ils sont dans la fonction `decoder_thread` où l'on teste `key_up_length >= 1,5` et `key_up_length >= 4,5` respectivement. Ces nombres devraient être réduits. Je recommande de les réduire étapes par étapes pour s'assurer que le temps pour un nouveau mot (où l'on affiche un espace) est toujours trois fois le temps pour une nouvelle lettre (où l'on décode la lettre). Essayer 1 et 3 respectivement pour voir comment vous vous en sortez avant d'abaisser encore.

## Licence

Sauf indication contraire, tout ce qui est dans ce dépôt est soumis à la licence suivante :

![Creative Commons License](http://i.creativecommons.org/l/by-sa/4.0/88x31.png)

***Morse Code Virtual Radio*** by the [Raspberry Pi Foundation](http://raspberrypi.org) is licenced under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypilearning/morse-code
Traduction par [Mathieu Rousse](mailto:rousse.mathieu@yahoo.fr)
