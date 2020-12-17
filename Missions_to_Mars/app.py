from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mission_to_Mars")

@app.route("/")
def home():
    
    mars = mongo.db.mars_data_db.find_one()
    print(mars)
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():  
    mars = mongo.db.mars_data_db
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

