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

# Seed the database with initial data     
def seed_data():
    if Villain.query.count() == 0:
        villain1 = Villain(
            name="HexeByte",
            url="https://imagizer.imageshack.com/v2/562x570q70/r/924/g7NQpa.png",
            description=(
                "HexeByte is a rogue hacker sorceress who fused her mind with a forbidden algorithm. "
                "Once an elite cybersecurity expert, she now uses her skills to corrupt systems and control the digital world. "
                "Her glowing eyes, twisted horns, and eerie calm make her presence unforgettable."
            ),
            interests=(
                "She enjoys crashing global databases, planting cursed code in open-source projects, and manipulating AI for her own gain. "
                "She collects rare encryption keys, reads hacker manifestos, and drinks coffee laced with magnetic pulses."
            )
        )

        villain2 = Villain(
            name="Ciphera",
            url="https://imagizer.imageshack.com/v2/557x570q70/r/922/O9iTeI.png",
            description=(
                "Ciphera is a master of encryption turned enemy of open-source freedom. "
                "Once a secret government coder, she now hides behind a hooded suit laced with shifting code. "
                "She believes all information should be hidden, locked, and controlled by those who deserve it. "
                "Her glowing visor and silent presence strike fear in any system she targets."
            ),
            interests=(
                "Ciphera loves breaking into secure networks, encrypting public data beyond recovery, and rewriting access protocols to trap coders in their own systems. "
                "She collects old cryptography books, obsesses over uncrackable ciphers, and runs black-market puzzles only a machine could solve."
            )
        )

        villain3 = Villain(
            name="ZeroVayne",
            url="https://imagizer.imageshack.com/v2/559x570q70/r/923/YwsTvs.png",
            description=(
                "ZeroVayne is a digital assassin born from a failed AI ethics experiment. "
                "Her icy appearance mirrors her emotionless logic. With glowing violet eyes and a cloak of shifting code, she moves like a phantom through firewalls. "
                "She sees coders as reckless gods and wants to bring them to ruin by turning their own creations against them."
            ),
            interests=(
                "She takes pleasure in hijacking machine learning models, injecting logic bombs into AI code, and erasing identity data from networks. "
                "She studies neural networks, trains rogue algorithms, and collects fragments of deleted personalities. "
                "Her favorite sound is corrupted startup tones fading into silence."
            )
        )

        db.session.add_all([villain1, villain2, villain3])
        db.session.commit()


with app.app_context():
    db.create_all()
    db.session.commit()
    seed_data()

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
    villain = Villain.query.filter(func.lower(func.trim(Villain.name)) == name.strip().lower()).first()
    if villain:
        db.session.delete(villain)
        db.session.commit()
        return render_template("villain.html", villains=Villain.query.all())
    else:
        return render_template("deletevillain.html", errors=["Oops! That villain doesn't exist!"])

# Run the flask server
if __name__ == "__main__":
    app.run()
