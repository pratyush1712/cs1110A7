"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREAT SHIP AND ALIENS
    def __init__(self, playerlose, alienblast, shipshoot):
        self._lives = SHIP_LIVES
        self.boltRate = random.randint(1, BOLT_RATE)
        self.step=0
        self._time = 0
        self.playerlose = playerlose
        self.alienblast = alienblast
        self.shipshoot = shipshoot
        self.mov = 1
        self.ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM+SHIP_HEIGHT/2)
        self._aliens = self.createAliens()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=2, linecolor='blue')

    # UPDAT METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def createAliens(self):
        aliens = []
        image = ALIEN_IMAGES[0]
        images = {}
        for row in range(1, ALIEN_ROWS+1,2):
            images[row] = ALIEN_IMAGES[ALIEN_IMAGES.index(image)]
            images[row+1] = ALIEN_IMAGES[ALIEN_IMAGES.index(image)]
            if ALIEN_IMAGES.index(image) != len(ALIEN_IMAGES)-1:
                image = ALIEN_IMAGES[ALIEN_IMAGES.index(image)+1]
            else:
                image = ALIEN_IMAGES[0]
        if len(images) > ALIEN_ROWS:
            del images[len(images)]
        for i in range(1, ALIEN_ROWS+1):
            alien = []
            for j in range(1, ALIENS_IN_ROW+1):
                alien.append(Alien((j)*ALIEN_H_SEP+(j-1)*(ALIEN_WIDTH)+ALIEN_WIDTH/2,GAME_HEIGHT - ALIEN_CEILING - (ALIEN_ROWS-i)*(ALIEN_HEIGHT + ALIEN_V_SEP) - ALIEN_HEIGHT/2, images[i]))
            aliens.append(alien)
        return aliens

    def update(self, input, dt, view, sound):
        self.shipMove(input)
        self._time+=dt
        if self._time > ALIEN_SPEED:
            self.aliensMove()
            self.step+=1
            if self.step >= self.boltRate:
                self.shootBolts()
                self.step = 0
            self._time = 0
        self.fireBolt(input, sound)
        self.updateBolts()
        alienLine = self.alienBoltCol_andDline()
        if alienLine is False:
            return False
        ship = self.shipDeath()
        if ship is not None:
            return ship
        aliensLeft = self.aliensCount()
        print(aliensLeft)
        if aliensLeft == 0:
            return 0
        self.draw(view)
        # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        """
        # IMPLEMENT ME
        if self.ship is not None:
            self.ship.image.draw(view)
        self._dline.draw(view)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.image.draw(view)
        for bolt in self._bolts:
            if not (not bolt):
                bolt.image.draw(view)
    
    def shipMove(self, input):
        if input.is_key_down('left'):
            if  not (not self.ship) and self.ship.image.x - self.ship.image.width/2 > 0:
                self.ship.image.x-=SHIP_MOVEMENT
        elif  not (not self.ship) and input.is_key_down('right'):
            if self.ship.image.x + self.ship.image.width/2 < GAME_WIDTH:
                self.ship.moveRght()
    
    def aliensMove(self):
        max = [0,0,0] # row, alien, max
        for i, row in enumerate(self._aliens):
            for j, alien in enumerate(row):
                if not not alien:
                    if alien.image.x>max[2]:
                        max[0] = i
                        max[1] = j
                        max[2] = alien.image.x
        min = [0,0,2*GAME_WIDTH] # row, alien, max
        for i, row in enumerate(self._aliens):
            for j, alien in enumerate(row):
                if not not alien:
                    if alien.image.x<min[2]:
                        min[0] = i
                        min[1] = j
                        min[2] = alien.image.x
        left = min[2] - ALIEN_WIDTH/2
        right = max[2] + ALIEN_WIDTH/2
        if right <= GAME_WIDTH - ALIEN_H_WALK and self.mov == 1:
            for row in self._aliens: 
                for alien in row:
                    if not (not alien):
                        alien.image.x+=ALIEN_H_WALK
        elif right > GAME_WIDTH - ALIEN_H_WALK and self.mov == 1:
            for row in self._aliens: 
                for alien in row:
                    if not (not alien):
                        alien.image.y-=ALIEN_V_WALK
                        alien.image.x-=ALIEN_H_WALK
            self.mov=-1
        elif left >= ALIEN_H_WALK and self.mov == -1:
            for row in self._aliens: 
                for alien in row:
                    if not (not alien):
                        alien.image.x-=ALIEN_H_WALK
        elif left < ALIEN_H_WALK and self.mov == -1:
            for row in self._aliens: 
                for alien in row:
                    if not (not alien):
                        alien.image.y-=ALIEN_V_WALK
                        alien.image.x+=ALIEN_H_WALK
            self.mov = 1
        
    def shootBolts(self):
        # HELPER METHODS FOR COLLISION DETECTION
        row=random.randint(0, ALIEN_ROWS-1)
        alien=random.randint(0, ALIENS_IN_ROW-1)
        while not self._aliens[row][alien]:
            row=random.randint(0, ALIEN_ROWS-1)
            alien=random.randint(0, ALIENS_IN_ROW-1)
        alien=self._aliens[row][alien].image
        self._bolts.append(Bolt(up=False, x=alien.x,y=alien.y,\
        width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='red'))
        self.boltRate = random.randint(1, BOLT_RATE)
    
    def fireBolt(self, input, sound):
        fire=True
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                fire=False
        if input.is_key_down('spacebar') and fire:
            self.shipshoot.play()
            self._bolts.append(Bolt(up=True, x=self.ship.image.x,y=self.ship.image.y,width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='red'))
    def updateBolts(self):
        for i, bolt in enumerate(self._bolts):
            if bolt.velocity>0:
                bolt.image.y+=BOLT_SPEED
                if bolt.image.y - bolt.image.width/2 >= GAME_HEIGHT:
                    del self._bolts[i]
            else:
                bolt.image.y-=BOLT_SPEED
                if bolt.image.y + bolt.image.height/2 <= 0:
                    del self._bolts[i]
    
    def alienBoltCol_andDline(self):
        for k, bolt in enumerate(self._bolts):
            for i, row in enumerate(self._aliens):
                for j, alien in enumerate(row):
                    if not not alien:
                        if alien.collides(bolt):
                            self.alienblast.play()
                            self._aliens[i][j] = None #.image = GSprite(source='ship-strip.png',format=(2,3),width=ALIEN_WIDTH,height=ALIEN_HEIGHT)
                            del self._bolts[k]
                        if alien.image.y <= DEFENSE_LINE:
                            self._aliens[i][j] = None
                            return False
    
    def shipDeath(self):
        for k, bolt in enumerate(self._bolts):
            if not not self.ship:
                if not bolt.isPlayerBolt():
                    if self.ship.collides(bolt):
                        self._lives-=1
                        if self._lives > 0:
                            del self._bolts[k]
                            return True
                        else:
                            self.ship = None
                            del self._bolts[k]
                            return False
            
    def aliensCount(self):
        count = 0
        for row in self._aliens: 
            for alien in row:
                if not not alien:
                    count+=1
        return count
