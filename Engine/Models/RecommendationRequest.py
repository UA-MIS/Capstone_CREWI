from flask import abort
import datetime

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
        except:
            # print issue to terminal and return 400 to requester
            print("400 ERROR: Invalid request body formatting")
            abort(400, "400 ERROR: Invalid request body formatting")