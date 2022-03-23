from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from Models import RecommendationRequest
from Models import Database

import os
import globalStatus
import printFormatting
import traceback
import recommendationEngine

# APP.PY: Handles the routing of the API (this is basically the controller)

# initializes the Flask app
app = Flask(__name__)

# handles CORS policy
CORS(app)

#specifying the route and methods allowed; this is the default/blank route, it accepts GET or POST
@app.route('/', methods=['GET', 'POST'])
#the function that runs when this route is used; this just returns documentation for the API routes
def welcome():
    return """
    <h1>Routes:</h1>
    <hr>
    <h3>/</h3>
    <p>Routes to this page</p>
    <hr>
    <h3>/recommendation</h3>
    <p>Requests item and location recommendations:</p>
    <p><strong>METHOD: </strong>POST<br></p>
    <strong>REQUEST BODY: </strong><br>
    &emsp;{<br>
        &emsp;&emsp;"username": &emsp;string,<br>
        &emsp;&emsp;"time": &emsp;&emsp;&emsp;datetime, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>(YYYY-DD-MM hh:mm:ss, note that this is 24-hour time)</em><br>
        &emsp;&emsp;"timeSlot": &nbsp;&nbsp;&emsp;string, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>(should be "Morning", "Afternoon", or "Night")</em><br>
        &emsp;&emsp;"latitude": &nbsp;&nbsp;&nbsp;&emsp;float, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>(6 decimal places preferred but not required)</em><br>
        &emsp;&emsp;"longitude": &emsp;float, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<em>(6 decimal places preferred but not required)</em><br>
    &emsp;}
    <hr>
    """

# this route is for recommendation; route is URL/recommendation, requires POST method
# refer to other documentation or the default route for details on the POST body
@app.route('/recommendation/', methods=['POST'])
# this function returns the recommended items and locations; refer to documentation or log the JSON return to see the structure
def recommendItemsAndLocations():
    printFormatting.printSuccess("Recommendation request received")
    
    # this is the global status array; it needs to be in this scope in case making the request fails
    # do not initialize it again, the Status object is basically a singleton
    globalStatus.init()
    printFormatting.printSuccess("Engine status initialized")

    # if this outer try/except excepts, a default item and blank locations are returned
    try:
        # loading environment variables; this should only have to happen once but try doing this before using them again if it causes issues
        load_dotenv()
        
        # making database object so that db credentials only have to be loaded once
        db = Database.Database()

        # request.json will contain the request body; this saves it into a RecommendationRequest object
        userRequest = RecommendationRequest.RecommendationRequest(request.json, db)

        # recommending closest location; will be the address or a blank string if something goes wrong
        closestLocation = recommendationEngine.recommendClosestLocation(userRequest, db)

        # recommending most recent location; will be the address or a blank string if something goes wrong
        recentLocation = recommendationEngine.recommendRecentLocation(userRequest, db)
        
        # best address should be blank unless the closest and most recent stores match; this function handles that logic
        bestLocation = recommendationEngine.determineBestLocation(closestLocation, recentLocation)

        # recommending items; if something goes wrong, it'll be just the default item
        items = recommendationEngine.recommendItems(userRequest, db)

        # returns the statuses and recommendations; recommendations[0] will be the top recommendation
        return jsonify({
            "statuses": globalStatus.statusArray,
            "items": [item.__dict__ for item in items],
            "locations": {
                "bestLocation": bestLocation,
                "closestLocation": closestLocation,
                "recentLocation": recentLocation
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
        # however, recommendations will just be an array with the single default recommendation (no default location, because that's unhelpful)
        # the values come from the configuration file rather than attempting to access the database since that's a likely cause of failure
        return jsonify({
            "statuses": globalStatus.statusArray,
            "items": [{
                "id": int(os.environ.get('Default_Recommendation_ID')),
                "imgUrl": os.environ.get('Default_Recommendation_ImageURL'),
                "name": os.environ.get('Default_Recommendation_Name'),
                "score": int(os.environ.get('Default_Recommendation_Score'))
            }],
            "locations": {
                "bestLocation": "",
                "closestLocation": "",
                "recentLocation": ""
            }
        })

# # from the article "This line ensures that our Flask app runs only when it is executed in the main file and not when it is imported in some other file"
# # gonna be honest idk what that means in a practical sense, but we can look into it more if we can get issues when hosting, might come up for file structure too
# if __name__ == '__main__':
#     # eventually host will be updated to our hosting service URL, can change port as needed
#     app.run(host='0.0.0.0', port=8000)