# -*- coding: utf-8 -*-

from flask_cors import CORS
from flask import Flask, request
import os
import sys
import requests
import asyncio
import json
# Hack to alter sys path, so we will run from microservices package
# This hack will require us to import with absolut path from everywhere in this module
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(APP_ROOT))

loop = asyncio.get_event_loop()

app = Flask(__name__)
CORS(app)

total_requests = 0

@app.route('/health', methods=['GET'])
def health():
    return 'OK'


@app.route('/', methods=['GET'])
def load():
    global total_requests
    total_requests  += 1
    my_host = os.environ.get("HOSTNAME", request.host)
    my_name = os.environ.get("RETURN_VALUE", "NOT_SET")
    dependencies = os.environ.get("DEPENDENCIES", "").split(",")
    res = ""
    for dependency in dependencies:
        if dependency == "":
            continue
        print("sending request to {}".format(dependency))
        res += requests.get("http://"+dependency).text + "\n"
    
    ret = "Advance Networking app running on host {}, my name is {}, and I have served a total of {} requests\n".format(my_host, my_name, total_requests)

    if res != "":
        ret += "propogated request to {} with result {}\n".format(dependency, res)
    
    return ret


if __name__ == '__main__':
    # threaded=True is a debugging feature, use WSGI for production!
    app.run(host='0.0.0.0', port='8080', threaded=False)
    print("Hey there from Advance Networking App")
