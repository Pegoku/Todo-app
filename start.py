from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thing_name = request.form.get('thing_name')
        thing = Thing(name=thing_name)
        db.session.add(thing)
        db.session.commit()
        return redirect(url_for('index'))
    things = Thing.query.all()
    return render_template('index.html', things=things)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    thing = Thing.query.get(id)
    if thing:
        db.session.delete(thing)
        db.session.commit()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)