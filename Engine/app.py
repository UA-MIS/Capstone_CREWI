from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import DfaDatabase
from Models import RecommendationRequest, RecommendationEngine

import os
import json

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
    load_dotenv()

    # request.json will contain the request body; this saves it into a RecommendationRequest object
    # will return a 400 if the request body formatting is bad
    userRequest = RecommendationRequest.RecommendationRequest(request.json)
    
    # making the engine; these are functionally static methods I figured instance methods would be a little clearer
    engine = RecommendationEngine.RecommendationEngine()
    
    # setting the time slot; even if its provided, this will confirm it (so if there's a logical conflict time will be prioritized)
    userRequest.timeSlot = engine.parseRequestTime(userRequest)


    db = DfaDatabase.DfaDatabase()
    
    transactions = []
    
    transactions = db.loadUserTransactions(userRequest)
    remainder = int(os.environ.get('Transaction_Count')) - len(transactions)
    print(remainder)
    transactions.extend(db.loadOtherTransactions(userRequest, remainder))
    
    # just for testing purposes; at the end, this will just return the rec
    return jsonify({
        "request": {
            "username": userRequest.username,
            "userId": userRequest.userId,
            "time": userRequest.time,
            "timeSlot": userRequest.timeSlot,
            "location": userRequest.location,
        },
        "database": {
            "host": os.environ.get('DFA_HOST'),
            "username": os.environ.get('DFA_Username'),
            "password": os.environ.get('DFA_Password'),
            "database": os.environ.get('DFA_Database')
        },
        "transactions": json.dumps([transactions])
    })

#from the article "This line ensures that our Flask app runs only when it is executed in the main file and not when it is imported in some other file"
#gonna be honest idk what that means in a practical sense, but we can look into it more if we can get issues when hosting, might come up for file structure too
if __name__ == '__main__':
    #eventually host will be updated to our hosting service URL, can change port as needed
    app.run(host='0.0.0.0', port=8000)