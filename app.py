from flask import Flask, request, send_from_directory
from teapot import Teapot
import json 
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/build')

CORS(app)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)



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