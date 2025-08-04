class Card():
  
    SUITS = ['Hearts','Diamonds','Clubs','Spades']
    VALUES = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

    def __init___(self,suit,value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"value:{self.value} suit: {self.suit}"

    def __repr__(self):
        return f"Card(value={self.value}, suit={self.suit})"

    @property
    def suit(self):
        return self.suit

    @suit.setter
    def suit(self,suit):
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit {suit}")
        self.suit = suit


    @property
    def value(self):
        self.value

    @value.setter
    def value(self,value):
        if value not in self.VALUES:
            raise ValueError(f"Invalid suit {value}")
        self.suit = value
        