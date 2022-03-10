from datetime import datetime
from dotenv import load_dotenv
from flask import abort
from math import radians, cos, sin, asin, sqrt
import os
import printFormatting
import globalStatus
from Models import Item

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

            printFormatting.printSuccess("Time parsed successfully")
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

    # takes in the transactions and request; this modifies the transactions directly so no return is needed
    def scoreTransactions(self, transactions, request):
        try:
            # loading environment data
            load_dotenv()

            # loops through all the transactions
            for index, transaction in enumerate(transactions):
                # transactions start with a score of a / (index + 1); a is configurable
                transaction.score = float(float(os.environ.get('Numerator_Constant')) / (index + 1))
                # after getting a base score, they all get a flat constant to reduce the importance of the base score (also configurable)
                transaction.score += float(os.environ.get('Addition_Constant'))

                # if the transaction does not match the request user, reduce the score by a "reducer" (just a multiplier that is less than 1, not a technical term; configurable)
                if transaction.userId != request.userId : transaction.score *= float(os.environ.get('Other_User_Reducer'))

            printFormatting.printSuccess("Scored transactions")
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("SCORE_TRANSACTION_FAIL")
            raise e

    # takes in the stores and request; this modifies the stores directly so no return is needed
    def calculateDistances(self, stores, request):
        try:
            # loading environment data
            load_dotenv()

            # loops through all the transactions
            for store in stores:
                requestLat = radians(request.latitude)
                storeLat = radians(store.latitude)
                requestLon = radians(request.longitude)
                storeLon = radians(store.longitude)
                
                dLon = requestLon - storeLon
                dLat = requestLat - storeLat
                a = sin(dLat / 2)**2 + cos(requestLat) * cos(storeLat) * sin(dLon / 2)**2

                c = 2 * asin(sqrt(a))

                # miles , use 6371 for kilometers
                r = 3956

                store.distance = c * r

            # sort the items by score; the recommendation will be items[0] after this
            stores.sort(key=lambda x: 1*x.distance)

            printFormatting.printSuccess("Calculated distances")
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("SCORE_TRANSACTION_FAIL")
            raise e


    # this takes in the scored transactions and returns an array of items with their scores aggregated
    # this is just control break logic
    def aggregateScores(self, transactions):
        try:
            # making item array
            items = []
            
            # sorting transactions by itemId
            transactions.sort(key=lambda x: x.itemId)

            # grabbing the first item ID and starting its score at 0
            currentItemId = transactions[0].itemId
            currentItemScore = 0

            # loop through all the transactions
            for transaction in transactions:
                # if the current item matches the item ID, add its score to the item's total score
                if (transaction.itemId == currentItemId):
                    currentItemScore += transaction.score
                # if the ID doesn't match, add the prior item to the array and start tracking the next item's ID and score
                else:
                    items.append(Item.Item(currentItemId, "", "", currentItemScore))
                    currentItemId = transaction.itemId
                    currentItemScore = transaction.score

            # add the last item to the array of items
            items.append(Item.Item(currentItemId, "", "", currentItemScore))

            # sort the items by score; the recommendation will be items[0] after this
            items.sort(key=lambda x: -1*x.score)

            printFormatting.printSuccess("Aggregated item scores")
            # return the items: they have their IDs and scores, but still need name/image URL
            return items
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("AGGREGRATE_SCORES_FAIL")
            raise e