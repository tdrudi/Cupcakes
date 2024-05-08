"""Flask app for Cupcakes"""
from flask import Flask, render_template, request, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret_key"

connect_db(app)

@app.route("/")
def homepage():
    """Homepage"""
    return render_template("index.html")

@app.route("/api/cupcakes")
def all_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes", methods=['POST'])
def create_cupcakes():
    """Create cupcake"""
    data = request.json
    cupcake = Cupcake(
        size = data['size'],
        flavor = data['flavor'],
        rating = data['rating'],
        image = data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    return(jsonify(cupcake = cupcake.to_dict()), 201)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake_info(cupcake_id):
    """Get specific cupcake data"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    """Get data"""
    data = request.json

    """Update cupcake"""
    cupcake.size = data['size']
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Cupcake deleted.')
