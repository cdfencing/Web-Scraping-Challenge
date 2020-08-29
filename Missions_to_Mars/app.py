# import the libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

# Flask app
app = Flask(__name__)
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

@app.route("/")
def home():

    marsDB = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars=marsDB)

@app.route("/scrape")
def scrape():
  
    marsDB = mongo.db.mars_dict
    mars_info = mars_scrape.scrape()
    
    marsDB.update({}, mars_info, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True, port = 5009)