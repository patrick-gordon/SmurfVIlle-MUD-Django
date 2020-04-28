import random as rd
import numpy as np
import sys

class Room():

    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.x = x
        self.y = y
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None

    def __str__(self):
        r = self.name + self.description
        # + "\n".join([str(i)] for i in self.items)
        return r

    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")



class World():
    def __init__(self):
        self.grid = None
        self.rooms = None
        self.x_max = 0
        self.y_max = 0

    def make_rooms(self, room_max):
        self.grid = [0]
        self.rooms = []
        self.x_max = room_max
        self.y_max = room_max

        room_names = ("name1", "name2", "name3", "foyer")
        room_descriptions = ("desc1", "desc2", "desc3", "it's musty in here.")

        room_count = 2
        # Establish starting room
        entry_room = Room(id = 1, name = "Entry", description = "This is the start", x = 0, y = 0)

        previous_room = entry_room
        x = 0
        y = 0
        x_max = 1
        y_max = 1
        allowed_dir = ("n", "e", "s", "w")
        self.rooms = [entry_room]

        main_room_count = room_max // 3
        # While loop to make a 'backbone' list of rooms with unique id's
        while room_count < main_room_count:
            # Set a random direction
            dir = rd.choice(("s", "e"))
            if dir == "e":
                x += 1
                if x > x_max:
                    x_max = x
            if dir == "s":
                y += 1
                if y > y_max:
                    y_max = y

            room = Room(id = room_count, name = rd.choice(room_names),
                        description = rd.choice(room_descriptions),
                        x = x, y = y)

            previous_room.connect_rooms(room, dir)
            previous_room = room

            self.rooms.append(room)

            # increase room_count and start over
            room_count += 1

        # After building a backbone, store room indexes in their positions in a
        # grid, for use in checking for overwrite conflicts and making a visual

        self.grid = [0] * (y_max+1)
        for i in range(len(self.grid)):
            self.grid[i] = [0] * (x_max+1)
        for room in self.rooms:
            self.grid[room.y][room.x] = room.id

        # Main cooridor is completed, and a grid is populated with room indecies
        # and empty spaces

        # Make a new while loop to make rooms branching off of existing rooms
        while room_count >= main_room_count and room_count < room_max:
            # select random room to snake off of
            allowed_dir = []
            while allowed_dir == []:
                start_id = rd.randint(1,room_count-1)
                previous_room = self.rooms[start_id]
                x = previous_room.x
                y = previous_room.y
                # Set allowed directions
                if y+1 < y_max:
                    if self.grid[y+1][x] == 0:
                        allowed_dir.append("s")
                if y-1 > 0:
                    if self.grid[y-1][x] == 0:
                        allowed_dir.append("n")
                if x+1 < x_max:
                    if self.grid[y][x+1] == 0:
                        allowed_dir.append("e")
                if x-1 > 0:
                    if self.grid[y][x-1] == 0:
                        allowed_dir.append("w")
                if allowed_dir != []:
                    dir = rd.choice(allowed_dir)
                    if dir == "n":
                        y -= 1
                    if dir == "s":
                        y += 1
                    if dir == "e":
                        x += 1
                    if dir == "w":
                        x -= 1

                    room = Room(id = room_count+1, name = rd.choice(room_names),
                                description = rd.choice(room_descriptions),
                                x = x, y = y)
                    previous_room.connect_rooms(room, dir)
                    self.rooms.append(room)
                    self.grid[y][x] = room.id
                    room_count = len(self.rooms)

        grid = np.array(self.grid)
        np.set_printoptions(threshold=sys.maxsize)
        print(grid)
        room_dictionaries = []
        r_dict = {}
        for room in self.rooms:
            r_dict = {'id': room.id, 'name': room.name, 'description': room.description,
                    'x': room.x, 'y': room.y}
            room_dictionaries.append(dict(r_dict))
        return room_dictionaries
        return self.rooms
        return self.grid


n = 100 # Number of rooms goes here
w = World()
w.make_rooms(n)
