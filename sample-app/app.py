from flask import Flask, jsonify

# initialize our Flask application
app = Flask(__name__)

movies = [
    {
        "name": "The Shawshank Redemption",
        "casts": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"],
        "genres": ["Drama"]
    },
    {
       "name": "The Godfather ",
       "casts": ["Marlon Brando", "Al Pacino", "James Caan", "Diane Keaton"],
       "genres": ["Crime", "Drama"]
    }
]

#GET Method   
@app.route('/movies')
def hello():
    return jsonify(movies)

#POST Method

#  main thread of execution to start the server
app.run()
