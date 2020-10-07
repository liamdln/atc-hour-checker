import datetime

class Menu():

    def __init__(self, validAnswers):
        self.validAnswers = validAnswers

    def displayMenu(self):
        print("""\nMenu:\nPlease choose an option:
            a) Search user.
            b) Enter search dates.
            c) Change minimum hours.
            d) Enter airport positions.
            e) Wipe settings.
            f) List settings.""")

    def getMenuUserChoice(self):
        userChoice = input("Enter choice (a, b, c, d, e or f): ")
        return userChoice.lower()

    def validateUserChoice(self, userChoice):
        if userChoice not in self.validAnswers:
            return False
        else:
            return True
