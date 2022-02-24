from datetime import datetime
from flask import abort
import os
import printFormatting

class RecommendationEngine:
    # this takes in a request and returns the time slot
    def parseRequestTime(self, userRequest):
        try:
            # if time is blank, return the timeslot if given or the default if it's also missing
            if userRequest.time == "":
                if userRequest.timeSlot != "":
                    return userRequest.timeSlot
                else:
                    return os.environ.get('Default_TimeSlot')

            # in effect, this will prioritize the time over the provided time slot if they were not related appropriately
            # this grabs the time from the request
            time = userRequest.time.time()

            # loading in the boundary times based on the .env file
            morningTime = datetime.strptime(os.environ.get('Morning_Time'), '%H:%M:%S').time()
            afternoonTime = datetime.strptime(os.environ.get('Afternoon_Time'), '%H:%M:%S').time()
            nightTime = datetime.strptime(os.environ.get('Night_Time'), '%H:%M:%S').time()

            # this should work in general, but it does presume 3 timezones and that night contains the midnight cutoff
            if time > morningTime and time <= afternoonTime:
                return 'Morning'
            elif time > afternoonTime and time <= nightTime:
                return 'Afternoon'
            elif time > nightTime or time <= morningTime:
                return 'Night'
            # this should basically never fire, but just in case return the default timeslot
            else:
                return os.environ.get('Default_TimeSlot')
        except:
            # print issue to terminal and return 500 to requester
            printFormatting.printError("Failed to parse request time into time slot")
            abort(500, "500 ERROR: Failed to parse request time into time slot")