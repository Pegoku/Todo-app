from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

@app.route('/tags', methods=['GET'])
def tags():
    query = request.args.get('query')
    tags = Tag.query.filter(Tag.name.like(f'{query}%')).all()
    return jsonify([tag.name for tag in tags])

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('thing_id', db.Integer, db.ForeignKey('thing.id'), primary_key=True)
)

class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
        backref=db.backref('things', lazy=True))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thing_name = request.form.get('thing_name')
        thing_tags = request.form.get('thing_tags').split(',')
        thing_tags = [Tag.query.filter_by(name=tag.strip()).first() or Tag(name=tag.strip()) for tag in thing_tags]
        thing = Thing(name=thing_name, tags=thing_tags)
        db.session.add(thing)
        db.session.commit()
        return redirect(url_for('index'))
    tag_filter = request.args.get('tag_filter')
    if tag_filter:
        things = Thing.query.join(tags).join(Tag).filter(Tag.name == tag_filter)
    else:
        things = Thing.query.all()
    return render_template('index.html', things=things)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    thing = Thing.query.get(id)
    if thing:
        db.session.delete(thing)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/bulk_delete', methods=['POST'])
def bulk_delete():
    ids_to_delete = request.form.getlist('ids')
    ids_to_delete = [int(id) for id in ids_to_delete]
    Thing.query.filter(Thing.id.in_(ids_to_delete)).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)