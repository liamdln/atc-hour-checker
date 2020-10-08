import dateutil
import json
import requests

class ApiRequestor:

    def __init__(self, cid, airports, positions):
        self.cid = cid
        self.airports = airports
        self.positions = positions

    def makeHttpGet(self, vatsimApiLink):
        userUrl = self.buildApiUrl(vatsimApiLink)
        # print(f"Making request to {userUrl}")
        response = requests.get(userUrl)
        if response:
            if response.status_code == 200:
                data = json.loads(response.content)
                return data
            elif response.status_code == 404:
                return "CID not found."
            # more response codes here

        else:
            return "An error occurred getting the response\n"

    def buildApiUrl(self, apiBase):
        if apiBase.__contains__("?page="):
            return apiBase
        apiRoute = f"/ratings/{self.cid}/atcsessions"
        return f"{apiBase}{apiRoute}"

    def makeRequest(self, vatsimApiLink, tailDate, headDate, totalHours=0):
        try:
            data = self.makeHttpGet(vatsimApiLink)
        except ConnectionError:
            return "An error occurred and your request could not be completed"

        sessions = data["results"]
        nextPage = data["next"]
        startDate = None

        counter = 0

        for session in sessions:
            if session["end"] is not None:
                airport, position = self.getCallsignAndPos(session["callsign"])
                startDate = dateutil.parser.isoparse(session["start"].split("T")[0])
                if tailDate <= startDate <= headDate and airport is not "":
                    # > = earlier than; < = later than
                    if airport in self.airports and position in self.positions:
                        connectionHours = 0
                        try:
                            connectionHours = float(session["minutes_on_callsign"])
                        except:
                            print("An error occurred converting hours to a number. Recorded as 0")
                        totalHours += (connectionHours / 60)

            counter += 1

        try:
            if counter == len(sessions) and startDate > tailDate:
                return self.makeRequest(nextPage, tailDate, headDate, totalHours)
        except ConnectionError:
            return "An error occurred trying to check a different page of the user's sessions"

        return totalHours

    @staticmethod
    def getCallsignAndPos(callsign):
        facility = callsign.split("_")
        if len(facility) > 2:
            del facility[1]
        elif len(facility) < 2:
            return "", ""
        return facility[0], facility[1]
