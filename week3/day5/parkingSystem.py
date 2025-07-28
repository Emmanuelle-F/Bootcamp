class ParkingSystem ():

    def __init__(self, big, medium, small) -> None:
        self.big = big
        self.medium = medium
        self.small = small

    def addCar(self, carType):
        
        if carType == 1:
            if self.big > 0:
                self.big -=1
                return True
            else:
                return False
        elif carType == 2:
            if self.medium > 0:
                self.medium -=1
                return True
            else:
                return False
        elif carType == 3:
            if self.small > 0:
                self.small -=1
                return True
            else:
                return False


parkingSystem = ParkingSystem(1,0,0)

print(parkingSystem.addCar(1))
print(parkingSystem.addCar(2))
print(parkingSystem.addCar(3))
print(parkingSystem.addCar(1))







#  carType

#  big => 1
#  medium => 2
#  small => 3
