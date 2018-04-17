import random
import math

from gamelib import *

class ZombieCharacter(ICharacter):
    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)

    def selectBehavior(self):
        prob = random.random()

        # If health is less than 50%, then heal with a 10% probability
        if prob < 0.1 and self.getHealth() < self.getInitHealth() * 0.5:
            return HealEvent(self)

        # Pick a random direction to walk 1 unit (Manhattan distance)
        x_off = random.randint(-1, 1)
        y_off = random.randint(-1, 1)

        # Check the bounds
        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()
        x, y = self.getPos()
        if x + x_off < 0 or x + x_off >= size_x:
            x_off = 0
        if y + y_off < 0 or y + y_off >= size_y:
            y_off = 0

        return MoveEvent(self, x + x_off, y + y_off)

class PlayerCharacter(ICharacter):
    lastScanned = False
    healCount = 5

    def __init__(self, obj_id, health, x, y, map_view):
        ICharacter.__init__(self, obj_id, health, x, y, map_view)
        # You may add any instance attributes you find useful to save information between frames

    def selectBehavior(self):
        # Replace the body of this method with your character's behavior
        movable_spots = set()
        zombie_spots = set()
        x, y = self.getPos()

        self.find_movable_spots(x, y, movable_spots, 3)

        # If health is less than 50%, then heal
        if self.getHealth() < self.getInitHealth() * 0.75 and self.healCount != 0:
            self.lastScanned = False
            self.healCount-=1
            return HealEvent(self)

        elif not self.lastScanned:
            ScanEvent(self)
            self.lastScanned = True

        #Attack if zombied are 3 distance or less away. Otherwise, walk
        elif self.lastScanned:
            self.find_zombie_spots(x, y, zombie_spots, 1)
            list_zombie_spots = list(zombie_spots)

            #if there's a zombie 1 spot away, focus him
            if len(list_zombie_spots) > 0:
                if len(list_zombie_spots) == 1:
                    index = 0
                else:
                    index = random.randint(0, len(list_zombie_spots) - 1)

                return AttackEvent(self, list_zombie_spots[index][1])

            #otherwise, look at zombies 2 spots away
            else:
                self.find_zombie_spots(x, y, zombie_spots, 2)
                list_zombie_spots = list(zombie_spots)

                #if zombie is 2 spots away, focus on him
                if len(list_zombie_spots) > 0:
                    if len(list_zombie_spots) == 1:
                        index = 0
                    else:
                        index = random.randint(0, len(list_zombie_spots) - 1)

                    return AttackEvent(self, list_zombie_spots[index][1])

                #otherwise, focus on zombies 3 spots away
                else:
                    self.find_zombie_spots(x, y, zombie_spots, 3)
                    list_zombie_spots = list(zombie_spots)

                    #if there's a zombie 3 spots away, focus him
                    if len(list_zombie_spots) > 0:
                        if len(list_zombie_spots) == 1:
                            index = 0
                        else:
                            index = random.randint(0, len(list_zombie_spots) - 1)

                        return AttackEvent(self, list_zombie_spots[index][1])

                    #otherwise, walk
                    else:
                        list_movable_spots = list(movable_spots)
                        if len(list_movable_spots) == 1:
                            index = 0
                        else:
                            index = random.randint(0, len(list_movable_spots) - 1)
                        return MoveEvent(self, list_movable_spots[index][0], list_movable_spots[index][1])
            self.lastScanned = False



    #method for checking a distance of max 3 away from player
    #returns a set of tuples that are open which the player can move to
    def find_movable_spots(self, x, y, set, steps):
        if steps == 0:
            return
        if self.is_valid_coordinate(x + 1, y):
            if self.spot_not_occupied(x + 1,y):
                set.add((x + 1,y))
                self.find_movable_spots(x + 1, y, set, steps - 1)
        if self.is_valid_coordinate(x - 1, y):
            if self.spot_not_occupied(x - 1, y):
                set.add((x - 1, y))
                self.find_movable_spots(x - 1, y, set, steps - 1)
        if self.is_valid_coordinate(x, y + 1):
            if self.spot_not_occupied(x, y + 1):
                set.add((x, y + 1))
                self.find_movable_spots(x, y + 1, set, steps - 1)
        if self.is_valid_coordinate(x, y - 1):
            if self.spot_not_occupied(x, y - 1):
                set.add((x, y - 1))
                self.find_movable_spots(x, y - 1, set, steps - 1)

    # method for checking a distance of 1 away from player
    # returns a set of zombies that the player can attack well
    def find_zombie_spots(self, x, y, set, steps):
        if steps == 0:
            return
        elif self.is_valid_coordinate(x + 1, y):
            if not self.spot_not_occupied(x + 1, y):
                zombie_ID = self.get_zombie_ID(x + 1, y)
                set.add((x + 1, y), zombie_ID)
                self.find_zombie_spots(x + 1, y, set, steps - 1)
        elif self.is_valid_coordinate(x - 1, y):
            if not self.spot_not_occupied(x - 1, y):
                zombie_ID = self.get_zombie_ID(x - 1, y)
                set.add((x - 1, y), zombie_ID)
                self.find_zombie_spots(x - 1, y, set, steps - 1)
        elif self.is_valid_coordinate(x, y + 1):
            if not self.spot_not_occupied(x, y + 1):
                zombie_ID = self.get_zombie_ID(x, y + 1)
                set.add((x, y + 1), zombie_ID)
                self.find_zombie_spots(x, y + 1, set, steps - 1)
        elif self.is_valid_coordinate(x, y - 1):
            if not self.spot_not_occupied(x, y - 1):
                zombie_ID = self.get_zombie_ID(x, y - 1)
                set.add((x, y - 1), zombie_ID)
                self.find_zombie_spots(x, y - 1, set, steps - 1)


    #check for valid coordinates
    def is_valid_coordinate(self, x, y):
        # Check the bounds
        map_view = self.getMapView()
        size_x, size_y = map_view.getMapSize()
        if x < 0 or x >= size_x:
            return False
        if y < 0 or y >= size_y:
            return False
        return True

    #determine if there's a zombie at a spot
    def spot_not_occupied(self, x, y):
        for object in self.getScanResults():
            if object[0] == (x,y):
                return False
        return True

    #get zombie ID
    def get_zombie_ID(self, x, y):
        for object in self.getScanResults():
            if object[0] == (x,y):
                return object[1]