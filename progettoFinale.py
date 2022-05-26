import pygame
import serial, time,queue
import random
import threading, queue
q = queue.Queue()

pygame.init()

class Read_Microbit(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._running = True
      
    def terminate(self):
        self._running = False
        
    def run(self):
        #serial config
        port = "COM8"
        s = serial.Serial(port)
        s.baudrate = 115200
        while self._running:
            data = s.readline().decode() 
            acc = [float(x) for x in data[1:-3].split(",")]
            q.put(acc)
            print(acc)
            time.sleep(0.01)
        
bianco = (255, 255, 255)        #IMPOSTO I COLORI PRINCIPALI CHE POTREBBERO SERVIRMI DURANTE IL GIOCO.
giallo = (255, 255, 102)
nero = (0, 0, 0)
rosso = (255, 0, 0)
verde = (0, 255, 0)
blu = (50, 153, 213)
bg = pygame.image.load("./Sfondo.png")  
lostIMage = pygame.image.load("./Sfondo.jpg") 

width = 1000
height = 600
                               #CARICO L'IMMAGINE DI SFONDO E SUCCESSIVAMENTE LA MODIFICO IN BASE ALLE DIMENSIONI DELLA SCHERMATA DI GIOCO.                                           
bg = pygame.transform.scale(bg, (width,height))  
lostIMage = pygame.transform.scale(lostIMage, (width,height)) 
 
dis = pygame.display.set_mode((width, height))      #IMPOSTO IL DISPLAY DI PYGAME CON LE DIMENSIONI DELLO SCHERMO
pygame.display.set_caption('Snake')
 
clock = pygame.time.Clock()
 
pezzoDiSerpente = 25        #IMPOSTO LA DIMENSIONE DEL BLOCCO DI SERPENTE E LA SUA VELOCITA'
VelocitaSerpente = 2
 
font_style = pygame.font.SysFont("omicsansms", 33)          #TIPOLOGIE DI CARATERI TROVATI PER LA SELEZIONE DEL FORMATO TESTO.
score_font = pygame.font.SysFont("comicsansms", 28)
 
 
def Punteggio(score):                                                           #FUNZIONE PER IL PUNTEGGIO DEL GIOCO
    value = score_font.render("Il tuo Punteggio: " + str(score), True, nero)
    dis.blit(value, [0, 0])
 
 
 
def Serpente(pezzoDiSerpente, listaSerpente):  #funzione per disegnare il serpente
    for x in listaSerpente:
        pygame.draw.rect(dis, nero, [x[0], x[1], pezzoDiSerpente, pezzoDiSerpente])

        #VelocitaSerpente  = VelocitaSerpente + 1
 
 
def message(msg, color):                        # FUNZIONE PER STAMPARE IL MESSAGGIO DI FINE GIOCO CON LE VARIE OPZIONI
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, height / 3])
 
 
def game():                     #funzione principale che permette il loop del gioco
    game_over = False
    game_close = False
 
    x1 = width / 2
    y1 = height / 2
 
    x1_change = 0
    y1_change = 0
 
    listaSerpente = []
    LunghezzaSerpente = 1
 
    foodx = round(random.randrange(100, width - pezzoDiSerpente) / 25.0) * 25.0
    foody = round(random.randrange(40, height - pezzoDiSerpente) / 25.0) * 25.0
 
    while not game_over:
 
        while game_close == True:
            dis.blit(bg,(0,0))
            message("Hai perso!  Premi ESC per uscire oppure SPAZIO per rigiocare", nero)
            Punteggio(LunghezzaSerpente - 1)
            pygame.display.update()
 
            for event in pygame.event.get():        ## "menu di fine gioco"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:     ##CODICE PER USCIRE
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE: #PER RIGIOCARE MI BARTA RICHIAMARE LA FUNZIONE PRINCIPALE CIOE' GAME
                        game()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -pezzoDiSerpente
                    y1_change = 0                  #codice per il movimento con i tasti
                elif event.key == pygame.K_RIGHT:
                    x1_change = pezzoDiSerpente
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -pezzoDiSerpente
                    x1_change = 0
                elif event.key == pygame.K_DOWN:    
                    y1_change = pezzoDiSerpente
                    x1_change = 0
        
        """acc = q.get()
        print(acc)                              #CODICE PER LO SPOSTAMENTO CON IL MICROBIT
        q.task_done()
        
        if acc != None:
            if acc[0] < 0:   #sinistra
                x1_change = -pezzoDiSerpente
                y1_change=0
            if acc[0] > 0: #destra
                x1_change = pezzoDiSerpente
                y1_change=0
            if acc[1] < 0:
                x1_change = 0 #su
                y1_change = -pezzoDiSerpente
            if acc[1] > 0:
                x1_change = 0 #giu
                y1_change = pezzoDiSerpente"""
 
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:    #CODICE PER FARE IN MODO CHE IL SERPENTE NON ESCA DAI BORDI
            game_close = True
        x1 += x1_change
        y1 += y1_change
        
        dis.blit(bg,(0,0))
        
        pygame.draw.rect(dis, rosso, [foodx, foody, pezzoDiSerpente, pezzoDiSerpente])
        inizioSerpente = []
        inizioSerpente.append(x1)
        inizioSerpente.append(y1)
        listaSerpente.append(inizioSerpente)
        if len(listaSerpente) > LunghezzaSerpente:
            del listaSerpente[0]
 
        for x in listaSerpente[:-1]:
            if x == inizioSerpente:
                game_close = True
 
        Serpente(pezzoDiSerpente, listaSerpente)
        Punteggio(LunghezzaSerpente - 1)
 
        pygame.display.update() #SERVE PER CARICARE SULLO SCHERMO LE MODIFICHE EFFETTUATE
 
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - pezzoDiSerpente) / 25.0) * 25.0   ## genera il cibo mangiabile sul campo di gioco
            foody = round(random.randrange(0, height - pezzoDiSerpente) / 25.0) * 25.0
            LunghezzaSerpente += 1
        
        clock.tick(VelocitaSerpente)
 
    pygame.quit()
    quit()
 
rm = Read_Microbit()    #CHIAMO LA FUNZIONE DEL THREAD 
rm.start()
game()