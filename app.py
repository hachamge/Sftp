import json
from typing import Dict
from pudb import set_trace
from paramiko import SFTPAttributes
from chost.hostconnect import hostconnect
from flask import (Flask, render_template, jsonify, request)

app = Flask(__name__)
app.config['DEBUG'] = True

session:Dict = None
with open("chost/host.json", 'r') as file:
    session = json.load(file)


@app.route("/")
def quickstart():
    data: list[SFTPAttributes] = None
    with hostconnect(session=session) as host:
        data = host.listdir_attr(path=".")

    return render_template("app.html", data=data)

@app.route("/edit", methods=["POST"])
def edit():
    #set_trace()
    responseJson = request.get_json()
    oldpath = responseJson.get("oldpath")
    newpath = responseJson.get("newpath")

    oldpath = f"./{oldpath}"
    newpath = f"./{newpath}"

    with hostconnect(session=session) as host:
        host.rename(oldpath=oldpath, newpath=newpath)

    return jsonify({"status": 202})

if __name__ == "__main__":
    app.run()
