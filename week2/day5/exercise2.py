class Person():
    def __init__(self, name, age, occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

    def show_details(self, yearsOfExperience ):
        print(f"Hello my name is {self.name}, I am a {self.occupation} and I have {yearsOfExperience} of experience")



first_person = Person("John", 36, "Software Engineer")
first_person.show_details(5)