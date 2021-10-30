from flask import Flask, request
from teapot import Teapot
import json 

from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET', 'POST'])
def hello_teapot():
    return "I'm a little teapot!"


@app.route("/getReply", methods=['POST'])
def test():
    req = request.get_json()
    print(req)

    
    teapot = Teapot(req["service_id"])
    teapot.load()
    knowledge_graph = json.dumps(teapot.knowledge_graph) 
    print(knowledge_graph)

    out_dict={}
    out_dict["message"]=teapot.reply(req["message"])

    return out_dict