from flask import Flask, request
from teapot import Teapot
import json 

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_teapot():
    return "I'm a little teapot!"


@app.route("/getReply", methods=['POST'])
def test():
    req = request.get_json()
    print(req)

    
    teapot = Teapot(req["serviceId"])
    teapot.setMode("cs")

    knowledge_graph = json.dumps(teapot.knowledge_graph) 
    print(knowledge_graph)

    return teapot.reply(req.message)