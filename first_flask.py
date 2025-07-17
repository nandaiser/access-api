from flask import Flask, request
from json import jsonify

app  = Flask(__name__)

@app.route('/')
def string():
    return " this HOME page"

@app.route('/notes',methods = ["POST"])

def notes():
    data = request.json
    return f"Notes posted:{data['content']}"

if __name__ == "__main__":
    app.run(debug = True)