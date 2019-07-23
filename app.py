import os
import flask
from flask import request, jsonify, render_template, url_for
from CSVManipulator import *

"""
Backend RESTful endpoints for code_challenge_question_dump.csv.
All functionality has been tested using Postman.
Input to this application should be validated by the client.
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True

dataManipulator = CSVManipulator("data/code_challenge_question_dump.csv")

"""
This endpoint allows for the favicon to display in the browser heading.
"""
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
"""
Homepage
"""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

"""
This endpoint returns all current entries in code_challenge_question_dump.csv in
JSON format.
"""
@app.route('/api/viewall', methods=['GET'])
def api_viewall():
    return jsonify(dataManipulator.dataEntries)

"""
This endpoint allows a user to add a question to code_challenge_question_dump.csv.
"""
@app.route('/api/createQ', methods=['POST'])
def api_createQ():
    try:
        dataManipulator.add_to(request.data.decode('utf-8'))
        return "Success!"
    except:
        return "Failure!"

"""
This endpoint allows deletion of a question from code_challenge_question_dump.csv.
Input format "arg0 + arg1?".
"""
@app.route('/api/deleteQ', methods=['DELETE'])
def api_deleteQ():
    try:
        dataManipulator.delete_from(request.data.decode('utf-8'))
        return "Success!"
    except:
        return "Failure!"

"""
This endpoint allows for a question to be edited in code_challenge_question_dump.csv.
"""
@app.route('/api/editQ', methods=['POST'])
def api_editQ():
    try:
        req_data = request.get_json()
        dataManipulator.edit_question(req_data['question'], req_data['newQ'])
        return "Success!"
    except:
        return "Failure!"

"""
This endpoint allows for questions to be found in code_challenge_question_dump.csv
based on given criteria.
"""
@app.route('/api/filter', methods=['POST'])
def api_filter():
    try:
        req_data = request.get_json()
        return jsonify(dataManipulator.filter_for(req_data))
    except:
        return jsonify([{"question" : "Failure!"}])

"""
This endpoint allows for the contents of code_challenge_question_dump.csv to be
sorted by question or answer.
"""
@app.route('/api/sort', methods=['POST'])
def api_sort():
    try:
        req_data = request.get_json()
        dataManipulator.sort_by(req_data['operation'], req_data['attribute'])
        return "Success!"
    except:
        return "Failure!"

app.run()
