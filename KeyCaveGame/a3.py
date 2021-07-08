

#Imports
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk
from PIL import Image

#Constants
TASK_ONE="Task1"
TASK_TWO="Task2"
GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,     
    "game2.txt": 12,    
    "game3.txt": 19,
}

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
}

WIN_TEXT = "You have won the game with your strength and honour!"

LOSE_TEST = "You have lost all your strength and honour."

#Load game function
def load_game_1(filename):
    """Create a 2D array of string representing the dungeon to display.
    
    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the 
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)
    
    return dungeon_layout

""" Modelling Classes.  """
class GameLogic:
    """ Initialises the Game Logic class. """
    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game_1(dungeon_name)
        self._dungeon_size = len(self._dungeon)
        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions

    def get_dungeon_size(self):
        """ Returns the width of the dungeon as an integer.
            Return:
               self._dungeon_size(int): The width of the dungeon. """
        return self._dungeon_size
    
    def init_game_information(self):
        """ Returns a dictionary with postion and corresponding Entity as the key
            and values respectively. Also set's the Player's position.
            Return:
                self.game_information(dict): A dictionary containing the position and it's
                entity as the key's and values. """
        self.game_information = {}
        
        wall_positions = self.get_positions(WALL)
        key_position = self.get_positions(KEY)
        door_position = self.get_positions(DOOR)
        player_position = self.get_positions(PLAYER)
        move_increase_position = self.get_positions(MOVE_INCREASE)

        self._player.set_position(player_position[0])
        self.get_player().get_position()


        self.game_information.update({key_position[0]: (Key())})
        self.game_information.update({door_position[0]: (Door())})
        for locations in wall_positions:
            self.game_information.update({locations: (Wall())})

        if move_increase_position != []:
            self.game_information.update({move_increase_position[0]: (MoveIncrease())})
        
        return self.game_information
                
    def get_game_information(self):
        """ Returns adictionary containing the position and the corresponding Entity,
            as the keys and values, for thecurrent dungeon.
            Return:
                self._game_information(dict): A dictionary containing the position and it's
                entity as the key's and values. """
        return self._game_information

    def set_game(self, dic):
        self._game_information = dic

    def get_player(self):
        """ This method returns the Player object within the game.
            Return:
                self._player(Entity): The representation of the player object. """
        return self._player

    def get_entity(self, position):
        """ Returns an Entity at a given position in the dungeon. If the position is off map,
            then returns None.
            Paramters:
                position(tuple<int, int>): The given position to be tested if entity exists from it.
            Returns:
                entity_in_position(Entity): Entity in the given position.
                None if no Entity in given position. """
        for location in self.game_information:
            if position == location:
                entity_in_position = self.game_information.get(position, None)
                return entity_in_position

    def get_entity_in_direction(self, direction):
        """ Returns an Entity at a given position in the dungeon. If the position is off map,
            then returns None.
            Paramters:
                direction(str): Diirection of the player (see DIRECTIONS)
            Returns:
                entity_in_direction(Entity): The entity in the given direction of player."""
        new_position = self.new_position(direction)
        return self.get_entity(new_position)
        
    def collision_check(self, direction):
        """ Returns ​False​ if a player cantravel in the given direction, they won’t collide. ​
            Returns True if they will collide.
            Parameters:
                direction(str): Direction of the player (see DIRECTIONS)
            Returns:
                True if Entity can collide.
                False if it can not,"""
        if str(self.get_entity_in_direction(direction)) == str(Wall()):
            return True
        else:
            return False
        

    def new_position(self, direction):
        """ Returns a tuple of integers that represents the new position given the direction.
            Parameters:
                direction(str): Diirection of the player (see DIRECTIONS)
            Returns:
                new_position(tuple<int, int>): Tuple of integers representing the new position
                                                given the direction. """
        player_position = self.get_player().get_position()
        coordinate = DIRECTIONS.get(direction)
        position1 = player_position[0]+coordinate[0]
        position2 = player_position[1]+coordinate[1]
        new_position = (position1, position2)
        
        return new_position


    def move_player(self, direction):
        """ Updates the Player’s position to place them one position in the given direction.
            Parameters:
                direction(str): Diirection of the player (see DIRECTIONS) """
        position = self.new_position(direction)
        self._player.set_position(position)

    def check_game_over(self):
        """ Return True if the game has been ​lost and False otherwise.
            Return:
                True (bool) if game lost.
                False (bool) if not game lost. """
        player_position = self.get_player().get_position()
        player_inventory = self.get_player().get_inventory()
        moves_remain = self.get_player().moves_remaining()
        if player_position == self.get_positions(DOOR) and player_inventory == [str(Key())]:
            return True
        elif moves_remain == 0:
            return True
        else:
            return False

    def set_win(self, win):
        """ Set the game’s win state to be True or False.
            Parameters:
                win(bool): Game's state, either True or False. """
        self._win = win

    def won(self):
        """ Return game’s win state.
            Returns:
                self._win(bool): The win state."""
        return self._win

class Entity(object):
    """ A generic Entity within the game. """
    def __init__(self):
        """ Initialises an Entity instance. """
        self._id = "Entity"
        self._collidable = True
        self._type = 'Entity'
        self._name = self._type
        self._colour = None
        self._image = None

    def get_id(self):
        """ Returns a string representing the Entity's ID.
            Returns:
                self._id(str): String representing Entity's ID. """
        return self._id

    def set_collide(self, other):
        """ Sets the collisiton state for the Entity to be True.
            Parameters:
                other(bool): The collision state of Entity. """
        self._collidable = other

    def can_collide(self):
        """ Returns True if the Entity can be collided with (anotherEntity
            can share the position that this one is in) and False otherwise.
            Returns:
                self._collidable(bool): The collision state of Entity."""
        return self._collidable
        
    def __str__(self):
        """ Returns the string representation of the Entity. """
        return self._type+"('" + self._id + "')"

    def __repr__(self):
        """ Returns the string representation of the Entity. """
        return self.__str__()
    
    def get_name(self):
        """Returns name as displayed on GUI
            Returns:
                self._name(str): The name to be displayed on GUI."""
        return self._name
    
    def get_colour(self):
        """Returns the colour of box in GUI for TASK ONE.
            Returns:
                self._colour(str): Colour of box containting the enitity."""
        return self._colour

    def get_image(self):
        """Open's the image of the enity to be displayed on GUI for TASK_TWO.
            Returns:
                self._image: Variable which open's the image to be later drawn."""
        return self._image

class Wall(Entity):
    """ A special type of an Entity. """
    def __init__(self):
        """ Initialises the Wall's instance. Methods inherited from Entity class. """
        super().__init__()
        self._collidable = False
        self._id = WALL
        self._type = 'Wall'
        self._colour = "dark gray"
        self._name = ""
        self._image = Image.open("images/wall.png")

class Item(Entity):
    """ Special type of Enitity within the game. It is an abstract class. """
    def __init__(self):
        """ Initialise's an instance of an Item Entity. """
        self._collidable = True
        self._id = 'Entity'
        self._type = 'Item'
        self._name = "Item"
        self._colour = None
        self._image = None

    def on_hit(self, game):
        """ Raises the NotImplementedError.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        raise NotImplementedError

class Key(Item):
    """ A special type of Item. """
    def __init__(self):
        """ Initialises an instance of the Key Entity. Methods inherited from Item. """
        self._collidable = True
        self._id = KEY
        self._type = 'Key'
        self._colour = "yellow"
        self._name = "Trash"
        self._image = Image.open("images/key.png")
        self._got_key = False

    def on_hit(self, game):
        """ Adds the Key to PLayer's Inventory and rmeoves it from the dungeon.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        game.get_player().add_item(self)
        key_position = game.get_positions(KEY)[0]
        game._game_information.pop(key_position)
        self._got_key = True

    def got_key(self):
        """ Returns if the player has got the key
            Returns:
                self._got_key(bool): Returns true if key in player's inventory, false otherwise."""
        return self._got_key
        
class MoveIncrease(Item):
    """ MoveIncrease is a special type of Item. """
    def __init__(self, moves=5):
        """ Intialises an instance of the MoveIncrease Entity. Methods inherited from Item.
            Parameters:
                moves(int): The number of moves a player is allowed. Default at 5. """
        super().__init__()
        self._collidable = True
        self._id = MOVE_INCREASE
        self._type = 'MoveIncrease'
        self._moves = moves
        self._colour = "orange"
        self._name = "Banana"
        self._image = Image.open("images/moveIncrease.png")
        
    def on_hit(self, game):
        """ Increases the number of moves for the player and removes the item from the game.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        game.get_player().change_move_count(self._moves)
        move_increase_position = game.get_positions(MOVE_INCREASE)[0]
        game._game_information.pop(move_increase_position)
        
class Door(Entity):
    """ A Door is a special type of an Entity. """
    def __init__(self):
        """ Intialises the instance of a Door Entity. Methods inherited from Entity class. """
        self._collidable = True
        self._id = DOOR
        self._type = 'Door'
        self._colour = "red4"
        self._name = "Nest"
        self._image = Image.open("images/door.png")
        
    def on_hit(self, game):
        """ Set's 'game over' state to be true id player's inventory contains the key. Else,
            print's "You don't have the key!".
            Parameters:
                game(class): Class containing game information and how it should play out."""
        if game.get_player().get_inventory() != []:
            game.set_win(True)
            door_position = game.get_positions(DOOR)[0]
            game._game_information.pop(door_position)
        else:
            return
            

class Player(Entity):
    """ A special type of Entity. """
    def __init__(self, move_count):
        """ Initialise a Player Instance.
            Paramters:
                move_count(int): Represents the moves a Player can have for given dungeon."""
        super().__init__()
        self._collidable = True
        self._id = PLAYER
        self._type = 'Player'
        self._move_count = move_count
        self._inventory = []
        self._position = None
        self._colour = "spring green"
        self._name = "Trash"
        self._image = Image.open("images/player.png")
        
    def set_position(self, position):
        """ Sets the position of  the Player.
            Parameters:
                position(tuple<int, int>): The position required to set for player. """
        self._position = position

    def get_position(self):
        """ Returns a tuple of ints representing the position of the Player. If the Player’s
            position hasn’t been set yet then, returns None.
            Returns:
                self._position(tuple<int, int>): The position of the player.
                None if no position has been set yet. """
        return self._position

    def change_move_count(self, number):
        """ Adds number to the Player's move count.
            Parameters:
                number(int): Number to be added to player's move count. """
        self._move_count += number

    def moves_remaining(self):
        """ Returns an int representing how many moves thePlayer has left before they reach
            the maximum move count.
            Returns:
                self._move_count(int): The Player's move remaining before reaching maximam
                    move count."""
        return  self._move_count

    def add_item(self, item):
        """ Adds the item to the Player’s Inventory.
            Parameters:
                item(Entity): An entity to be added to Player's Inventory."""
        self._inventory.append(item)

    def get_inventory(self):
        """ Returns a list that represents the Player’s inventory. If the Player has nothing
            in their inventory, returns an empty list.
            Returns:
                self._inventory(List): A list that represents the Player's inventory."""
        return self._inventory

    def moves(self, number):
        """Sets the moves remaining to a specific number.
            Parameters:
                number(int): The number to change move count to. """
        self._move_count = number

""" View classes """

class AbstractGrid(tk.Canvas):
    """ Instance of AbstractGrid class which inherits from tk.Canvas"""
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """Intialises the canvas to be drawn.
            Parameters:
                master: Master window of GUI
                rows(int): Number of rows of the grid.
                cols(int): Number of cols of the grid.
                width(pixel): The width of grid.
                height(pixel): The height of the grid."""
        super().__init__(master, width=width, height=height, **kwargs)
        self._master = master
        self._rows = rows
        self._cols = cols
        self._width = width/cols
        self._height = height/rows

    def get_bbox(self, position):
        """Returns the bounding box for the (row, col) position.
            Parameters:
                position(tuple): The tuple representing the position in (row, column) format.
            Returns:
                bbox(tuple): Bounding box for the (row, col) position"""
        bbox1_x = self._width * position[1]
        bbox1_y = self._height * position[0]
        bbox1 =(bbox1_x, bbox1_y)
        bbox2_x = bbox1_x + self._width 
        bbox2_y = bbox1_y + self._height 
        bbox2 =(bbox2_x,bbox2_y)
        bbox = [bbox1, bbox2]
        return bbox

    def pixel_to_position(self, pixel):
        """Converts the x, y pixel position (in graphics units) to a (row, col) position
            Parameters:
                pixel(pixel):The x, y pixel position
            Returns:
                position(tuple): The tuple representing the position in (row, column) format."""
        x, y = pixel
        row = int(y/self._height)
        column = int(x/self._width)
        position = (row, column)
        return position

    def get_position_center(self, position):
        """ Gets the graphics coordinates for the center of the cell at the
            given (row, col) position.
            Parameters:
                position(tuple): The tuple representing the position in (row, column) format.
            Returns:
                centre(tuple): The centre position of a cell."""
        bbox = self.get_bbox(position)
        bbox1 = bbox[0]
        bbox2 = bbox[1]
        centre_x = (bbox1[0]+bbox2[0])/2
        centre_y = (bbox1[1]+bbox2[1])/2
        centre = (centre_x, centre_y)
        return centre

    def annotate_position(self, position, texts):
        """Annotates the cell at the given (row, col) position with the
            provided text.
            Parameters:
                position(tuple): The tuple representing the position in (row, column) format.
                texts(string): The text to be used to annotate cell.
            """
        self.create_text(self.get_position_centre(position), text = texts)

class DungeonMap(AbstractGrid):
    """ An instance of the DungeonMap class, responsible for handling the map to be displayed. """
    def __init__(self, master, rows, cols, width=600, height=600, **kwargs):
        """Intialises the DungeonMap canvas to be drawn.
            Parameters:
                master: Master window of GUI
                rows(int): Number of rows of the grid.
                cols(int): Number of cols of the grid.
                width(pixel): The width of grid.
                height(pixel): The height of the grid."""
        super().__init__(master, rows, cols, width, height, bg="light gray")
    
    def draw_grid(self, dungeon, player_position):
        """Draws the dungeon on the DungeonMap based on dungeon game information,
            and draws the player at the specified (row, col) position.
            Paramters:
                dungeon(dict): The game information dictionary with all positions of entities.
                player_position(tuple): The position of the player in (row,column) format."""
        for key in dungeon:
            entity = dungeon.get(key)
            self.create_rectangle(self.get_bbox(key), fill = entity.get_colour())
            self.create_text(self.get_position_center(key), text = entity.get_name())
        
        self.create_rectangle(self.get_bbox(player_position), fill = "pale green")
        self.create_text(self.get_position_center(player_position), text = "Ibis")

 
class KeyPad(AbstractGrid):
    """ An instance of the KeyPad class, repsonsible for handling the keypad. """
    
    def __init__(self, master, rows=2, columns=3, width=200, height=100, **kwargs):
        """Intialises the KeyPad canvas to be drawn.
            Parameters:
                master: Master window of GUI.
                rows(int): Number of rows of the grid.
                cols(int): Number of cols of the grid.
                width(pixel): The width of grid.
                height(pixel): The height of the grid."""
        super().__init__(master, rows, columns, width, height, bg="white")
  
    def draw_grid(self):
        """ Draws the grid of the keypad (North, South, West, East)"""
        directions = {"N":(0,1), "S":(1,1), "W": (1,0), "E": (1,2)}
        for direction in directions:
            coordinate = directions.get(direction)
            self.create_rectangle(self.get_bbox(coordinate), fill = "dark gray")
            self.create_text(self.get_position_center(coordinate), text = direction)


    def pixel_to_direction(self, pixel):
        """  Converts the x, y pixel position to the direction of the arrow depicted
            at that position.
            Parameters:
                pixel(pixel): x, y pixel position to be converted.
            Returns:
                direction(str): The direction as a string (see directions dictionary).
                None if no direction given by pixel. """
        position = self.pixel_to_position(pixel)
        directions = {"W":(0,1), "S":(1,1), "A": (1,0), "D": (1,2)}
        for direction in directions:
            if directions.get(direction) == position:
                return direction
        else:
            return None
        


class GameApp(object):
    """ The controller class.  Manages necessary communication between any model
        and view classes, as well as event handling. """
    def __init__(self, master, task=TASK_TWO, dungeon_name="game3.txt"):
        """ Initalises the controller class.
            Parameters:
                master: The master of the GUI.
                task: A constant which determines if game is run via TASK_ONE or TASK_TWO.
                dungeon_name(txt): The file containing the dungeon. """
        self._task = task
        self._dungeon_name = dungeon_name
        self._master = master
        master.title("Key Cave Adventure Game")
        self._lbl = tk.Label(master, text="Key Cave Adventure Game")
        self._lbl.pack(side=tk.TOP, fill=tk.X, ipady=4)
        self._lbl.configure(bg="spring green")
        self._lbl.configure(font=("Arial", 15))
        if self._task == TASK_ONE: #check bg for keypad, zooming out
            #window size
            master.minsize(800, 600)

            #game initialisation
            self._game = GameLogic(dungeon_name)
            self._game_info = self._game.get_game_information()
            size = self._game.get_dungeon_size()
            player_position = self._game.get_player().get_position()
            self._player = self._game.get_player()

            #map
            self._dungeon_map = DungeonMap(master,size,size)
            self._dungeon_map.pack(side=tk.LEFT)
            self._dungeon_map.draw_grid(self._game_info, player_position)

            #keypad
            self._key_pad = KeyPad(master)
            self._key_pad.pack(side=tk.LEFT, expand= True)
            self._key_pad.draw_grid()
            
            self._mode = None

        if self._task == TASK_TWO:
            #window size
            master.maxsize(800, 800)

            #game intialisation
            self._game = GameLogic(dungeon_name)
            self._game_info = self._game.get_game_information()
            self._size = self._game.get_dungeon_size()
            self._player = self._game.get_player()
            player_position = self._player.get_position()
            self._mode = None
            self._player = self._game.get_player()

            #status bar
            self._status_bar = StatusBar(master)
            self._status_bar.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
            self._status_bar._new_game.configure(command=self.new_game_press)
            self._status_bar._quit_game.configure(command=self.quit_press)
            moves = self._player.moves_remaining()
            self._status_bar.set_moves(moves)
            
            #map
            self._dungeon_map = AdvancedDungeonMap(master,self._size,self._size)
            self._dungeon_map.pack(side=tk.LEFT, anchor="w")
            self._dungeon_map.draw_grid(self._game_info, player_position)

            #keypad
            self._key_pad = KeyPad(master)
            self._key_pad.pack(side=tk.LEFT, anchor = "e")
            self._key_pad.draw_grid()
             
            #menu
            menubar = tk.Menu(self._master)
            self._master.config(menu=menubar)
            filemenu = tk.Menu(menubar)
            menubar.add_cascade(label="File", menu=filemenu)
            filemenu.add_command(label="Save game", command=self.save_game)
            filemenu.add_command(label="Load game", command=self.load_game)
            filemenu.add_command(label="New game", command=self.new_game_press)
            filemenu.add_command(label="Quit Game", command=self.quit_press)

            #status of key and move increase
            self._key_got = False
            self._got_move = False

        #binds
        self._key_pad.bind("<Button-1>", self.button1)
        self._master.bind("<Key>", self.move)

    def button1(self, event):
        """Responsible for handling events due to keyboard presses.
            Paramters:
                event(pixel): The event that has occured on canvas."""
        if self._key_pad.pixel_to_direction((event.x, event.y)) != None:
            self._mode = self._key_pad.pixel_to_direction((event.x, event.y))
            self.action()
            self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
            

    def move(self, event):
        """Responsible for handling events due to keypad press.
            Paramters:
                event(pixel): The event that has occured on canvas."""
        movements = ["a", "s", "d", "w"]
        for direction in movements:
            if direction==event.char:
                self._mode = event.char.upper()
                self.action()
                self._dungeon_map.draw_grid(self._game_info, self._player.get_position())

    def new_game_press(self):
        """ Reset's the game to start again. """
        self._dungeon_map.delete(tk.ALL)
        self._game = GameLogic(self._dungeon_name)
        self._game_info = self._game.get_game_information()
        self._size = self._game.get_dungeon_size()
        self._player = self._game.get_player()
        player_position = self._player.get_position()
            
        self._dungeon_map.draw_grid(self._game_info, player_position)
        self._status_bar.set_time(0)
        moves = self._player.moves_remaining()
        self._status_bar.set_moves(moves)
        self._key_got = False
        self._got_move = False

    def quit_press(self):
        """ Prompt's user to ask if they want to quit. If yes, terminates the window. """
        quit_question = tk.messagebox.askquestion ('Quit?',
                                              "Are you sure you want to quit?")
        if quit_question == "yes":
            self._master.destroy()
            exit
        elif quit_question == "no":
            pass

    def save_game(self):
        """ Prompt the user for the location to save their file and save all necessary information
            to replicate the current state of the game. """
        self._player = self._game.get_player() 
        self._player_pos = self._game.get_player().get_position() 
        self._moves = self._player.moves_remaining() 
        self._time = self._status_bar.get_time() 
        self._key_gotten = self._key_got 
        self._move_gotten = self._got_move 
        self._size = self._game.get_dungeon_size()
        game_information = [self._player_pos, self._moves, self._time, self._key_gotten,
                            self._move_gotten, self._size, self._dungeon_name]
        
        filename = filedialog.asksaveasfilename()
        try:
            if filename:
                self._filename = filename
            if self._filename:
                file = open(self._filename, "w")
                for info in game_information:
                    file.write(str(info)+"\n")
                file.close()
                
        except (IOError, EOFError) as e:
            pass

    def load_game(self):
        """ Prompt the user for the location of the file to load a game from and load the
            game described in that file. """
        filename = filedialog.askopenfilename() #aks user to save file
        try:
            if filename:
                self._filename = filename
                file = open(filename, "r")
                info = file.readlines()

                dungeon_name = info[6].strip()
                if dungeon_name != self._dungeon_name and dungeon_name in ["game1.txt",
                                                                           "game2.txt",
                                                                           "game3.txt"]:
                    self._dungeon_name = dungeon_name
                    self._game = GameLogic(self._dungeon_name)
                    self._game_info = self._game.get_game_information()
                    self._player = self._game.get_player()
                    self._size = self._game.get_dungeon_size()
                    self._dungeon_map.adjust(self._size, self._size)
                    
                player_pos = eval(info[0])
                self._player_pos = player_pos 
                self._player.set_position(self._player_pos)
                self._dungeon_map.delete(tk.ALL)
                
                moves = int(info[1])
                self._player.moves(moves)
                self._status_bar.set_moves(moves)

                time = int(info[2])
                self._status_bar.set_time(time)

                key_taken = bool(info[3].strip())
                move_taken = bool(info[4].strip())
                if info[3] == "True\n":
                    pos = self._game.get_positions(KEY)[0]
                    entity = self._game.get_entity(pos)
                    if entity!=None:
                        entity.on_hit(self._game)
                if info[4] == "True\n":
                    pos = self._game.get_positions(MOVE_INCREASE)[0]
                    entity = self._game.get_entity(pos)
                    if entity != None:
                        entity.on_hit(self._game)
                        self._player.change_move_count(-5)

                self._size = self._game.get_dungeon_size()    
                self._dungeon_map.draw_grid(self._game_info, self._player_pos)
                
        except (IOError, EOFError, IndexError, SyntaxError) as e:
            messagebox.showinfo("ERROR", "Unsupported File")
            pass

    def key_status(self):
        """ Set's the key_status to True if taken. """
        if self._game.get_player().get_position() == self._game.get_positions(KEY)[0]:
            self._key_got = True

    def move_increase_status(self):
        """ Set's the move_increase_status to True if taken. """
        if self._game.get_player().get_position() == self._game.get_positions(MOVE_INCREASE)[0]:
            self._got_move = True
    
    def action(self):
        """ Handle's the gaemplay action between the user and GUI. """
        self._dungeon_map.delete(tk.ALL)
        direction = self._mode
        if self._game.collision_check(direction) == True:   #checks if player does not collide
            self._game.get_player().change_move_count(-1)
            if self._task == TASK_TWO:
                moves = self._player.moves_remaining()
                self._status_bar.set_moves(moves)
            if self._game.get_player().moves_remaining() == 0:
                if self._task == TASK_ONE:
                    self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                    messagebox.showinfo("Game Over", LOSE_TEST)

                if self._task == TASK_TWO:
                    messages = ["You have failed",
                                            "Would you like to play again?"]
                    self._status_bar.stop_time()
                    self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                                            
                    finish_question = tk.messagebox.askquestion ('You lost!',
                                            "\n\n".join(messages))
                    if finish_question == "yes":
                        self.new_game_press()
                        self._status_bar.reset_time()
                        return
                    elif finish_question == "no":
                        self._master.destroy()
                        exit
                        return
                return
            
        else:
            self._game.move_player(direction)
            entity = self._game.get_entity(self._player.get_position())

            # process on_hit and check win state
            if entity is not None:
                entity.on_hit(self._game)
                self.key_status()
                if self._dungeon_name != "game1.txt":
                    self.move_increase_status()
                if self._game.won():
                    if self._task == TASK_ONE:
                        self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                        messagebox.showinfo("Game Over", WIN_TEXT)
                    elif self._task == TASK_TWO: #end game
                        self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                        time = self._status_bar.get_time()
                        self._status_bar.stop_time()
                        messages = ["You have finshed the level with a score of "+ str(time-1),
                                        "Would you like to play again?"]
                                        
                        finish_question = tk.messagebox.askquestion ('You won!',
                                        "\n\n".join(messages))
                        if finish_question == "yes":
                            self.new_game_press()
                            self._status_bar.reset_time()
                            return
                        elif finish_question == "no":
                            self._master.destroy()
                            exit
                            return


            self._player.change_move_count(-1)
            if self._task == TASK_TWO:
                moves = self._player.moves_remaining()
                self._status_bar.set_moves(moves)
                self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                
            if self._game.check_game_over():
                if self._task == TASK_ONE:
                    self._dungeon_map.draw_grid(self._game_info, self._player.get_position())
                    messagebox.showinfo("Game Over", LOSE_TEST)

                elif self._task == TASK_TWO:
                    messages = ["You have failed",
                                        "Would you like to play again?"]
                    self._status_bar.stop_time()                    
                    finish_question = tk.messagebox.askquestion ('You lost!',
                                            "\n\n".join(messages))
                    if finish_question == "yes":
                        self.new_game_press()
                        self._status_bar.reset_time()
                        return
                    elif finish_question == "no":
                        self._master.destroy()
                        exit
                        return
    
            
""" Task 2 """
class StatusBar(tk.Frame):
    """ An instance of status bar class which inherits from tk.Frame. """
    def __init__(self, master):
        """ Initialises the StatusBar class.
            Parameters:
                master: The master of the GUI """

        super().__init__(master, bg="white", height=80, width=800)

        #new game and quit button
        left_frame = tk.Frame(self, bg="white")
        left_frame.pack(side=tk.LEFT, padx=80)
        self._new_game = tk.Button(left_frame,text="New game",fg="black")
        self._new_game.pack(side=tk.TOP, expand=True, pady=5)      
        self._quit_game = tk.Button(left_frame,text="Quit",fg="black")
        self._quit_game.pack(side=tk.TOP, expand=True, pady=5)


        #time image
        self._time=0
        self._timer_image = Image.open("images/clock.png")
        self._timer_image = self._timer_image.resize((50,75), Image.ANTIALIAS)
        self._timer_pic = ImageTk.PhotoImage(self._timer_image)
        self._time_label = tk.Label(self, image = self._timer_pic, bg="white")
        self._time_label.pack(side=tk.LEFT)

        #time elapsed text and time
        time_frame = tk.Frame(self)
        time_frame.pack(side=tk.LEFT)
        self._time_elapsed=tk.Label(time_frame, text = "Time elapsed", bg="white")
        self._time_elapsed.configure(font=("Arial", 11))
        self._time_elapsed.pack(side=tk.TOP, expand=1, fill=tk.BOTH, anchor=tk.W)
        self._timer = tk.Label(time_frame, text = "0m 0s", bg="white")
        self._timer.configure(font=("Arial", 10))
        self._timer.pack(side=tk.TOP, expand=1, fill=tk.BOTH, anchor=tk.W)
        self._working = True
        self.new_time()

        #moves remaining image
        self._moves_remaining_image = Image.open("images/lightning.png")
        self._moves_remaining_image = self._moves_remaining_image.resize((50,75), Image.ANTIALIAS)
        self._moves_remaining_pic = ImageTk.PhotoImage(self._moves_remaining_image) 
        self._moves_remaining = tk.Label(self, image = self._moves_remaining_pic, bg="white")
        self._moves_remaining.pack(side=tk.LEFT, padx=(150,0))

        #moves remaining text and socre
        right_frame = tk.Frame(self, bg="white")
        right_frame.pack(side=tk.LEFT)        
        self._moves_left = tk.Label(right_frame, text = "Moves left", bg="white")
        self._moves_left.configure(font=("Arial", 11))
        self._moves_left.pack(side=tk.TOP)
        self._moves = tk.Label(right_frame, text = "", bg="white")
        self._moves.configure(font=("Arial", 10))
        self._moves.pack(side=tk.TOP)
        
        
    def new_time(self):
        """ Keeps increasing the time each second and converts it into minutes and seconds. """
        if self._working:
            minutes = self._time//60
            seconds = self._time%60
            time = "{}m {}s".format(minutes, seconds)
            self._timer.configure(text=time)
            self._time +=1
            self.after(1000, self.new_time)
        else:
            return

    def get_time(self):
        """ Returns the current time.
            Returns:
                self._time(int): The current time. """
        return self._time

    def set_time(self, time):
        """ Set's the time given as the current time.
            Parameters:
                time(int): The time to set the current timer to. """
        self._time = time

    def set_moves(self, moves):
        """ Set's the number of moves remaining.
            Parameters:
                moves(int): The numebr of moves to set the moves remaining to."""
        self._moves.configure(text=str(moves)+" Moves Remaining")

    def stop_time(self):
        """ Set's the state of the timer to stop continuing. """
        self._working = False

    def reset_time(self):
        """ Reset's the time and starts the timer again. """
        self._time = 0
        if not self._working:
            self._working = True
            self.new_time()
        

class AdvancedDungeonMap(AbstractGrid):
    """ Extends the DungeonMap class, accounting for images. """
    def __init__(self, master, rows, cols, width=600, height=600, **kwargs):
        """Intialises the DungeonMap canvas to be drawn.
            Parameters:
                master: Master window of GUI
                rows(int): Number of rows of the grid.
                cols(int): Number of cols of the grid.
                width(pixel): The width of grid.
                height(pixel): The height of the grid."""
        super().__init__(master, rows, cols, width, height, bg="white")
    
    def draw_grid(self, dungeon, player_position):
        """Draws the dungeon on the DungeonMap based on dungeon game information,
            and draws the player at the specified (row, col) position using images.
            Paramters:
                dungeon(dict): The game information dictionary with all positions of entities.
                player_position(tuple): The position of the player in (row,column) format."""
        #Background
        row=0
        column=0
        self._image = Image.open("images/empty.png")
        self._image = self._image.resize((int(self._width), int(self._height)), Image.ANTIALIAS)
        self._background_image = ImageTk.PhotoImage(self._image)
        while column<self._cols:
            centre_position = self.get_position_center((row,column))
            self.create_image(centre_position[0], centre_position[1], image=self._background_image)
            row+=1
            if row==self._rows:
                row=0
                column+=1

        #Entity Images
        self._images ={}
        for key in dungeon:
            entity = dungeon.get(key)
            self._image = entity.get_image()
            self._image = self._image.resize((int(self._width), int(self._height)),Image.ANTIALIAS)
            self._entity_image = ImageTk.PhotoImage(self._image)
            self._images[key] = self._entity_image
        # could have combined this with above, but program crashes
        for key in self._images:
            self._the_image = self._images.get(key)
            centre_position = self.get_position_center(key)
            self.create_image(centre_position[0], centre_position[1], image = self._the_image)


        #Player
        self._image = Image.open("images/player.png")
        self._image = self._image.resize((int(self._width), int(self._height)), Image.ANTIALIAS)
        self._player_image = ImageTk.PhotoImage(self._image)
        centre_position = self.get_position_center(player_position)
        self.create_image(centre_position[0], centre_position[1], image = self._player_image)
        
    def adjust(self, rows, cols):
        """ Adjusts the rows and column for the grid.
            Parameters:
                rows(int): Number of rows of grid to be changed to.
                cols(int): Number of columns of grid to be changed to. """
        self._rows = rows
        self._cols = cols
        self._width = 600/self._rows
        self._height = 600/self._cols

def main():
    root = tk.Tk()
    app = GameApp(root)
    root.configure(bg='white')
    root.mainloop()

if __name__ == '__main__':
    main()
