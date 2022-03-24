import datetime
from ..Functions import printFormatting
from ..Functions import globalStatus

# RECOMMENDATIONREQUEST.PY: Class for holding request data, this is just a constructor

class RecommendationRequest:
    # constructor takes in "userRequest", which is the JSON object that came from the POST request body; also takes a db so that it can look up the user ID
    def __init__(self, userRequest, db):
        #if the user's request is in the right format, it'll make the rec request object
        try:
            self.username = userRequest["username"]
            
            # if time is missing, proceed without it; this happens if the provided timeslot scenario
            if userRequest["time"] != "":
                self.time = datetime.datetime.strptime(userRequest["time"], '%Y-%m-%d %H:%M:%S')
            else:
                printFormatting.printWarning("Initializing request without time")
                globalStatus.addIssue("MISSING_TIME_ISSUE")

                self.time = ""

            self.timeSlot = userRequest["timeSlot"]
            
            # if coordinates are missing, go on without them but flag it as an issue (recommending closest will fail)
            try:
                self.latitude = userRequest["latitude"]
                self.longitude = userRequest["longitude"]
            except:
                printFormatting.printWarning("Proceeding without user coordinates")
                globalStatus.addIssue("MISSING_COORDINATES_ISSUE")

            # attempts to find user ID immediately based off of username
            self.userId = db.lookupUser(self)
            printFormatting.printSuccess("Request parsed successfully")
        except Exception as e:
            # printing issue and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("REQUEST_INIT_FAIL")
            raise e