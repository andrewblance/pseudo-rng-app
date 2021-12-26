from flask import Flask
from flask import jsonify
import rng

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    date = "2021/12/24"
    try:
        value = rng.number_generator(date)
    except:
        value = 117
    return jsonify({"randnum":value})
