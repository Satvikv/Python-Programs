#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    
    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
	
def getJsonData(args1,args2):
	jsondata=json.load(open('Flight Data.json'))
	    
	for airline in jsondata:
		for key in dic:
		  if(args1 == dic.get(key)):
			   return {"result":dic.get(args2)}
	return {}		   
def makeWebhookResult(req):
    if req.get("result").get("action") != "Status":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    flight = parameters.get("FlightNumber")

    resultDic=getJsonData(flight,"Status")
    print(resultDic)
    speech = "The status of flight " + flight + " is " + resultDic.get("result")

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')