import json
from typing import Dict
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    return "Hi from Flask"

# Create a route for webhook
@app.route('/webhook', methods = ['GET','POST'])

def webhook() -> Dict:
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    if query_result.get('action') == 'CheckZipCode':

        fulfillmentText = 'Hi'

    

if __name__ == '__main__':
    app.run(port=8080, debug=True)
    
