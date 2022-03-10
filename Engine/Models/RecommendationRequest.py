from flask import abort
import datetime
import DfaDatabase
import printFormatting
import globalStatus

class RecommendationRequest:
    def __init__(self, userRequest):
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

            dfaDatabase = DfaDatabase.DfaDatabase()

            self.userId = dfaDatabase.lookupUser(self)
            printFormatting.printSuccess("Request parsed successfully")
        except Exception as e:
            # printing issue and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("REQUEST_INIT_FAIL")
            raise e