import urllib

import dateutil


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
