from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# list all workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():
    pass

# list one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    pass

# create workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    pass

# delete a workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    pass

# list all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    pass

# list one exercise 
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    pass

# create an exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    pass

# delete an exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    pass

# add an exercise to a workout
@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    pass


if __name__ == '__main__':
    app.run(port=5555, debug=True)