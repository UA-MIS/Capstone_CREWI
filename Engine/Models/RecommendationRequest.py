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
            self.location = userRequest["location"]

            dfaDatabase = DfaDatabase.DfaDatabase()

            # the request will start without user and store ID; these will be looked up in the engine functions
            self.userId = dfaDatabase.lookupUser(self)
            self.storeId = dfaDatabase.lookupStore(self)
            printFormatting.printSuccess("Request parsed successfully")
        except Exception as e:
            # printing issue and updating status
            printFormatting.printError(str(e))
            globalStatus.addFail("REQUEST_INIT_FAIL")
            raise e