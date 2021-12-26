from flask import Flask
from flask import jsonify
import rng
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    date = datetime.today().strftime('%Y/%m/%d')

    try:
        value = rng.number_generator(date)
    except:
        value = 117
    return jsonify({"date": date,
                    "randnum": value})
