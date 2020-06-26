import datetime
import json
import urllib.request
import string


def grabData(id):
    try:

        userURL = ("https://api.vatsim.net/api/ratings/%s/connections/" % id)
        userRequest = urllib.request.Request(userURL, headers={'User-Agent': 'Mozilla/5.0'})
        userHTML = urllib.request.urlopen(userRequest)
        respondeCode = userHTML.getcode()
        jsonResponse = userHTML.read()

        print(jsonResponse)

    except:

        print("An error occurred trying to get the user's info!")


def getDetails(mode):
    userCID = getCID()
    measureDate = getMeasureData()
    dateNow = datetime.date.today()
    if mode == "debug":
        print(userCID)
        print(measureDate)
        print(dateNow)

    return userCID, measureDate, dateNow


def getCID():
    happy = False
    while not happy:
        userCID = input("Please enter your CID: ")
        if userCID == "":
            print("CID not valid...")
        else:
            return userCID


def getMeasureData():
    happy = False
    while not happy:

        measureDate = input("Enter the date in format 'yyyy-mm-dd': ")
        year, month, day = measureDate.split("-")
        try:
            datetime.datetime(int(year), int(month), int(day))
            happy = True
        except:
            print("Date is not valid.")
            happy = False

    return measureDate


userCID, measureDate, dateNow = getDetails("debug")
grabData(userCID)

