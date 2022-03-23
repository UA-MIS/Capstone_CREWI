from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from .Models import RecommendationRequest
from .Models import Database
from .Functions import globalStatus
# from .Functions import printFormatting
from .Functions import recommendationEngine

import os
import traceback

app = Flask(__name__)
 
@app.route("/")
def home_view():
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