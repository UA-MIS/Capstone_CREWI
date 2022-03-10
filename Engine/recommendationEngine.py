from datetime import datetime
from dotenv import load_dotenv
from flask import abort
from math import radians, cos, sin, asin, sqrt
import os
import printFormatting
import globalStatus
from Models import Item


def recommendClosestLocation(userRequest, db):
    try:
        # need to load environment variables for remainder use later
        load_dotenv()

        # loading all the stores
        stores = db.loadStores()

        # assigning each store its distance from the user; returns the list sorted from nearest to farthest
        calculateDistances(stores, userRequest)        

        # closest store is the first one in the array; making a blank store for recent location
        return stores[0].address
    except Exception as e:
        # if recommendation fails, use "" as the default value and print the issue; do not raise the exception since the engine should proceed
        printFormatting.printError(str(e))
        globalStatus.addFail("RECOMMEND_CLOSEST_FAIL")
        return ""

def recommendRecentLocation(userRequest, db):
    try:
        # need to load environment variables for remainder use later
        load_dotenv()

        # finding the most recent store's ID using the user ID from the request
        recentStoreId = db.lookupRecentStore(userRequest)

        # if the store ID is 0, that means the user or transactions weren't found; log the error and skip the lookup
        if recentStoreId == 0:
            printFormatting.printWarning("Unable to find a store for the user's most recent transaction")
            globalStatus.addFail("RECOMMEND_RECENT_FAIL")
            return ""

        # this method returns the address of the given store ID, so it can be returned directly
        return db.lookupStoreId(recentStoreId)
    except Exception as e:
        # if recommendation fails, use "" as the default value and print the issue; do not raise the exception since the engine should proceed
        printFormatting.printError(str(e))
        globalStatus.addFail("RECOMMEND_RECENT_FAIL")        
        return ""

def determineBestLocation(closestLocation, recentLocation):
    try:
        # if the locations match, return that; otherwise, return a blank
        if closestLocation == recentLocation: return closestLocation
        return ""
    except Exception as e:
        # there's no way this ever throws an exception, but just to be safe it would return a blank
        printFormatting.printError(str(e))
        globalStatus.addFail("RECOMMEND_BEST_FAIL")        
        return ""

def recommendItems(userRequest, db):
    try:

        # setting the time slot; even if its provided, this will confirm it (so if there's a logical conflict time will be prioritized)
        userRequest.timeSlot = parseRequestTime(userRequest)
        
        # making empty transaction array
        transactions = []
        
        # start with transactions from the current user that match day part
        transactions = db.loadUserTransactions(userRequest)

        # calculating the remainder: the total number to use minus the number that matched the user
        remainder = int(os.environ.get('Transaction_Count')) - len(transactions)

        # adding the non-user transactions to the user ones; loadOtherTransactions takes in the remainder to pull the right number
        # at this point, transactions contains ordered transactions from the user, then ordered from other users, all matching day part
        transactions.extend(db.loadOtherTransactions(userRequest, remainder))

        # if fewer than preferred transactions were loaded (because not enough were in the time slot), add an issue
        if (len(transactions) < int(os.environ.get('Transaction_Count'))):
            printFormatting.printWarning("Using fewer transactions than requested in configuration")
            globalStatus.addIssue("INSUFFICIENT_TRANSACTIONS_ISSUE")

        if len(transactions) == 0:
            printFormatting.printError("No transactions found; cannot proceed with analysis")
            globalStatus.addFail("ZERO_TRANSACTIONS_FAIL")
            raise Exception("No transactions found; cannot proceed with analysis")

        # scoring the transactions; this is pass by reference so nothing is returned, the transactions are directly updated
        scoreTransactions(transactions, userRequest)

        # initializing item array
        items = []
        
        # this will return items with ID and scores, sorted from highest to lowest score (items[0] is the top recommendation)
        items = aggregateScores(transactions)

        # removing the lower scoring items; the remaining items will be returned as the recommendations
        items = items[:int(os.environ.get('Recommendation_Count'))]

        # this will modify the items directly by adding their URLs and scores
        db.lookupItems(items)

        return items
    except Exception as e:
        # if recommending items fails, use the default recommendation
        printFormatting.printError(str(e))
        globalStatus.addFail("RECOMMEND_ITEMS_FAIL")
        # making a one item array with the default item
        return [Item.Item(
            int(os.environ.get('Default_Recommendation_ID')),
            os.environ.get('Default_Recommendation_Name'),
            os.environ.get('Default_Recommendation_ImageURL'),
            int(os.environ.get('Default_Recommendation_Score'))
        )]


# this takes in a request and returns the time slot
def parseRequestTime(userRequest):
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
def scoreTransactions(transactions, request):
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
def calculateDistances(stores, request):
    try:
        # loading environment data
        load_dotenv()

        # loops through all the stores and assigns each its distance
        # it uses a Haversine formula, pulled this code from: https://www.geeksforgeeks.org/haversine-formula-to-find-distance-between-two-points-on-a-sphere/
        for store in stores:
            # converting coordinates to radians
            requestLat = radians(request.latitude)
            storeLat = radians(store.latitude)
            requestLon = radians(request.longitude)
            storeLon = radians(store.longitude)
            
            # finding differences in longitude and latitude
            dLon = requestLon - storeLon
            dLat = requestLat - storeLat
            
            # this is how the math is done... refer to a Haversine formula for details
            # summarized answer is that it finds the distance between points on a globe
            a = sin(dLat / 2)**2 + cos(requestLat) * cos(storeLat) * sin(dLon / 2)**2
            c = 2 * asin(sqrt(a))

            # converting whatever units c is in to miles, use 6371 for kilometers
            r = 3956

            # the stores will have the linear distance in miles from the user; this is just literally distance, not based on traffic/roads/etc.
            store.distance = c * r

        # sort the stores by distance; stores[0] will be the nearest store after this
        stores.sort(key=lambda x: 1*x.distance)
        printFormatting.printSuccess("Calculated distances")
    except Exception as e:
        # print issue to terminal and update status
        printFormatting.printError(str(e))
        globalStatus.addFail("CALCULATE_DISTANCES_FAIL")
        raise e


# this takes in the scored transactions and returns an array of items with their scores aggregated
# this is just control break logic
def aggregateScores(transactions):
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