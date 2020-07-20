import datetime
import json
import urllib.request
import string
import dateutil
import dateutil.parser
import csv
from datetime import timedelta

_totalHours = datetime.timedelta(hours=0)


def grabData(userURL, backPointer, frontPointer, airports, positions):
    try:

        global _totalHours

        userRequest = urllib.request.Request(userURL, headers={'User-Agent': 'Mozilla/5.0'})
        userHTML = urllib.request.urlopen(userRequest)
        respondeCode = userHTML.getcode()
        jsonResponse = userHTML.read()

        data = json.loads(jsonResponse)
        sessions = data["results"]
        nextPage = data["next"]

        counter = 0

        for session in sessions:
            if session["end"] is not None:
                id = session["id"]
                airport, position = getCallsignAndPos(session["callsign"])
                startDate = dateutil.parser.isoparse(session["start"])
                if backPointer <= startDate <= frontPointer and airport is not "":
                    # > = earlier than; < = later than
                    if airport in airports and position in positions:
                        endDate = dateutil.parser.isoparse(session["end"])
                        connectionHours = endDate - startDate
                        _totalHours += connectionHours

            counter += 1
            if counter == len(sessions) and startDate > backPointer:
                grabData(nextPage, backPointer, frontPointer, airports, positions)

    except:

        print("""An error occurred trying to get the user's info!
Reasons for this:
1. The CID is incorrect.
2. You are not connected to the internet, or the VATSIM API is down.""")


def getCallsignAndPos(callsign):
    facility = callsign.split("_")
    if len(facility) > 2:
        del facility[1]
    elif len(facility) < 2:
        return "", ""

    # print(facility[0])
    # print(facility[1])

    return facility[0], facility[1]


def getDetails(mode):
    happy = False

    while not happy:

        fromDate = getDate("Enter the date you want to measure from in format 'yyyy-mm-dd': ")
        toDate = getDate("Enter the date you want to measure to in format 'yyyy-mm-dd': ")

        if (toDate <= fromDate):
            print("The date you want to measure to cannot be earlier than the date you want to measure from.")
        else:
            happy = True

    # debugging
    if mode == "debug":
        print(userCID)
        print(fromDate)
        print(toDate)

    print("""Dates changed to {0} (from date) and {1} (to date).""".format(str(fromDate), str(toDate)))

    return dateutil.parser.isoparse(fromDate), dateutil.parser.isoparse(toDate)


def getCID():
    happy = False
    while not happy:
        userCID = input("Please enter your CID: ")
        if userCID == "":
            print("CID not valid...")
        else:
            return userCID


def getDate(question):
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


def changeMinHours():
    minHours = int(input("Enter minimum required hours: "))
    print("Minimum hour requirement now set to: {0}".format(minHours))
    return minHours


def editStations():
    print("""You are entering stations. Please read this is VERY important.
Please enter the station ICAOs first, for example OMDB, OTHH, OBBB, OJAC.
Then you will be asked to enter the positions, for example TWR, CTR, APP.
Once you have finished with each, write 'x' to stop.""")

    correctData = False

    while not correctData:
        searchAirports = getStations("Enter station ICAO ('x' to stop): ")
        goodData = input("Is this correct? (y/n): ")
        if goodData.lower() == "y":
            correctData = True
        else:
            print("Okay let's try again...\n")

    correctData = False

    while not correctData:
        searchPositions = getStations("Enter the position ('x' to stop): ")
        goodData = input("Is this correct? (y/n): ")
        if goodData.lower() == "y":
            correctData = True
        else:
            print("Okay let's try again...\n")

    print("Airports entered:")
    for element in searchAirports:
        print(element)

    print("Positions entered:")
    for element in searchPositions:
        print(element)

    return searchAirports, searchPositions


def getStations(message):
    data = []
    takingData = True
    while takingData:
        itemToAppend = (input(message))
        if itemToAppend is not "x":
            data.append(itemToAppend.upper())
        else:
            data = filter(None, data)
            print("Data entered:")
            for element in data:
                print(element)
            takingData = False

    return data


def main():
    global _totalHours

    searchPositions = ["DEL", "GND", "TWR", "APP", "CTR", "FSS"]
    #searchAirports = ["OTHH", "OTBD", "OBBI", "DOH", "OBBB"] #bahrain
    searchAirports = ["OMDB", "OMSJ", "OMDW", "OMAA", "OMDM"] #uae

    _totalHours = None

    # minHours = None
    # fromDate = None
    # toDate = None

    fromDate = dateutil.parser.isoparse("2020-05-01T00:00:00")
    toDate = dateutil.parser.isoparse("2020-07-20T00:00:00")
    minHours = 6

    happy = False
    while not happy:
        _totalHours = datetime.timedelta(hours=0)

        print("""\nPlease choose an option:
    a) Search user.
    b) Enter search dates.
    c) Change minimum hours.
    d) Enter airport positions.
    e) Wipe settings.""")

        userChoice = input("Enter choice (a, b, c, d or e): ")

        if userChoice.lower() == "a":
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
        elif userChoice.lower() == "b":
            fromDate, toDate = getDetails("")
        elif userChoice.lower() == "c":
            print("Not functional.")
            # minHours = changeMinHours()
        elif userChoice.lower() == "d":
            searchPositions, searchAirports = editStations()
        elif userChoice.lower() == "e":
            print("Not functional.")
        else:
            print("That is not a valid entry... Try again.")


print("""VATSIM ATC Hour Checker v1.0
By Liam Pickering - 1443704""")

main()
