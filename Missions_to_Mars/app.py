# Import Flask dependencies
# Bring in pymongo optimized for Flask
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Import scrape function located in scrape_mars.py
import scrape_mars

# Setup Flask
app = Flask(__name__)


# Configure MongoDB connection
# Create a database called mars_app
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():

    # Pull in data from MongoDB and save it into a listing
    mars_data = mongo.db.mars_data.find_one()

    # Render results into an HTML format
    return render_template("index.html",mars_data = mars_data)

@app.route("/scrape")
def scraper():
    # Call scrape.py to pull into data from web scraping function called scrape
    result = scrape_mars.scrape()

    # Create a mars_data collection in mars_app database
    mars_data = mongo.db.mars_data

    # Update the mars_data collection with result (from web scraping)
    # if there no docs with the name, then insert.
    # if document exists, then update the already existing record
    mars_data.update({}, result, upsert=True)

    # Return back to homesite with a specific message
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

