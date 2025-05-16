from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func 
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///villain.db"

db = SQLAlchemy(app)

class Villain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    interests = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Villain " + self.name + ">"

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/")
def villains_cards():
    return render_template("villain.html", villains=Villain.query.all())

@app.route("/add", methods=["GET"])
def add_villain():
    return render_template("addvillain.html", errors=[])

@app.route("/delete", methods=["GET"])
def delete_villain():
    return render_template("deletevillain.html", errors=[])

@app.route("/list")
def list_villains():
    return "<br>".join([f" '{v.name}' " for v in Villain.query.all()])

@app.route("/addVillain", methods=["POST"])
def add_user():
    errors = []
    name = request.form.get("name").strip() #Remove Whitespace
    villain = Villain.query.filter(func.lower(Villain.name) == name.lower()).first() #Case-insensitive match
    
    if not name:
        errors.append("Oops! Looks like you forgot a name!")
    description = request.form.get("description")
    if not description:
        errors.append("Oops! Looks like you forgot a description!")
    interests = request.form.get("interests")
    if not interests:
        errors.append("Oops! Looks like you forgot some interests!")
    url = request.form.get("url")
    if not url:
        errors.append("Oops! Looks like you forgot an image!")
    if villain:
        errors.append("Oops! A villain with that name already exists!")

    if errors:
        return render_template("addvillain.html", errors=errors)
    else:
        new_villain = Villain(
            name=name, description=description, interests=interests, url=url
        )
        db.session.add(new_villain)
        db.session.commit()
        return render_template("villain.html", villains=Villain.query.all())
    
@app.route("/deleteVillain", methods=["POST"])
def delete_user(): 
    name = request.form.get("name").strip().lower()
    villain = Villain.query.filter(func.lower(Villain.name) == name).first()
    if villain:
        db.session.delete(villain)
        db.session.commit()
        return render_template("villain.html", villains=Villain.query.all())
    else:
        return render_template("deletevillain.html", errors=["Oops! That villain doesn't exist!"])

# Run the flask server
if __name__ == "__main__":
    app.run()
