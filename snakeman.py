#Highly inspired by https://github.com/Gravitar64/A-beautiful-code-in-Python/blob/master/Teil_17_Pacman.py
import pygame_functions as pgf


class Figur: 
    def __init__(self,name,pos):
        self.name = name
        self.x, self.y = pos
        self.richtung= STARTRICHTUNG
        self.rx,self.ry= richtungen[self.richtung]
        self.modus='jagd'
        self.bildNr=0
   
    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)
        
    def bewege(self):
        self.x += self.rx
        self.y += self.ry

    def ändereRichtung(self, richtung):
        self.richtung=richtung
        self.rx,self.ry= richtungen[richtung]
    
    def animiere(self):
        sprite, animationsbilder,ricthungsabhängig=self.sprites[self.modus]
        self.bildNr = (self.bildNr+1)%animationsbilder
        if ricthungsabhängig:
            self.bildNr+= animationsbilder*self.richtung
        pgf.changeSpriteImage(sprite,self.bildNr)



class Body (Figur):
    def __init__(self,name,pos,abstand, myStartrichtung, moveListe):
        Figur.__init__(self,name,pos)
        self.sprite=pgf.makeSprite('img/snake_body.png')
        self.moveListe=moveListe.copy()
        for i in range (0,ABSTAND_BODY):
            self.moveListe.insert(0,myStartrichtung)  

    def bewege(self):
        self.richtung=self.moveListe.pop(0)
        self.rx,self.ry=richtungen[self.richtung]
        self.x += self.rx
        self.y += self.ry


    def addToMoveList(self,richtung):
        self.moveListe.append(richtung)
        
    
#Nur der Kopf
class Snakeman(Figur):
    def __init__(self,name,pos):
        Figur.__init__(self,name,pos)
        self.sprites = {'jagd': [pgf.makeSprite('img/snake_head.png',12),3,True]}
        self.sprite= self.sprites[self.modus][0]
        self.body= []

    def bewege(self):   
        self.x += self.rx
        self.y += self.ry
        for b in range (0,len(self.body)):
            self.body[b].addToMoveList(self.richtung)
            self.body[b].bewege()

    def anzeigen(self):
        pgf.moveSprite(self.sprite, self.x, self.y, centre=True)
        pgf.showSprite(self.sprite)
        for b in range (0,len(self.body)):
            self.body[b].anzeigen()

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

    

    def ändereRichtung(self,richtung):
        #180 Grad-Wende nicht möglich
        if((self.richtung==0 and richtung==1) or (self.richtung==1 and richtung ==0) or (self.richtung==2 and richtung==3) or (self.richtung==3 and richtung==3)): return
        self.richtung=richtung
        self.rx,self.ry= richtungen[richtung]
        


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
#größe des rasters 
raster = 24

#abstand der einzelnen körperteile zueinander
ABSTAND_BODY=40

richtungen = {0:(1,0),1:(-1,0),2:(0,-1),3:(0,1)}
STARTRICHTUNG=0
spalten, zeilen = breite / raster, höhe / raster
pgf.screenSize(breite, höhe)
pgf.setBackgroundImage('./img/level.png')
pgf.setAutoUpdate(False)
SNAKEMAN_START_X=336
SNAKEMAN_START_Y=564
ANIMATION_REFRESH_RATE=100
snakeman = Snakeman("Snake-Man",(SNAKEMAN_START_X,SNAKEMAN_START_Y))
figuren=[snakeman]

nextAnimation=pgf.clock()+ANIMATION_REFRESH_RATE

snakeman.addBody()
snakeman.addBody()
run=True
while True:
    pgf.tick(120)
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
