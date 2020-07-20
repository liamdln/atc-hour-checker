import datetime


class Menu():

    def displayMenu(self):
        print("""\nPlease choose an option:
            a) Search user.
            b) Enter search dates.
            c) Change minimum hours.
            d) Enter airport positions.
            e) Wipe settings.""")

    def getMenuUserChoice(self):
        userChoice = input("Enter choice (a, b, c, d or e): ")
        return userChoice.lower()

    def validateUserChoice(self, userChoice):
        validAnswers = ["a", "b", "c", "d", "e"]
        if userChoice not in validAnswers:
            return False
        else:
            return True
