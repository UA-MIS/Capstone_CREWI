from flask import abort
import datetime
import DfaDatabase
import printFormatting
import Status

class RecommendationRequest:
    def __init__(self, userRequest):
        #if the user's request is in the right format, it'll make the rec request object
        try:
            self.username = userRequest["username"]
            
            # if time is missing, proceed without it; this happens if the provided timeslot scenario
            if userRequest["time"] != "":
                self.time = datetime.datetime.strptime(userRequest["time"], '%Y-%m-%d %H:%M:%S')
            else:
                self.time = ""

            self.timeSlot = userRequest["timeSlot"]
            self.location = userRequest["location"]

            dfaDatabase = DfaDatabase.DfaDatabase()

            # status array contains the various notifiers from the process; like bad username, missing location, etc.
            # this must happen before the lookups because they may add statuses
            self.statusArray = []

            # the request will start without user and store ID; these will be looked up in the engine functions
            self.userId = dfaDatabase.lookupUser(self)
            self.storeId = dfaDatabase.lookupStore(self)
        except Exception as e:
            Status.statusArray.append("test")
            print(e)
            # print issue to terminal and return 400 to requester
            print("400 ERROR: Invalid request body formatting")
            # abort(400, "400 ERROR: Invalid request body formatting")