from Menu import Menu
from DateHandler import getDetails

print("""VATSIM ATC Hour Checker v2
By Liam Pickering - 1443704""")

satisfied = False
running = True

mainMenu = Menu()
menuOption = None

while running:

    fromDate = None
    toDate = None
    minHours = None

    mainMenu.displayMenu()

    while not satisfied:
        menuOption = mainMenu.getMenuUserChoice()
        if not mainMenu.validateUserChoice(menuOption):
            print("Invalid entry.")
            mainMenu.displayMenu()
        else:
            satisfied = True

    satisfied = False
    if menuOption == "a":
        if fromDate is not None and toDate is not None and minHours is not None:
            userCID = getCID()
            print("""
        Searching for {0}'s hours between {1} and {2}.
        The hour requirement is set at: {3}""".format(userCID, str(fromDate), str(toDate), minHours))

            apiURL = "https://api.vatsim.net/api/ratings/%s/connections/" % userCID
            grabData(apiURL, fromDate, toDate, searchAirports, searchPositions)

            print("\nController hours: {0}".format(_totalHours))
        else:
            print("You have not setup either: \n1) The dates.\n2. The minimum hours.")
    elif menuOption == "b":
        fromDate, toDate = getDetails()
