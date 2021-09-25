from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)
app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_data = mongo.db.mars.find_one()
    return render_template('index.html', mars = mars_data)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_info = mars_scrape.scrape_info()
    mars.update(
        {},
        mars_info,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)