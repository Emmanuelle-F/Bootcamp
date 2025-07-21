# Try to recreate the class explained below:

# We have a class called Door that has an attribute of is_opened declared when an instance is initiated.

# We can create a class called BlockedDoor that inherits from the base class Door.

# We just override the parent class's functions of open_door() and close_door() with our own BlockedDoor version of those functions,
#  which simply raises an Error that a blocked door cannot be opened or closed.

class Door:
    def __init__(self, is_opened):
        self.is_opened = is_opened

    def open_door(self):
        if not self.is_opened:
            self.is_opened = True
            print("The door is open.")
        else:
            print("The door is already open.")

    def close_door(self):
        if self.is_opened:
            self.is_opened = False
            print("The door is closed.")
        else:
            print("The door is already closed.")

class BlockedDoor(Door):
    def __init__(self, is_opened):
        super().__init__(is_opened)

    def open_door(self):
        print ("Error: A blocked door cannot be opened.")

    def close_door(self):
        print ("Error: A blocked door cannot be closed.")



# Regular Door
door = Door(True)
door.close_door()
door.open_door()


# Blocked Door
blocked = BlockedDoor(True)
blocked.open_door()

