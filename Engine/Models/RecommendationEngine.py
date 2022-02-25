from datetime import datetime
from dotenv import load_dotenv
from flask import abort
import os
import printFormatting
import globalStatus

class RecommendationEngine:
    # this takes in a request and returns the time slot
    def parseRequestTime(self, userRequest):
        try:
            # if time is blank, return the timeslot if given or the default if it's also missing
            if userRequest.time == "":

                printFormatting.printWarning("Time is missing from request")
                globalStatus.addIssue("MISSING_TIME_ISSUE")
                
                if userRequest.timeSlot != "":
                    return userRequest.timeSlot
                else:
                
                    printFormatting.printWarning("Time and time slot are missing from request, using default time slot")
                    globalStatus.addIssue("MISSING_TIME_AND_TIMESLOT_ISSUE")
                
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
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("PARSE_TIME_FAIL")            
            raise e

    def scoreTransactions(self, transactions, request):
        try:
            load_dotenv()

            for index, transaction in enumerate(transactions):
                transaction.score = float(float(os.environ.get('Numerator_Constant')) / (index + 1))
                transaction.score += float(os.environ.get('Addition_Constant'))

                if transaction.userId != request.userId : transaction.score *= float(os.environ.get('Other_User_Reducer'))
                if transaction.storeId == request.storeId : transaction.score *= float(os.environ.get('Matching_Store_Multiplier'))


        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("SCORE_TRANSACTION_FAIL")
            raise e
