from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"
db = SQLAlchemy(app)

@app.route("/")
def hello_world():
  return render_template("villain.html")

# Run the flask server
if __name__ == "__main__":
    app.run()