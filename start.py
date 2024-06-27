from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

@app.route('/')
def index():
    things = Thing.query.all()
    return render_template('index.html', things=things)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)