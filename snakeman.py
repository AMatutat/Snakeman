#Highly inspired by https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_17_Pacman.py
import pygame_functions as pgf
import random as rng

def i2xy(i):
  sp, ze = i % spalten, i // spalten
  return sp * raster + raster // 2, ze * raster + raster // 2

def xy2i(x,y):
  sp, ze = (x - raster // 2) // raster, (y - raster // 2) // raster
  return ze * spalten + sp



class Punkt:
  def __init__(self, pos):
    self.x, self.y = pos
    self.sprite = pgf.makeSprite('img/point.png')
    pgf.moveSprite(self.sprite,self.x, self.y, centre=True)

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
        self.x, self.y = pos
        self.richtung= STARTRICHTUNG
        self.rx,self.ry= richtungen[self.richtung]
        self.inMiddle= False
        self.i = self.i=xy2i(self.x,self.y)
        self.pressedKey= STARTRICHTUNG
        #body-elements
        self.body= []  

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

    def bewegungsLogik(self):
        if not self.inMiddle: return
        if self.warp(): return
        self.ändereRichtung(self.pressedKey)
        if not self.richtungGültig(self.richtung):
            self.rx,self.ry=0,0

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

    def richtungGültig(self, richtung):
        rx, ry = richtungen[richtung]
        i = self.i + rx + (ry * spalten)
        return spielraster[i] != 9

    def warp(self):
        if spielraster[self.i] not in (5,6): return False
        self.i = self.i + 27   if spielraster[self.i] == 5 else self.i - 27  
        self.x, self.y = i2xy(self.i)

        return True    

    def ändereRichtung(self,richtung):
        #180 Grad-Wende nicht möglich        
        if((self.richtung==0 and richtung==1) or (self.richtung==1 and richtung ==0) or (self.richtung==2 and richtung==3) or (self.richtung==3 and richtung==2)): return False
        
        if self.richtungGültig(richtung):       
           self.richtung=richtung
           self.rx,self.ry= richtungen[richtung]
           return True


    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)
        for b in range (0,len(self.body)):
            self.body[b].anzeigen()

    def animiere(self):
        sprite, animationsbilder,richtungsabhängig=self.sprites[self.modus]
        self.bildNr = (self.bildNr+1)%animationsbilder
        if richtungsabhängig:
            self.bildNr+= animationsbilder*self.richtung
        pgf.changeSpriteImage(sprite,self.bildNr)
        
    def punktFressen(self,punkt):
        if spielraster[self.i] != 1: return punkt
        pgf.killSprite(punkt.sprite)
        spielraster[self.i] = 0
        self.addBody()
        return None
    
    def updateModus(self,modus):
        self.modus=modus
        pgf.hideSprite(self.sprite)
        self.sprite=self.sprites[self.modus][0]
    def kollision(self):
        for body in self.body:
            if(body.i==self.i): 
                self.updateModus('tot')
                return
class Body ():
    def __init__(self,name,pos,abstand, myStartrichtung, moveListe):
        self.x, self.y = pos
        self.sprite=pgf.makeSprite('img/snake_body.png')
        self.moveListe=moveListe.copy()
        self.richtung=0
        self.rx,self.ry= 0,0
        self.i= self.i=xy2i(self.x,self.y)
        for i in range (0,ABSTAND_BODY):
            self.moveListe.insert(0,myStartrichtung)  

    def bewege(self):
        if self.warp(): return
        self.richtung=self.moveListe.pop(0)
        self.rx,self.ry=richtungen[self.richtung]
        self.x += self.rx
        self.y += self.ry
        self.i=xy2i(self.x,self.y)
    
    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)

    def addToMoveList(self,richtung):
        self.moveListe.append(richtung)

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



def punktSetzen():
  while True: 
    placeOn = rng.randrange(len(spielraster))
    if spielraster[placeOn] == 0:
        punkt = Punkt(i2xy(placeOn))
        spielraster[placeOn]=1
        pgf.showSprite(punkt.sprite)  
        return punkt

#9 = Wall, 0= Empty_space, 1= Point, 5/6 = Teleport 7= Gate (to save ghosts)
spielraster = [ 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
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

#in pixel
breite, höhe = 672, 744
#pixelgröße eines Feldes
raster = 24
#abstand der einzelnen körperteile zueinander
ABSTAND_BODY=50

richtungen = {0:(1,0),1:(-1,0),2:(0,-1),3:(0,1)}
STARTRICHTUNG=0
spalten, zeilen = breite // raster, höhe // raster
pgf.screenSize(breite, höhe)
pgf.setBackgroundImage('./img/level.png')
pgf.setAutoUpdate(False)
SNAKEMAN_START_X=336
SNAKEMAN_START_Y=564
ANIMATION_REFRESH_RATE=100
ADD_TICK_RATE=10
TICK_RATE=120-ADD_TICK_RATE

snakeman = Snakeman("Snake-Man",(SNAKEMAN_START_X,SNAKEMAN_START_Y))
figuren=[snakeman]

nextAnimation=pgf.clock()+ANIMATION_REFRESH_RATE
SCORE_FOR_POINT=100
SCORE=-100

snakeman.addBody()
snakeman.addBody()
punkt= None

run=True
while True:    
    pgf.tick(TICK_RATE)
    if pgf.keyPressed('right'): snakeman.pressedKey=0
    if pgf.keyPressed('left'): snakeman.pressedKey=1
    if pgf.keyPressed('up'): snakeman.pressedKey=2
    if pgf.keyPressed('down'): snakeman.pressedKey=3
    if pgf.keyPressed('P'): run = not run

    if punkt==None:
        punkt=punktSetzen()
        SCORE+=SCORE_FOR_POINT
        print(SCORE)
        TICK_RATE+=ADD_TICK_RATE
    for figur in figuren:
        if run and figur.modus!='tot':
            figur.kollision()
            punkt=figur.punktFressen(punkt)
            figur.bewegungsLogik()
            figur.bewege()
        if pgf.clock()>nextAnimation:
            figur.animiere()
        figur.anzeigen()
    pgf.updateDisplay()
    if pgf.clock()>nextAnimation:
        nextAnimation=pgf.clock()+ANIMATION_REFRESH_RATE
    if pgf.keyPressed('ESC'):
        break
