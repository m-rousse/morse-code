#!/usr/bin/python
import pygame, time, RPi.GPIO as GPIO, thread
from array import array
from pygame.locals import *
from morse_lookup import *

# Initialisation de la librairie permettant de jouer des notes
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

# Classe permettant de jouer des notes
class ToneSound(pygame.mixer.Sound):
	# Initialisation de la classe (définition de la fréquence de la note, et de son volume)
    def __init__(self, frequency, volume):
        self.frequency = frequency
        pygame.mixer.Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

	# Fonction permettant de générer l'onde de la note à jouer
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

# fonction qui attend un appui sur la clé télégraphique
def wait_for_keydown(pin):
    while GPIO.input(pin):
        time.sleep(0.01)

# fonction qui attend un relâchement de la clé télégraphique
def wait_for_keyup(pin):
    while not GPIO.input(pin):
        time.sleep(0.01)

# Fonction indépendante, destinée à être un thread à part, qui décode le morse qui est tapé.
def decoder_thread():
    global key_up_time # Variable qui stocke le temps auquel a eu lieu le dernier relâchement de la clé
    global buffer	   # Dictionnaire où sont stockés les suites de points/traits devant être traités par la fonction
    new_word = False   # Fonction indiquant si l'on est entrain d'afficher un mot
    while True:
        time.sleep(.01)		# Pause dans le programme pour ne pas surcharger le processeur
        key_up_length = time.time() - key_up_time # Temps de silence depuis que la clé est en position haute
        if len(buffer) > 0 and key_up_length >= 1.5: # Si le buffer n'est pas vide et que la clé est relevée depuis plus d'1,5 seconde (temps entre deux lettres)
            new_word = True 			# On affiche un mot
            bit_string = "".join(buffer)# On rassemble tous les points/traits du buffer
            try_decode(bit_string)		# On décode la suite contenue dans bit_string
            del buffer[:]				# On vide le buffer
        elif new_word and key_up_length >= 4.5: # S'il y a un nouveau mot et que la clé est haute depuis plus de 4,5 secondes (temps entre deux mots)
            new_word = False 	  # Le mot est écrit, donc on attend maintenant un autre mot
            sys.stdout.write(" ") # On affiche un espace
            sys.stdout.flush()

# initialisation de la classe pour jouer des notes, à 800 Hz
tone_obj = ToneSound(frequency = 800, volume = .5)

# Définition des pins à utiliser, et dans quel mode
# ( Ici, on utilise le pin 7 en mode Pull Up pour la clé télégraphique)
pin = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Définition du caractère à afficher lorsqu'il faut afficher un point ou un trait
DOT = "."
DASH = "-"

# Initialisation à 0 des variables de fonctionnement
key_down_time = 0
key_down_length = 0
key_up_time = 0
buffer = []

# Lancement du thread de décodage
thread.start_new_thread(decoder_thread, ())

# On notifie l'utilisateur que le programme est prêt à l'emploi
print "Ready"

while True:
    wait_for_keydown(pin)
    key_down_time = time.time() # On enregistre le moment où la clé est pressée
    tone_obj.play(-1) # On joue une note
    wait_for_keyup(pin) # On attend que la clé soit relâchée
    key_up_time = time.time() # Lorsqu'elle est relâchée, on enregistre le temps
    key_down_length = key_up_time - key_down_time # On peut calculer le temps pendant lequel elle a été appuyée
    tone_obj.stop() # Et on stoppe le son
    buffer.append(DASH if key_down_length > 0.15 else DOT) # On place dans le buffer les données, pour que le thread de décodage puisse l'analyser
