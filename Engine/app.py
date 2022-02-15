from flask import Flask, request, jsonify
from Models import RecommendationRequest

# initializes the Flask app
app = Flask(__name__)

#specifying the route and methods allowed; I think we'll just do GET, maybe something for logging in?
@app.route('/hello/', methods=['GET', 'POST'])
#I don't think the name of the function matters? I have no clue tbh, I guess they don't matter in .NET either...
def welcome():
    return "update"

@app.route('/recommendation/', methods=['GET'])
def recommendItem():
    # request.json will contain the request body; this saves it into a RecommendationRequest object
    # will return a 400 if the request body formatting is bad
    userRequest = RecommendationRequest.RecommendationRequest(request.json)
    
    #for testing, just returning the rec request as-is
    return jsonify({
        "username": userRequest.username,
        "time": userRequest.time,
        "timeSlot": userRequest.timeSlot,
        "location": userRequest.location
    })

#from the article "This line ensures that our Flask app runs only when it is executed in the main file and not when it is imported in some other file"
#gonna be honest idk what that means in a practical sense, but we can look into it more if we can get issues when hosting, might come up for file structure too
if __name__ == '__main__':
    #eventually host will be updated to our hosting service URL, can change port as needed
    app.run(host='0.0.0.0', port=8000)