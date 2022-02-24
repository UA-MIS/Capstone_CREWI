from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from flask_cors import CORS
import DfaDatabase
from Models import RecommendationRequest, RecommendationEngine

import os
import Status
import printFormatting

status = []

# initializes the Flask app
app = Flask(__name__)

CORS(app)

#specifying the route and methods allowed; I think we'll just do GET, maybe something for logging in?
@app.route('/hello/', methods=['GET', 'POST'])
#I don't think the name of the function matters? I have no clue tbh, I guess they don't matter in .NET either...
def welcome():
    return "update"


def breakingFunction():
    try:
        raise Exception("Date provided can't be in the past")
    except:
        abort(400)

@app.route('/recommendation/', methods=['POST'])
def recommendItem():
    # this is the global status array; it needs to be in this scope in case making the request fails
    # do not initialize it again, the Status object is basically a singleton
    Status.init()

    try:
        # need to load environment variables for remainder use later
        load_dotenv()

        # request.json will contain the request body; this saves it into a RecommendationRequest object
        # will return a 400 if the request body formatting is bad
        userRequest = RecommendationRequest.RecommendationRequest(request.json)
        
        # making the engine; these are functionally static methods I figured instance methods would be a little clearer
        engine = RecommendationEngine.RecommendationEngine()
        
        # setting the time slot; even if its provided, this will confirm it (so if there's a logical conflict time will be prioritized)
        userRequest.timeSlot = engine.parseRequestTime(userRequest)

        # making database object
        db = DfaDatabase.DfaDatabase()
        
        # making empty transaction array
        transactions = []
        
        # start with transactions from the current user that match day part
        transactions = db.loadUserTransactions(userRequest)

        # calculating the remainder: the total number to use minus the number that matched the user
        remainder = int(os.environ.get('Transaction_Count')) - len(transactions)

        # adding the non-user transactions to the user ones; loadOtherTransactions takes in the remainder to pull the right number
        # at this point, transactions contains ordered transactions from the user, then ordered from other users, all matching day part
        transactions.extend(db.loadOtherTransactions(userRequest, remainder))
        # abort(500, "test")
        # just for testing purposes; at the end, this will just return the rec
        return jsonify({
            "request": {
                "username": userRequest.username,
                "userId": userRequest.userId,
                "time": userRequest.time,
                "timeSlot": userRequest.timeSlot,
                "location": userRequest.location,
                "status": userRequest.statusArray
            },
            "database": {
                "host": os.environ.get('DFA_HOST'),
                "username": os.environ.get('DFA_Username'),
                "password": os.environ.get('DFA_Password'),
                "database": os.environ.get('DFA_Database')
            }
        })
    # if any full failures occur during the recommendation process, print the error and return the status array and default rec for the widget
    except Exception as e:
        # global fail refers to something in the over-arching try/except failing; add it and print the issue
        Status.addFail("GLOBAL_FAIL")
        printFormatting.printError(str(e))
        # prints out all the fails from the engine
        printFormatting.printFinalFails(Status.statusArray)
        # return the status array and back-up/default recommendation
        return jsonify({
            "status": Status.statusArray,
            "defaultRec": "change this later"
        })

#from the article "This line ensures that our Flask app runs only when it is executed in the main file and not when it is imported in some other file"
#gonna be honest idk what that means in a practical sense, but we can look into it more if we can get issues when hosting, might come up for file structure too
if __name__ == '__main__':
    #eventually host will be updated to our hosting service URL, can change port as needed
    app.run(host='0.0.0.0', port=8000)
