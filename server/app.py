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
    workouts = Workout.query.all()

    return make_response(workouts_schema.dump(workouts))

# list one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    return make_response(workouts_schema.dump(workout), 200)

# create workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = workout_schema.load(request.get_json())
    new_workout = Workout(duration_minutes=data["duration_minutes"], notes=data.get("notes"))

    db.session.add(new_workout)
    db.session.commit()
    return make_response(workout_schema.dump(new_workout), 201)

# delete a workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response( {"error": "Workout not found"})

    db.session.delete(workout)
    db.session.commit()
    return make_response({"message": "Workout deleted"}, 200)

# list all exercises
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)

# list one exercise 
@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    
    return make_response(exercises_schema.dump(exercise), 200)

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