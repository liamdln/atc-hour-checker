import datetime
from dateutil import parser

class ApplicationSettings():

    def __init__(self, fromDate = None, toDate = None, minHours = None, cid = None):
        self.fromDate = fromDate
        self.toDate = toDate
        self.minHours = minHours
        self.cid = cid

    def setDates(self):
        happy = False

        while not happy:

            self.fromDate = self.parseDate("Enter the date you want to measure from in format 'yyyy-mm-dd': ")
            self.toDate = self.parseDate("Enter the date you want to measure to in format 'yyyy-mm-dd': ")

            if self.toDate <= self.fromDate:
                print("The date you want to measure to cannot be earlier than the date you want to measure from.")
            else:
                happy = True

        print(f"Date range changed to measure from {self.fromDate} to {self.toDate}.")

        return parser.isoparse(self.fromDate), parser.isoparse(self.toDate)


    def parseDate(self, question):
        happy = False
        while not happy:

            measureDate = input(question)
            year, month, day = measureDate.split("-")
            try:
                datetime.datetime(int(year), int(month), int(day))
                happy = True
            except:
                print("Date is not valid.")
                happy = False

        return measureDate

    def getMinHours(self):
        try:
            self.minHours = int(input("Enter minimum required hours: "))
            return self.minHours
        except:
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
            "From date": self.fromDate,
            "To date": self.toDate,
            "Min hours": self.minHours
        }