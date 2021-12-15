"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Pratyush Sudhakar (ps2245) and Yuvan Chugh (yc698)
# December 9, 2021
"""
from consts import *
from game2d import *
from wave import *

# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _lastkeys: the last key pressed by the user
    # Invariant: _lastkeys
    #
    # Attribute _startkey: the key pressed to the start the game
    # Invariant: _startkey is a String that contains the key on the keyboard 
    # to be pressed to start the game
    #
    # Attribute _lives: The lives the user has till the end of the game
    # Invariant: _lives
    #
    # Attribute _game
    #
    # Attribute _win: checks if the winner has won or not
    # Invariant: _win is a Boolean value that checks if the user has won
    #
    # Attribute _alienblast: The sound when the alien blasts
    # Invariant: _alienblast is a sound object
    #
    # Attribute _shipshoot: The sound when the ship shoots 
    # Invariant: _shipshoot is a sound object
    #
    # Attribute _playerlose: The sound when the player loses
    # Invariant: _playerlose is a sound object
    #
    # Attribute _playerWin: The sound when the player wins
    # Invariant: _playerWin is a sound object
    #
    # Attribute sound: The background music
    # Invariant: sound is a sound object
    #
    # Attribute _score: Displays player score
    # Invariant: _score is a GLabel object
    #
    # Attribute _life: Displays the lives the user has left
    # Invariant: _life is a GLabel Object
    #
    # Attribute _logo: Displays the logo/title of the game
    # Invariant: _logo is a GLabel Object
    #
    # Attribute _inst: Displays the instruction to shoot bolts with the ship
    # Invariant: _inst is a GLabel Object
    #
    # Attribute _blsc: Background of the game
    # Invariant: _blsc is a GRectangle Object

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # IMPLEMENT ME
        # constants and variables
        self._lastkeys = 0
        self._state = STATE_INACTIVE
        self._startkey = 'enter'
        self._wave = None
        self._lives = SHIP_LIVES
        self._game = None
        self._win = False
        # sounds
        self._alienblast = Sound('alienblast.wav')
        self._shipshoot = Sound('shipshoot.wav')
        self._playerlose = Sound('playerlose.wav')
        self._playerWin = Sound('win.wav')
        self._sound = Sound('bkg.wav')
        # screen
        self._blsc = GRectangle(width = GAME_WIDTH, height = GAME_HEIGHT, \
            x=GAME_WIDTH/2, y=GAME_HEIGHT/2, fillcolor='light green')
        # texts
        self._score = GLabel(text = f"Player's score: 0",font_size=40,\
             left=5, bottom=5, \
            x=GAME_WIDTH - 200, y=30, font_name = 'Arcade.ttf')
        self._life = GLabel(text = f"Lives: {self._lives}",font_size=60,\
             left=5, bottom=5, \
            x=120, y=24*GAME_HEIGHT/25, font_name = 'Arcade.ttf')
        self._logo = GLabel(text = "War Against Humanity",\
            font_size=60, left=5,\
             bottom=5, x=GAME_WIDTH/2, y=24*GAME_HEIGHT/25, \
                 font_name = 'Arcade.ttf')
        self._inst = None
        if self._state == STATE_INACTIVE:
            self._text = self._text = GLabel(\
                text = f"Press {self._startkey} to start",font_size=60,\
                 left=5, bottom=5, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, \
                     font_name = 'Arcade.ttf')
        else:
            self._text = None
        
        
    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        if self._state == STATE_INACTIVE:
            self._determineState()
        elif self._state == STATE_NEWWAVE:
            self.newwave()
        elif self._state == STATE_ACTIVE:
            self.active(dt)
        elif self._state == STATE_PAUSED:
            self.paused()
        elif self._state == STATE_CONTINUE:
            self.continues()
        elif self._state == STATE_COMPLETE:
            self.complete()


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # IMPLEMENT ME
        #self._blsc.draw(self.view)
        if self._text != None:
            self._text.draw(self.view)
        if self._logo is not None:
            self._logo.draw(self.view)
        if self._life is not None:
            self._life.draw(self.view)
        if self._score is not None:
            self._score.draw(self.view)
        if self._inst is not None:
            self._inst.draw(self.view)
        if self._wave is not None:
            self._wave.draw(self.view)

        
    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Determines the current state and assigns it to
        self.state

        This method checks for a key press, and if there is
        one, changes the state to the next value.  A key
        press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as
        we hold down the key. The user must release the
        key and press it again to change the state.
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self._lastkeys == 0
        if change and self.input.is_key_down(self._startkey):
            self._state = STATE_NEWWAVE
        self.lastkeys = curr_keys
    

    def newwave(self):
        """
        Plays background music when a new wave of aliens start.
        Creates a new instance of class Wave
        sets state to STATE_ACTIVE
        sets text to None
        """

        self._sound.play()
        self._inst = GLabel(text = "Press spacebar to fire",\
            font_size=30, left=5, bottom=5, \
                x=GAME_WIDTH/2, y=DEFENSE_LINE+20, font_name = 'Arcade.ttf')
        self._wave = Wave(self._playerlose, self._alienblast, self._shipshoot)
        self._state = STATE_ACTIVE
        self._text = None
    
    
    def active(self, dt):
        """
        Updates the current wave
        Plays background music when a new wave of aliens start.
        Creates a new instance of class Wave
        sets state to STATE_ACTIVE
        sets text to None
        """
        self._wave.update(self.input, dt)
        if self._wave.getShipDies() and self._lives > 1:
            self._lives-=1
            self._state = STATE_PAUSED
        elif self._wave.getPlayerWin():
            self._win = True
            self._state = STATE_COMPLETE
        elif self._wave.alienLine():
            self._win = False
            self._state = STATE_COMPLETE
        elif self._wave.getShipDies() and self._lives == 1:
            self._win = False
            self._state = STATE_COMPLETE
        self._score.text = f"Player's score: {self._wave.getScore()}"
    
    
    def paused(self):
        """
        Updates the text of self._life
        calls the function to draw self._wave objects
        Changes state to STATE_CONTINUE if a key press is detected
        """
        self._life.text = f"lives: {self._lives}"
        self._wave.draw(self.view)
        self._text = GLabel(text = f"Press {self._startkey} to continue",\
            font_size=60, left=5, bottom=5, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, \
                font_name = 'Arcade.ttf')
        if self.input.is_key_down(self._startkey):
            self._state = STATE_CONTINUE
            self._text = None
        
        
    def continues(self):
        """
        Creates a new ship object
        changes state to STATE_ACTIVE
        """
        self._wave.setShip(Ship(GAME_WIDTH/2, SHIP_BOTTOM+SHIP_HEIGHT/2))
        self._wave.setShipDies(False)
        self._wave.setPlayerWin(False)
        self._state = STATE_ACTIVE
    
    
    def complete(self):
        """
        Final state of the game, where wave is set to None, 
        and music is played if the player wins
        """
        self._sound.stop()
        self._life = None
        self._inst = None
        self._score = GLabel(text = f"Player's score: {self._wave.getScore()}",\
            font_size=60, left=5, bottom=5, x=GAME_WIDTH/2, \
                y=120, font_name = 'Arcade.ttf')
        self._wave = None
        if self._win == False:
            self._logo.text =  'War Against Humanity'
            self._text = GLabel(text = "You lost :(",font_size=60, \
                left=5, bottom=5, x=GAME_WIDTH/2, y=4*GAME_HEIGHT/5, \
                    font_name="Arcade.ttf")
        elif self._win == True:
            #self._sound = None
            self._playerWin.play()
            self._logo = None
            self._lives = None
            self._text = GLabel(text = "Well done! You have completed the game.",\
                font_size=60, \
                left=5, bottom=5, x=GAME_WIDTH/2, y=GAME_HEIGHT/2, font_name='Arcade.ttf')
        self._state = 6
