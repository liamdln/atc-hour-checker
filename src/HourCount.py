import datetime
from dateutil import parser


class Menu:

    def __init__(self, validAnswers):
        self.validAnswers = validAnswers

    @staticmethod
    def displayMenu():
        print("""\nMenu:\nPlease choose an option:
        a) Search user.
        b) Enter search dates.
        c) Change minimum hours.
        d) Enter airports and positions.
        e) Wipe settings.
        f) List settings.""")

    @staticmethod
    def getMenuUserChoice():
        userChoice = input("Enter choice (a, b, c, d, e or f): ")
        return userChoice.lower()

    def validateUserChoice(self, userChoice):
        if userChoice not in self.validAnswers:
            return False
        else:
            return True


class ApplicationSettings:

    def __init__(self, fromDate=None, toDate=None, minHours=None, cid=None, airportsToSearch=None,
                 positionsToSearch=None):
        self.fromDate = fromDate
        self.toDate = toDate
        self.minHours = minHours
        self.cid = cid
        self.airportsToSearch = airportsToSearch
        self.positionsToSearch = positionsToSearch

    def setDates(self):
        happy = False

        while not happy:

            self.fromDate = self.parseDate("Enter the date you want to measure from in format 'yyyy-mm-dd': ")
            self.toDate = self.parseDate("Enter the date you want to measure to in format 'yyyy-mm-dd': ")

            if self.toDate < self.fromDate:
                print("The date you want to measure to cannot be earlier than the date you want to measure from.")
            else:
                happy = True

        print(f"Date range changed to measure from {self.fromDate} to {self.toDate}.")

        return parser.isoparse(self.fromDate), parser.isoparse(self.toDate)

    @staticmethod
    def parseDate(question):
        happy = False
        measureDate = None
        while not happy:

            measureDate = input(question)
            try:
                year, month, day = measureDate.split("-")
                datetime.datetime(int(year), int(month), int(day))
                happy = True
            except TypeError:
                print("Date is not valid.")
                happy = False

        return measureDate

    def getMinHours(self):
        try:
            self.minHours = int(input("Enter minimum required hours: "))
            return self.minHours
        except TypeError:
            print("You did not enter a number.")
            return

    def wipeSettings(self):
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() != "y":
            return "Settings not wiped."

        self.fromDate = None
        self.toDate = None
        self.minHours = None

        return "Settings wiped."

    def listSettings(self):
        return {
            "from-date": self.fromDate,
            "to-date": self.toDate,
            "min-hours": self.minHours,
            "cid": self.cid,
            "airports": self.airportsToSearch,
            "positions": self.positionsToSearch
        }

    def editStations(self):
        print("""You are entering stations. Please read this is VERY important.
Please enter the station ICAOs first, for example OMDB, OTHH, OBBB, OJAC.
Then you will be asked to enter the positions, for example TWR, CTR, APP.
Once you have finished with each, write 'x' to stop.""")

        searchAirports = self.getUserStationData("Enter station ICAO ('x' to stop): ")
        searchPositions = self.getUserStationData("Enter the position ('x' to stop): ")

        print("Airports entered:")
        for element in searchAirports:
            print(element)

        print("Positions entered:")
        for element in searchPositions:
            print(element)

        self.airportsToSearch = searchAirports
        self.positionsToSearch = searchPositions

    def getUserStationData(self, message):
        correctData = False
        enteredData = []

        while not correctData:
            enteredData = self.takeUserStations(message)
            goodData = input("Is this correct? (y/n): ")
            if goodData.lower() == "y":
                correctData = True
            else:
                print("Okay let's try again...\n")

        return enteredData

    @staticmethod
    def takeUserStations(message):
        data = []
        takingData = True
        while takingData:
            itemToAppend = (input(message))
            if itemToAppend is not "x":
                data.append(itemToAppend.upper())
            else:
                print("Data entered:")
                for element in data:
                    print(element)
                takingData = False
        return data

    def setCid(self, cid):
        self.cid = cid
