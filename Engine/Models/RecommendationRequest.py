from flask import abort

class RecommendationRequest:
    def __init__(self, userRequest):
        #if the user's request is in the right format, it'll make the rec request object
        try:
            self.username = userRequest["username"]
            self.time = userRequest["time"]
            self.timeSlot = userRequest["timeSlot"]
            self.location = userRequest["location"]
        except:
            # print issue to terminal and return 400 to requester
            print("400 ERROR: Invalid request body formatting")
            abort(400, "400 ERROR: Invalid request body formatting")