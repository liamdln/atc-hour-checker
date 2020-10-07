from Menu import Menu
from ApplicationSettings import ApplicationSettings

print("""VATSIM ATC Hour Checker v2
By Liam Pickering - 1443704""")

satisfied = False
running = True

_validAnswers = ["a", "b", "c", "d", "e", "f"]
mainMenu = Menu(_validAnswers)
menuOption = None

settings = ApplicationSettings()

while running:

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
        if settings.fromDate is not None and settings.toDate is not None and settings.minHours is not None:




            userCID = getCID()
            print("""
        Searching for {0}'s hours between {1} and {2}.
        The hour requirement is set at: {3}""".format(userCID, str(fromDate), str(toDate), minHours))

            apiURL = f"https://api.vatsim.net/api/ratings/{userCID}/connections/"
            grabData(apiURL, fromDate, toDate, searchAirports, searchPositions)

            print(f"\nController hours: {_totalHours}.")
        else:
            print("\nYou have not setup either: \n1) The dates.\n2. The minimum hours.")
    elif menuOption == "b":
        fromDate, toDate = settings.setDates()
    elif menuOption == "c":
        minHours = settings.getMinHours()
    elif menuOption == "d":
        print("Not implimented.")
    elif menuOption == "e":
        print(settings.wipeSettings())
    elif menuOption == "f":
        appSettings = settings.listSettings()
        for setting in appSettings:
            print(f"{setting}: {appSettings[setting]}")
