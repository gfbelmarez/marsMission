from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

site_data = mongo.db.mars_data

@app.route("/")
def index():
    data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars=data)


@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    site_data.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
