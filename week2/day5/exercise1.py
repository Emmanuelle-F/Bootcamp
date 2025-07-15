# Create a class Square
class Square ():
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

# Create an instance of class Square
square1 = Square(5,5)
square2 = Square(7,10)

area1 = square1.area()
print (f"The area of square1 is {area1}")

area2 = square2.area()
print (f"The area of square2 is {area2}")
        