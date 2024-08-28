from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
import pprint
import secrets
import random



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

db = SQLAlchemy(app)

with open('jokes.json') as f:
    jokes = json.load(f)
    
class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setup = db.Column(db.String(255), nullable=False)
    punchline = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Joke {self.setup}>'
    
def load_joke_to_db():
    for joke in jokes:
        j = Joke(setup=joke['setup'], punchline=joke['punchline'], type=joke['type'])
        db.session.add(j)
    db.session.commit()
    return jsonify({'message': 'Jokes loaded successfully'}), 201

@app.route('/api/v1/load_jokes', methods=['GET'])
def load_jokes():
    for joke in jokes:
        j = Joke(setup=joke['setup'], punchline=joke['punchline'], type=joke['type'])
        db.session.add(j)
    db.session.commit()
    return jsonify({'message': 'Jokes loaded successfully'}), 201

@app.route('/api/v1/jokes', methods=['GET'])
def get_jokes():
    load_joke_to_db()
    jokes = db.session.query(Joke).all()
    if not jokes:
        return jsonify({'error': 'No jokes found'}), 404
    jokes_list = [{'id': joke.id, 'setup': joke.setup, 'punchline': joke.punchline, 'type': joke.type} for joke in jokes]
    return jsonify(jokes_list), 200

@app.route('/api/v1/jokes/random', methods=['GET'])
def get_random_jokes():
    jokes = db.session.query(Joke).all()
    if not jokes:
        return jsonify({'error': 'No jokes found'}), 404
    joke = random.choice(jokes)
    return jsonify({'id': joke.id, 'setup': joke.setup, 'punchline': joke.punchline, 'type': joke.type}), 200

@app.route('/api/v1/jokes/<int:joke_id>', methods=['GET'])
def get_joke_by_id(joke_id):
    joke = Joke.query.filter_by(id=joke_id).first()
    if not joke:
        return jsonify({'error': 'Joke not found'}), 404
    return jsonify({'id': joke.id, 'setup': joke.setup, 'punchline': joke.punchline, 'type': joke.type}), 200

@app.route('/api/v1/jokes/<int:joke_id>', methods=['DELETE'])
def delete_joke(joke_id):
    joke = Joke.query.filter_by(id=joke_id).first()
    if not joke:
        return jsonify({'error': 'Joke not found'}), 404
    db.session.delete(joke)
    db.session.commit()
    return jsonify({'message': 'Joke deleted successfully'}), 200

@app.route('/api/v1/jokes', methods=['POST'])
def create_joke():
    data = request.get_json()
    joke = Joke(setup=data['setup'], punchline=data['punchline'], type=data['type'])
    db.session.add(joke)
    db.session.commit()
    return jsonify({'message': 'Joke created successfully'}), 201



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        app.run(debug=True, host="0.0.0.0", port=5055)