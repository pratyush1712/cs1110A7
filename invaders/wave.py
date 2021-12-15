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

# Pratyush Sudhakar (ps2245) and Yuvan Chugh (yc698)
# December 9, 2021
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
    # Invariant: _aliens is a rectangular 2d list containing Alien objects 
    # or None
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
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    #
    # Attribute _boltRate: the number of ALIEN STEPS (not frames) between bolts
    # Invariant: _boltRate is an integer greater than 0
    #
    # Attribute _step: number of steps taken by aliens
    # Invariant: _step is an integer greater than or equal to zero
    #
    # Attribute _shipDies: A boolean to determine if alien died by collision
    # Invariant: _shipDies is True (ship died), False (ship hasn't died yet)
    #
    # Attribute _playerWins: A boolean to determine if the player won 
    # by killing all aliens
    # Invariant: _playerWins is True (player won/ all aliens killed) or False
    #
    # Attribute _playerlose: music to play when a ship dies
    # Invariant: _playerlose is an object of sound class or None
    #
    # Attribute _alienblast: music to play when an alien bursts
    # Invariant: _alienblast is an object of sound class or None
    #
    # Attribute _shipshoot: music to play when the ship shoots
    # Invariant: _shipshoot is an object of Sound class or None
    #
    # Attribute _killsReq: number of alien kills required to increase 
    # point per alien
    # Invariant: _killsReq is an integer greater than zero
    #
    # Attribute _aPIAK: the number of points by which value of one alien kill 
    # is increased
    # Invariant: _aPIAK is an integer greater than 0
    #
    # Attribute _kills: number of aliens killed so far
    # Invariant: _kills is an integer greater than or equal to zero
    #
    # Attribute _score: score of the player
    # Invariant: _score is an integer (can be negative)
    #
    # Attribute _mov: the direction of movement of aliens
    # Invariant: _mov is either 1 (aliens move right) or -1 (aliens move left)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPlayerWin(self):
        """
        Returns self._playerWins
        """
        return self._playerWins


    def getShipDies(self):
        """
        Returns self._shipDies
        """
        return self._shipDies


    def setShip(self, ship):
        """
        Sets self._ship to ship

        Parameter ship: A ship object
        Precondition: ship is a an instance of GObject
        """
        self._ship = ship


    def getScore(self):
        """
        Returns self._score
        """
        return self._score


    def getPlayerlose(self):
        return self._playerlose


    def setShipDies(self, value):
        """
        Sets self._shipDies to value

        Parameter value: A boolean value representing 
        whether ship is dead or not
        Precondition: value is a boolean
        """
        self._shipDies = value


    def setPlayerWin(self, value):
        """
        Sets self._playerWins to value.

        Parameter value: A boolean value representing 
        whether player has won or not
        Precondition: value is a boolean
        """
        self._playerWins = value


    # INITIALIZER (standard form) TO CREAT SHIP AND ALIENS
    def __init__(self, playerlose, alienblast, shipshoot):
        # required
        self._ship = Ship(GAME_WIDTH/2,SHIP_BOTTOM+SHIP_HEIGHT/2)
        self._aliens = self._createAliens()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
            linewidth=2, linecolor='blue')
        self._lives = SHIP_LIVES
        self._time = 0
        # animation
        self._animator = None
        # alien firings
        self._boltRate = random.randint(1, BOLT_RATE)
        self._step=0
        # win-lose
        self._shipDies = False
        self._playerWins = False
        # sounds
        self._playerlose = playerlose
        self._alienblast = alienblast
        self._shipshoot = shipshoot
        # player's score
        self._killsReq = ALIEN_ROWS*ALIENS_IN_ROW//5
        self._aPIAK = 2
        self._kills = 0
        self._score = 0
        self._alienpoints = 30
        # helper
        self._mov = 1


    # UPDAT METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Animates a single wave in the game.

        Parameter dt: The time in seconds since last Invader's update
        Precondition: dt is a number (int or float)

        Parameter input: user input, used to control the ship or shoot bolts
        Invariant: input is an instance of GInput (inherited from GameApp)
        """
        if self._animator is None:
            self._shipMove(input,dt)
            self._aliensMoveShoot(dt)
            self._fireBolt(input)
            self._updateBolts(dt)
            if self.aliensCount() == 0:
                self._playerWins = True
            if self.alienLine() == True:
                self._playerlose = True
        else:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
                self._ship = None
                self._shipDies = True
                self._bolts = []


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draw method to draw objects of a wave

        Parameter view: the game view, used in drawing (from Invaders)
        Precondition: view is an instance of GView (inherited from GameApp)
        """
        # IMPLEMENT ME
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        for bolt in self._bolts:
            if not (not bolt):
                bolt.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def _createAliens(self):
        """
        Creates and returns a 2-D list of aliens
        """
        aliens = []
        images = self._getImages()
        for i in range(1, ALIEN_ROWS+1):
            alien = []
            for j in range(1, ALIENS_IN_ROW+1):
                alien.append(Alien(\
                    x=(j)*ALIEN_H_SEP+(j-1)*(ALIEN_WIDTH)+ALIEN_WIDTH/2,\
                    y=GAME_HEIGHT - ALIEN_CEILING - \
                        (ALIEN_ROWS-i)*\
                    (ALIEN_HEIGHT + ALIEN_V_SEP) - ALIEN_HEIGHT/2, \
                        width = ALIEN_WIDTH, \
                        height = ALIEN_HEIGHT, source= images[i]))
            aliens.append(alien)
        return aliens


    def _getImages(self):
        """
        Determines the images each row of alien would have, 
        and then returns a dictionary
        whose keys are aliens rows (bottom-to-top) and values are images
        """
        images = {}
        image = ALIEN_IMAGES[0]
        for row in range(1, ALIEN_ROWS+1,2):
            images[row] = ALIEN_IMAGES[ALIEN_IMAGES.index(image)]
            images[row+1] = ALIEN_IMAGES[ALIEN_IMAGES.index(image)]
            if ALIEN_IMAGES.index(image) != len(ALIEN_IMAGES)-1:
                image = ALIEN_IMAGES[ALIEN_IMAGES.index(image)+1]
            else:
                image = ALIEN_IMAGES[0]
        if len(images) > ALIEN_ROWS:
            del images[len(images)]
        return images


    def alienLine(self):
        """
        Determines if any alien touched the Defence line.

        Return True if alien reached the Defence line, false otherwise.
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    if self._aliens[row][col].y - ALIEN_WIDTH/2 <= DEFENSE_LINE:
                        return True
        return False


    def _null(self, col):
        """
        Takes column index as a parameter and return whether
        the column contains aliens or all the aliens in that 
        column are dead (set to None)

        Parameter col: The column index in self._aliens
        Precondition: col is a valid column index (0<=col<ALIENS_IN_ROW)
        """
        for row in range(ALIEN_ROWS):
            if self._aliens[row][col] is not None:
                return False
        return True


    def _alienCollides(self, bolt):
        """
        Takes an index of a bolt that collided with an alien 
        as a parameter and updates the self._score (increases by self.),
        self._alienpoints(increase by self._aPIAK if valid), 
        and self._kills(+1) accordingly.

        It also increases alien_speed
        It also plays alienblast sound.

        Parameter bolt: index of a valid bolt that collided with an alien
        Invariant: bolt is a valid bolt index in self._bolts
        """
        self._alienblast.play()
        self._kills +=1
        if self._kills > self._killsReq:
            self._alienpoints+=self._aPIAK
        del self._bolts[bolt]
        self._score+=self._alienpoints
        global ALIEN_SPEED
        ALIEN_SPEED = ALIEN_SPEED*0.97


    def _shipCollides(self, bolt):
        """
        Takes an index of a bolt that collided with the ship as 
        a parameter and updates the self._score (decrease by SHIP_BURSTS, 
        a penalty)

        It also initalizes animation.
        It also plays playerlose sound.

        Parameter bolt: index of a valid bolt that collided with the ship
        Invariant: bolt is a valid bolt index in self._bolts
        """
        self._score-=SHIP_BURSTS
        self._animator = self._ship.animate()
        next(self._animator)
        self._playerlose.play()
        del self._bolts[bolt]
        self._bolts = []


    def _alienColision(self, bolt):
        """
        Takes a bolt as a parameter and
        checks if the bolt has collided with any alien so far.

        Returns True if a collsion occured, false otherwise.

        Parameter bolt: index of a valid bolt that collided with the ship
        Parameter: bolt is a valid bolt index in self._bolts
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] is not None:
                    if self._aliens[row][col].collides(bolt):
                        self._alienblast.play()
                        self._aliens[row][col] = None
                        return True
        return False


    def aliensCount(self):
        """
        Counts number of aliens in each row
        Returns count of aliens
        """
        count = 0
        for row in self._aliens:
            for alien in row:
                if not not alien:
                    count+=1
        return count


    def _shipMove(self, input, dt):
        """
        Moves the ship based on user's inputs

        Parameter input: user input, used to control the ship or shoot bolts
        Invariant: input is an instance of GInput (inherited from GameApp)

        Parameter dt: The time in seconds since last Invader's update
        Precondition: dt is a number (int or float)

        """
        if self._animator is None:
            if input.is_key_down('left'):
                if  self._ship is not None and self._ship.x-self._ship.width/2>0:
                    self._ship.move(False)
            elif  self._ship is not None and input.is_key_down('right'):
                if self._ship.x + self._ship.width/2 < GAME_WIDTH:
                    self._ship.move()
        else:
            try:
                self._animator.send(dt)
            except:
                self._shipDies = True
                self._animator = None
                self._ship = None
                self._bolts = []


    def _aliensMoveShoot(self, dt):
        """
        Moves the aliens based on alien's speed and direction
        Selects random alien to shoot and creates a bolt.
        Increments aliens steps and time

        Parameter dt: The time in seconds since last Invader's update
        Precondition: dt is a number (int or float)
        """
        self._time+=dt
        if self._time > ALIEN_SPEED:
            self._aliensMove()
            self._step+=1
            if self._step >= self._boltRate:
                self._shootBolts()
                self._step = 0
            self._time = 0


    def _shootBolts(self):
        """
        Allows aliens to shoot bolts at the ship
        """

        col = random.randint(0, ALIENS_IN_ROW-1)
        while self._null(col):
            col = random.randint(0, ALIENS_IN_ROW-1)
        for row in range(ALIEN_ROWS-1,-1,-1):
            if self._aliens[row][col] is not None:
                alien=self._aliens[row][col]
        self._bolts.append(Bolt(up=False, x=alien.x,y=alien.y-ALIEN_HEIGHT/2,\
        width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='red'))
        self._boltRate = random.randint(1, BOLT_RATE)


    def _aliensMove(self):
        """
        Allows alien movement to the right, to the left, upwards or downwards
        """
        max = self._extrema()[0]
        min = self._extrema()[1]
        left = min[2] - ALIEN_WIDTH/2
        right = max[2] + ALIEN_WIDTH/2
        if right <= GAME_WIDTH - ALIEN_H_SEP and self._mov == 1:
            for row in self._aliens:
                for alien in row:
                    if not (not alien):
                        alien.x+=ALIEN_H_WALK
        elif right > GAME_WIDTH - ALIEN_H_SEP and self._mov == 1:
            for row in self._aliens:
                for alien in row:
                    if not (not alien):
                        alien.y-=ALIEN_V_WALK
                        alien.x-=ALIEN_H_WALK
            self._mov=-1
        elif left >= ALIEN_H_SEP and self._mov == -1:
            for row in self._aliens:
                for alien in row:
                    if not (not alien):
                        alien.x-=ALIEN_H_WALK
        elif left < ALIEN_H_SEP and self._mov == -1:
            for row in self._aliens:
                for alien in row:
                    if not (not alien):
                        alien.y-=ALIEN_V_WALK
                        alien.x+=ALIEN_H_WALK
            self._mov = 1


    def _extrema(self):
        """
        Finds the x-coordinate of aliens at exteme positions
        Returns a list: [max, min] where
        max, min are lists of the form [row, alien, value of x]
        """
        max = [0,0,0] # row, alien, max
        for i, row in enumerate(self._aliens):
            for j, alien in enumerate(row):
                if not not alien:
                    if alien.x>max[2]:
                        max[0] = i
                        max[1] = j
                        max[2] = alien.x
        min = [0,0,2*GAME_WIDTH] # row, alien, min
        for i, row in enumerate(self._aliens):
            for j, alien in enumerate(row):
                if not not alien:
                    if alien.x<min[2]:
                        min[0] = i
                        min[1] = j
                        min[2] = alien.x
        return [max, min]


    def _fireBolt(self, input):
        """
        Allows the ship to firebolts based on user's inputs

        Parameter input: user input, used to shoot bolts in this method
        Invariant: input is an instance of GInput (inherited from GameApp)
        """

        fire=True
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                fire=False
        if input.is_key_down('spacebar') and fire:
            self._shipshoot.play()
            self._bolts.append(Bolt(up=True, x=self._ship.x,\
                y=self._ship.y+ALIEN_HEIGHT/2,width=BOLT_WIDTH,\
                    height=BOLT_HEIGHT,fillcolor='red'))


    def _updateBolts(self, dt):
        """
        Checks for collisions of aliens, ship and bolts
        Parameter dt: The time in seconds since last Invader's update
        Precondition: dt is a number (int or float)
        """
        for i, bolt in enumerate(self._bolts):
            if bolt.velocity>0:
                bolt.y+=BOLT_SPEED
                if bolt.y - bolt.width/2 >= GAME_HEIGHT:
                    del self._bolts[i]
                if self._alienColision(bolt):
                    self._alienCollides(i)
            else:
                bolt.y-=BOLT_SPEED
                if bolt.y + bolt.height/2 <= 0:
                    del self._bolts[i]
                if self._ship is not None and self._ship.collides(bolt):
                    self._shipCollides(i)

