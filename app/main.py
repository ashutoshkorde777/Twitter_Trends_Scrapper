from flask import Flask, render_template, jsonify
import sys
import os
from pymongo import MongoClient
import json
from dotenv import load_dotenv



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.scraper import scrape_trending_topics 


load_dotenv()

# Get the MongoDB configuration from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  
db_name = os.getenv("DB_NAME", "twitter_trends")  
collection_name = os.getenv("COLLECTION_NAME", "trends")  

# MongoDB setup
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-scraper", methods=["GET"])
def run_scraper():
    record = scrape_trending_topics()
    return jsonify(record)

@app.route("/get_record/<string:id>", methods=["GET"])
def get_record_by_id(id):
    try:
       
        record = collection.find_one({"_id": id})

        # Check if record exists
        if record:
            record["_id"] = str(record["_id"])  
            return jsonify(record), 200
        else:
            return jsonify({"message": "Record not found"}), 404

    except Exception as e:
        # Handle errors (invalid ObjectId, etc.)
        return jsonify({"error": f"An error occurred while fetching the record: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
