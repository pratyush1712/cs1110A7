"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Pratyush Sudhakar (ps2245) and Yuvan Chugh (yc698)
# December 9, 2021
"""
from consts import *
from game2d import *
import random
from kivy.graphics import *
from kivy.graphics.instructions import *
from introcs.geom import Point2, Matrix

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREAT A NEW SHIP
    def __init__(self, posX, posY):
        super().__init__(x=posX, y=posY, width=SHIP_WIDTH,\
            height=SHIP_HEIGHT,source=SHIP_BLOW_UP, format=(2,4))


    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move(self, right = True):
        """
        moves the ship based on the direction

        Parameter right: direction of the movement of ship
        Precondition: right is a boolean value
        """
        if right:
            self.x+=SHIP_MOVEMENT
        else:
            self.x-=SHIP_MOVEMENT
    

    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this ship
        
        This method returns False if bolt was not fired by the player.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if bolt.isPlayerBolt():
            return False
        botRghtX = bolt.x + bolt.width/2
        botRghtY = bolt.y - bolt.height/2
        botLeftX = bolt.x - bolt.width/2
        botLeftY = bolt.y - bolt.height/2
        return self.contains((botRghtX,botRghtY)) or self.contains((botLeftX,botLeftY))


    # COROUTINE METHOD TO ANIMATE THE SHIP
    def animate(self):
        """
        Animates a  vertical up or down of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up' or 'down'.
        """
        time = 0
        animating = True
        while animating:
            dt = (yield)
            time +=dt
            frames = time/DEATH_SPEED
            amt = frames* self.count
            self.frame = round(amt)
            if time>DEATH_SPEED:
                animating = False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    # IF YOU ADD ATTRIBUTES, LIST THEM BELOW
        
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREAT AN ALIEN
    def __init__(self, **keywords):
        super().__init__(**keywords)
    

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien
        
        This method returns False if bolt was not fired by the player.
        
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if not bolt.isPlayerBolt():
            return False
        topRghtX = bolt.x + bolt.width/2
        topRghtY = bolt.y + bolt.height/2
        topLeftX = bolt.x - bolt.width/2
        topLeftY = bolt.y - bolt.height/2
        return self.contains((topRghtX,topRghtY)) or self.contains((topLeftX,topLeftY))

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO SE THE VELOCITY
    def __init__(self, up, **keywords):
        super().__init__(**keywords)
        if up:
            self.velocity = BOLT_SPEED
        else:
            self.velocity = -BOLT_SPEED


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns True if the bolt was shot by the ship, false otherwise.
        """
        if self.velocity > 0:
            return True


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
