from flask import Flask
from flask import request
from flask import jsonify, make_response
import numpy as np

from datetime import datetime, timezone

from db_table import db_table

app = Flask(__name__)

# Set up db connection
def get_db_conn():
    db_schema = {
        "Date": "date PRIMARY KEY",
        "Gold": "float",
        "Silver": "float"
    }
    return db_table("Prices", db_schema)


@app.route('/commodity', methods=["GET"])
def compute_commodity():
    db = get_db_conn()
    # Making sure we have all the arguments we need
    if not request.args.get("start_date"):
        return make_response(jsonify({"message": "Invalid start date"}), 400)
    if not request.args.get("end_date"):
        return make_response(jsonify({"message": "Invalid end date"}), 400)
    if not request.args.get("commodity_type"):
        return make_response(jsonify({"message": "Invalid commodity type"}), 400)

    start = request.args.get("start_date")
    end = request.args.get("end_date")
    commodity_type = request.args.get("commodity_type")

    # Convert datetime to Unix timestamp to index into DB
    start = datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()
    end = datetime.strptime(end, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()

    if commodity_type.lower() != "gold" and commodity_type.lower() != "silver":
        return make_response(jsonify({"message": "Commodity type gold or silver only"}), 400)

    results = db.select_prices_between_dates(start, end, commodity_type)
    data = {}
    numpy_array = []
    for result in results:
        date = str(datetime.utcfromtimestamp(result[0]))
        price = result[1] or -1
        if price is -1:
            continue
        data[date[:-9]] = price
        numpy_array.append(price)

    mean = np.mean(numpy_array).astype(float)
    variance = np.var(numpy_array).astype(float)

    return_data = {
        "data": data,
        "mean": round(mean, 2),  # Example given, the data was rounded to the closes 2 decimal places
        "variance": round(variance, 2)
    }

    return make_response(jsonify(return_data), 200)
