#Highly inspired by https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_17_Pacman.py
import pygame_functions as pgf


def i2xy(i):
  sp, ze = i % spalten, i // spalten
  return sp * raster + raster // 2, ze * raster + raster // 2

def xy2i(x,y):
  sp, ze = (x - raster // 2) // raster, (y - raster // 2) // raster
  return ze * spalten + sp

  
class Snakeman():
    def __init__(self,name,pos):
        #view
        self.name = name
        self.modus='jagd'
        self.bildNr=0
        self.sprites = {'jagd': [pgf.makeSprite('img/snake_head.png',12),3,True]}
        self.sprite= self.sprites[self.modus][0]

        #position and movment
        self.x, self.y = pos
        self.richtung= STARTRICHTUNG
        self.rx,self.ry= richtungen[self.richtung]
        self.inMiddle= False
        self.i = self.i=xy2i(self.x,self.y)
        
        #body-elements
        self.body= []  

    def bewege(self):         
        if self.richtungGültig(self.richtung):
            self.x += self.rx
            self.y += self.ry
            
            #Ermittleren der Mittlerposition des aktuellen kachels
            self.i=xy2i(self.x,self.y)
            x2,y2=i2xy(self.i)
            self.inMiddle= self.x == x2 and self.y == y2
            
            for b in range (0,len(self.body)):
                self.body[b].addToMoveList(self.richtung)
                self.body[b].bewege()

    def addBody(self):
        if (len(self.body)>10): return
        if (len(self.body)==0):
            pos=(self.x-ABSTAND_BODY,self.y)
            richtung=STARTRICHTUNG
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
                pos=(aX,aY-ABSTAND_BODY)
            #schwanz zeigt nach unten
            elif(richtung==3):
                 pos=(aX,aY+ABSTAND_BODY)

        newBody = Body("body",pos,len(self.body)+1,richtung,moveListe)
        self.body.append(newBody)

    def richtungGültig(self, richtung):
        rx, ry = richtungen[richtung]
        i = self.i + rx + (ry * spalten)
        return spielraster[i] != 9


    def ändereRichtung(self,richtung):       
        if not self.inMiddle: return     
        #180 Grad-Wende nicht möglich        
        if((self.richtung==0 and richtung==1) or (self.richtung==1 and richtung ==0) or (self.richtung==2 and richtung==3) or (self.richtung==3 and richtung==2)): return
        if self.richtungGültig(richtung):       
           self.richtung=richtung
           self.rx,self.ry= richtungen[richtung]



    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)
        for b in range (0,len(self.body)):
            self.body[b].anzeigen()

    def animiere(self):
        sprite, animationsbilder,ricthungsabhängig=self.sprites[self.modus]
        self.bildNr = (self.bildNr+1)%animationsbilder
        if ricthungsabhängig:
            self.bildNr+= animationsbilder*self.richtung
        pgf.changeSpriteImage(sprite,self.bildNr)
        


class Body ():
    def __init__(self,name,pos,abstand, myStartrichtung, moveListe):
        self.x, self.y = pos
        self.sprite=pgf.makeSprite('img/snake_body.png')
        self.moveListe=moveListe.copy()
        self.richtung=0
        self.rx,self.ry= 0,0
        for i in range (0,ABSTAND_BODY):
            self.moveListe.insert(0,myStartrichtung)  

    def bewege(self):
        self.richtung=self.moveListe.pop(0)
        self.rx,self.ry=richtungen[self.richtung]
        self.x += self.rx
        self.y += self.ry
    
    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)

    def addToMoveList(self,richtung):
        self.moveListe.append(richtung)
        
    
#Nur der Kopf

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
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
                5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
                9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9,
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
ABSTAND_BODY=40

richtungen = {0:(1,0),1:(-1,0),2:(0,-1),3:(0,1)}
STARTRICHTUNG=0
spalten, zeilen = breite // raster, höhe // raster
pgf.screenSize(breite, höhe)
pgf.setBackgroundImage('./img/level.png')
pgf.setAutoUpdate(False)
SNAKEMAN_START_X=336
SNAKEMAN_START_Y=564
ANIMATION_REFRESH_RATE=100
TICK_RATE=120

snakeman = Snakeman("Snake-Man",(SNAKEMAN_START_X,SNAKEMAN_START_Y))
figuren=[snakeman]

nextAnimation=pgf.clock()+ANIMATION_REFRESH_RATE

snakeman.addBody()
snakeman.addBody()
run=True
while True:
    pgf.tick(TICK_RATE)
    if pgf.keyPressed('right'): snakeman.ändereRichtung(0)
    if pgf.keyPressed('left'): snakeman.ändereRichtung(1)
    if pgf.keyPressed('up'): snakeman.ändereRichtung(2)
    if pgf.keyPressed('down'): snakeman.ändereRichtung(3)
    if pgf.keyPressed('P'): run = not run
    for figur in figuren:
        if run:
            figur.bewege()
        if pgf.clock()>nextAnimation:
            figur.animiere()
        figur.anzeigen()
    pgf.updateDisplay()
    if pgf.clock()>nextAnimation:
        snakeman.addBody()
        nextAnimation=pgf.clock()+ANIMATION_REFRESH_RATE
    if pgf.keyPressed('ESC'):
        break
