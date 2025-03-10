from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"

db = SQLAlchemy(app)

class Villain(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(250), nullable=False)
  interests = db.Column(db.String(250), nullable=False)
  url = db.Column(db.String(250), nullable=False)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def __repr__(self):
  return "<Villain "+ self.name + ">"

@app.route("/")
def villains_cards():
  return render_template("villain.html")

# Run the flask server
if __name__ == "__main__":
    app.run()