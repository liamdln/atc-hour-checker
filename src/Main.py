import dateutil
from HourCount import Menu, ApplicationSettings
from ApiHandler import ApiRequestor

print("""VATSIM ATC Hour Checker v2
By Liam Pickering - 1443704""")

satisfied = False
running = True

_validAnswers = ["a", "b", "c", "d", "e", "f"]
mainMenu = Menu(_validAnswers)
settings = ApplicationSettings()
menuOption = None

vatsimBaseUrl = "https://api.vatsim.net/api"

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
        if settings.fromDate is None and settings.toDate is None:
            print("The dates have not been entered. Please choose option b) to enter the dates.")
        elif settings.minHours is None:
            print("The minimum hours have not been specified. Please choose option c) to enter the minimum hour requirement.")
        elif settings.airportsToSearch is None or settings.positionsToSearch is None:
            print("The airports or positions have not been specified. Please choose option d) to enter the airports and positions you want to search.")
        else:
            appSettings = settings.listSettings()
            if appSettings["cid"] is None:
                settings.setCid(input("Enter the user's CID: "))

            print(f"""Searching for {appSettings["cid"]}'s hours between {appSettings["from-date"]} and {appSettings["to-date"]}.\nThe hour requirement is set at: {appSettings["min-hours"]}""")

            request = ApiRequestor(appSettings["cid"], appSettings["airports"], appSettings["positions"])
            totalHours = request.makeRequest(vatsimBaseUrl, dateutil.parser.isoparse(appSettings["from-date"]), dateutil.parser.isoparse(appSettings["to-date"]))

            print(f"\nController hours: {totalHours}.")
    elif menuOption == "b":
        fromDate, toDate = settings.setDates()
    elif menuOption == "c":
        minHours = settings.getMinHours()
    elif menuOption == "d":
        settings.editStations()
    elif menuOption == "e":
        print(settings.wipeSettings())
    elif menuOption == "f":
        appSettings = settings.listSettings()
        for setting in appSettings:
            print(f"{setting}: {appSettings[setting]}")
