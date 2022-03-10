from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from flask_cors import CORS
import DfaDatabase
from Models import RecommendationRequest, RecommendationEngine
from Models import Store

import os
import globalStatus
import printFormatting
import sys
import traceback

# initializes the Flask app
app = Flask(__name__)

CORS(app)

#specifying the route and methods allowed; I think we'll just do GET, maybe something for logging in?
@app.route('/hello/', methods=['GET', 'POST'])
#I don't think the name of the function matters? I have no clue tbh, I guess they don't matter in .NET either...
def welcome():
    return "update"

@app.route('/recommendation/', methods=['POST'])
def recommendItem():
    printFormatting.printSuccess("Recommendation request received")
    
    # this is the global status array; it needs to be in this scope in case making the request fails
    # do not initialize it again, the Status object is basically a singleton
    globalStatus.init()
    printFormatting.printSuccess("Engine status initialized")

    try:
        # need to load environment variables for remainder use later
        load_dotenv()

        # request.json will contain the request body; this saves it into a RecommendationRequest object
        userRequest = RecommendationRequest.RecommendationRequest(request.json)

        # making the engine; these are functionally static methods but I figured instance methods would be a little clearer
        engine = RecommendationEngine.RecommendationEngine()
        
        # making database object
        db = DfaDatabase.DfaDatabase()

        # finding closest store ID
        stores = db.loadStores()

        engine.calculateDistances(stores, userRequest)        

        closestLocation = stores[0]
        recentLocation = Store.Store(0, "", float(0), float(0))

        recentStoreId = db.lookupRecentStore(userRequest)

        for store in stores:
            if store.id == recentStoreId:
                recentLocation = store
        
        bestAddress = ""

        if (closestLocation.address == recentLocation.address):
            bestAddress = closestLocation.address

        # setting the time slot; even if its provided, this will confirm it (so if there's a logical conflict time will be prioritized)
        userRequest.timeSlot = engine.parseRequestTime(userRequest)
        
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
        engine.scoreTransactions(transactions, userRequest)

        # initializing item array
        items = []
        
        # this will return items with ID and scores, sorted from highest to lowest score (items[0] is the top recommendation)
        items = engine.aggregateScores(transactions)

        # removing the lower scoring items; the remaining items will be returned as the recommendations
        items = items[:int(os.environ.get('Recommendation_Count'))]

        # this will modify the items directly by adding their URLs and scores
        db.lookupItems(items)

        # returns the statuses and recommendations; recommendations[0] will be the top recommendation
        return jsonify({
            "statuses": globalStatus.statusArray,
            "recommendations": [item.__dict__ for item in items],
            "locations": {
                "bestLocation": bestAddress,
                "closestLocation": closestLocation.address,
                "recentLocation": recentLocation.address
            }
        })
    # if any full failures occur during the recommendation process, print the error and return the status array and default rec for the widget
    except Exception as e:
        # global fail refers to something in the over-arching try/except failing; add it and print the issue
        globalStatus.addFail("GLOBAL_FAIL")
        printFormatting.printError(str(e))
        # prints out all the fails from the engine
        printFormatting.printFinalStatus(globalStatus.statusArray)
        printFormatting.printError(traceback.format_exc())
        # return the status array and back-up/default recommendation; this uses the same format for easier handling on the front-end
        # however, recommendations will just be an array with the single default recommendation
        # the values come from the configuration file rather than attempting to access the database since that's a likely cause of failure
        return jsonify({
            "statuses": globalStatus.statusArray,
            "items": [{
                "id": int(os.environ.get('Default_Recommendation_ID')),
                "imgUrl": os.environ.get('Default_Recommendation_ImageURL'),
                "name": os.environ.get('Default_Recommendation_Name'),
                "score": int(os.environ.get('Default_Recommendation_Score'))
            }],
            "bestLocation": "BEST LOC",
            "closestLocation": "CLOSEST LOC",
            "recentLocation": "RECENT LOC"
        })

#from the article "This line ensures that our Flask app runs only when it is executed in the main file and not when it is imported in some other file"
#gonna be honest idk what that means in a practical sense, but we can look into it more if we can get issues when hosting, might come up for file structure too
if __name__ == '__main__':
    #eventually host will be updated to our hosting service URL, can change port as needed
    app.run(host='0.0.0.0', port=8000)
