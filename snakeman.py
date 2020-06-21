#Highly inspired by https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_17_Pacman.py
import pygame_functions as pgf
import random as rng
#Punkt zum fressen
class Punkt:
  def __init__(self, pos):
    self.x, self.y = pos
    self.sprite = pgf.makeSprite('img/point.png')
    pgf.moveSprite(self.sprite,self.x, self.y, centre=True)

#Snakeman Kopf mit Body Array
class Snakeman():
    def __init__(self,name,pos):
        #view
        self.name = name
        self.modus='jagd'
        self.bildNr=0 
        self.sprites = {'jagd': [pgf.makeSprite('img/snake_head.png',12),3,True],
                        'tot':   [pgf.makeSprite('img/snake_head_die.png',12),12,False]}
        self.sprite= self.sprites[self.modus][0]
        
        #position and movment
        self.x, self.y = pos #position in pixel
        self.richtung= STARTRICHTUNG #aktuelle Bewegungsrichtung
        self.rx,self.ry= RICHTUNGEN[self.richtung] #bewegung in pixel
        self.inMiddle= False #befindet sich der kopf in der mitte des feldes
        self.i = self.i=xy2i(self.x,self.y) #position im spielraster
        self.pressedKey= STARTRICHTUNG #letzter gedrückter bewegungsbefehl        
        self.body= []   #body-elements

    #snakeman bewegen
    def bewege(self):    
            if(self.rx==0 and self.ry==0): return   
            self.x += self.rx
            self.y += self.ry            
            #Ermittleren der Mittlerposition des aktuellen kachels
            self.i=xy2i(self.x,self.y)
            x2,y2=i2xy(self.i)
            self.inMiddle= self.x == x2 and self.y == y2            
            for b in range (0,len(self.body)):
                self.body[b].addToMoveList(self.richtung)
                self.body[b].bewege()

    #bewegung kalkulieren
    def bewegungsLogik(self):
        #bewegung nur wenn der Head sich in der Mitte vom Feld befindet
        if not self.inMiddle: return
        #if self.warp(): return
        self.ändereRichtung(self.pressedKey)
        if not self.richtungGültig(self.richtung):
            self.rx,self.ry=0,0

    #boddy element am ende hinzufügen
    def addBody(self):    
        if (len(self.body)==0):
            pos=(self.x-ABSTAND_BODY,self.y)
            richtung=self.richtung
            moveListe=[]
        else:
            richtung=self.body[-1].richtung
            aX,aY=self.body[-1].x, self.body[-1].y
            moveListe=self.body[-1].moveListe

            #schwanz zeigt nach rechts           
            if (richtung==0):
                pos=(aX-ABSTAND_BODY,aY)
            #schwanz zeigt nach links
            elif(richtung==1):
                pos=(aX+ABSTAND_BODY,aY)
            #schwanz zeigt nach oben
            elif(richtung==2):
                pos=(aX,aY+ABSTAND_BODY)
            #schwanz zeigt nach unten
            elif(richtung==3):
                 pos=(aX,aY-ABSTAND_BODY)

        newBody = Body("body",pos,len(self.body)+1,richtung,moveListe)
        self.body.append(newBody)   

    #warpen auf andere Spielfeldseite
    def warp(self):
        if spielraster[self.i] not in (5,6): return False
        self.i = self.i + 27   if spielraster[self.i] == 5 else self.i - 27  
        self.x, self.y = i2xy(self.i)
        return True    

    #prüfen ob die Richtung gültig ist (keine Wand)
    def richtungGültig(self, richtung):
        rx, ry = RICHTUNGEN[richtung]
        i = self.i + rx + (ry * SPALTEN)
        return spielraster[i] != 9

    #bewegungsrichtung updaten
    def ändereRichtung(self,richtung):
        #180 Grad-Wende nicht möglich        
        if((self.richtung==0 and richtung==1) or (self.richtung==1 and richtung ==0) or (self.richtung==2 and richtung==3) or (self.richtung==3 and richtung==2)): return False
        if self.richtungGültig(richtung):       
           self.richtung=richtung
           self.rx,self.ry= RICHTUNGEN[richtung]
           return True

    #gesammte Snake anzeigen
    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)
        for b in range (0,len(self.body)):
            self.body[b].anzeigen()

    #animationen des kopfes
    def animiere(self):
        sprite, animationsbilder,richtungsabhängig=self.sprites[self.modus]
        self.bildNr = (self.bildNr+1)%animationsbilder
        if richtungsabhängig:
            self.bildNr+= animationsbilder*self.richtung
        pgf.changeSpriteImage(sprite,self.bildNr)
        
    #prüfen ob Kopf auf den selben Feld ist wie ein Punkt und dann fressen und größer werden    
    def punktFressen(self,punkt):
        if spielraster[self.i] != 1: return punkt
        pgf.killSprite(punkt.sprite)
        spielraster[self.i] = 0
        self.addBody()
        return None
    
    #modus für sprite ändern
    def updateModus(self,modus):
        self.modus=modus
        pgf.hideSprite(self.sprite)
        self.sprite=self.sprites[self.modus][0]

    #prüft auf kollision mit Bodyelementen 
    def kollision(self):
        for body in self.body:
            if(body.i==self.i): 
                self.updateModus('tot')
#Bodyelement 
class Body ():
    def __init__(self,name,pos,abstand, myStartrichtung, moveListe):
        self.x, self.y = pos #position in Pixel
        self.sprite=pgf.makeSprite('img/snake_body.png') #sprite vom body
        self.moveListe=moveListe.copy() #enthält alle Bewegungen des Kopfes zum nachmachen
        self.richtung=0 #akutelle Bewegungsrichtung
        self.rx,self.ry= 0,0 #Bewegung in Pixel
        self.i= self.i=xy2i(self.x,self.y) # position im spielraster
        for i in range (0,ABSTAND_BODY): #der Body muss sich ABSTAND_BODY mal in die Startichtung bewegen um den Kopf exakt nachzulaufen
            self.moveListe.insert(0,myStartrichtung)  

    #Body bewegen
    def bewege(self):
        #if self.warp(): return
        self.richtung=self.moveListe.pop(0)
        self.rx,self.ry=RICHTUNGEN[self.richtung]
        self.x += self.rx
        self.y += self.ry
        self.i=xy2i(self.x,self.y)
    
    #Body anzeigen
    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)

    #bewegunge zur Moveliste hinzufügen
    def addToMoveList(self,richtung):
        self.moveListe.append(richtung)

    #warpen auf andere Spielfeldseite (buggy)
    def warp(self):
        if spielraster[self.i] not in (5,6): return False
    
        #Porter left to right
        if (spielraster[self.i] == 5 and self.richtung==1):
            #27 Felder liegen zwischen den beiden Warpgates
            self.i = self.i + 27 
            self.x, self.y = i2xy(self.i)
            return True  
        #porter right to left
        elif (spielraster[self.i] == 6 and self.richtung==0):
            self.i = self.i - 27 
            self.x, self.y = i2xy(self.i)
            return True  
        return False


# umrechenen von Spielfeld Index auf Pixel Position 
def i2xy(i):
  sp, ze = i % SPALTEN, i // SPALTEN
  return sp * RASTER + RASTER // 2, ze * RASTER + RASTER // 2

# umrechnen von Pixel position auf Spielfeld Index
def xy2i(x,y):
  sp, ze = (x - RASTER // 2) // RASTER, (y - RASTER // 2) // RASTER
  return ze * SPALTEN + sp

#punkt auf feld verteilen
def punktSetzen():
  global time_since_last_point
  while True: 
    placeOn = rng.randrange(len(spielraster))
    if spielraster[placeOn] == 0:
        punkt = Punkt(i2xy(placeOn))
        spielraster[placeOn]=1
        pgf.showSprite(punkt.sprite) 
        time_since_last_point=pgf.clock()
        return punkt

#restart game
def restart():
    global snakeman
    global SCORE
    global NEXT_ANIMATION
    global TICK_RATE
    global punkt
    global spielraster

    #kill sprites
    pgf.killSprite(snakeman.sprite)
    for body in snakeman.body:
        pgf.killSprite(body.sprite)
    pgf.killSprite(punkt.sprite)
    
    #setup start parameter
    spielraster=SPIELRASTER_START.copy()
    snakeman = Snakeman("Snake-Man",(SNAKEMAN_START_X,SNAKEMAN_START_Y))
    NEXT_ANIMATION=pgf.clock()+ANIMATION_REFRESH_RATE
    SCORE=-100
    TICK_RATE=START_RATE-ADD_TICK_RATE
    snakeman.addBody()
    snakeman.addBody()
    punkt= None


#9 = Wall, 0= Empty_space, 1= Point, 5/6 = Teleport 7= Gate (to save ghosts)
SPIELRASTER_START = [ 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
                9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 7, 7, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 3, 3, 3, 3, 3, 3, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                5, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 3, 3, 3, 3, 3, 3, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 6,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 3, 3, 3, 3, 3, 3, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 0, 9,
                9, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 9,
                9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9,
                9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 0, 9, 9, 9,
                9, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9,
                9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9,
                9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9,
                9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9,
                9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]




#konstante paramter gegeben durch grafik und game größe
BREITE, HÖHE = 672, 744
RASTER = 24
ABSTAND_BODY=50
SPALTEN, ZEILEN = BREITE // RASTER, HÖHE // RASTER

#konfigurations parameter
RICHTUNGEN = {0:(1,0),1:(-1,0),2:(0,-1),3:(0,1)}
STARTRICHTUNG=0
SNAKEMAN_START_X=336
SNAKEMAN_START_Y=564

#ANIMATION time
ANIMATION_REFRESH_RATE=100
NEXT_ANIMATION=pgf.clock()+ANIMATION_REFRESH_RATE

#SCORE 
MIN_SCORE_POINT=50
SCORE_FOR_POINT=100
SCORE=-100
time_since_last_point=pgf.clock()

#TICK RATE
ADD_TICK_RATE=10
START_RATE=120
TICK_RATE=START_RATE-ADD_TICK_RATE

#setup Screen
pgf.screenSize(BREITE, HÖHE)
pgf.setBackgroundImage('./img/level.png')
pgf.setAutoUpdate(False)

#setup start
snakeman = Snakeman("Snake-Man",(SNAKEMAN_START_X,SNAKEMAN_START_Y))
snakeman.addBody()
snakeman.addBody()
punkt= None
spielraster=SPIELRASTER_START.copy()


#gameloop
while True:    
    #geschwindigkeit setzten
    pgf.tick(TICK_RATE)

    #controlls
    if pgf.keyPressed('right'): snakeman.pressedKey=0
    if pgf.keyPressed('left'): snakeman.pressedKey=1
    if pgf.keyPressed('up'): snakeman.pressedKey=2
    if pgf.keyPressed('down'): snakeman.pressedKey=3
    if pgf.keyPressed('R'): restart()
    if pgf.keyPressed('ESC'): break

    #Neue Punkte Setzten
    if punkt==None:
        malus= min(((pgf.clock()-time_since_last_point)//1000),MIN_SCORE_POINT)
        SCORE+=SCORE_FOR_POINT-malus
        punkt=punktSetzen()       
        print(SCORE)
        TICK_RATE+=ADD_TICK_RATE

    #ablauf logik
    if snakeman.modus!='tot':
        snakeman.kollision()
        punkt=snakeman.punktFressen(punkt)
        snakeman.bewegungsLogik()
        snakeman.bewege()

    #neue Animation
    if pgf.clock()>NEXT_ANIMATION: snakeman.animiere()

    #update View
    snakeman.anzeigen()
    pgf.updateDisplay()

    #reset Animationstimer
    if pgf.clock()>NEXT_ANIMATION:
        NEXT_ANIMATION=pgf.clock()+ANIMATION_REFRESH_RATE
  
