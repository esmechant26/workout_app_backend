from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError

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
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    return make_response(workout_schema.dump(workout), 200)

# create workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

    new_workout = Workout(duration_minutes=data["duration_minutes"], notes=data.get("notes"))

    db.session.add(new_workout)
    db.session.commit()
    # 201 indicates the request succeded and created a new source
    return make_response(workout_schema.dump(new_workout), 201)

# delete a workout
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response( {"error": "Workout not found"}, 404)

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
    
    return make_response(exercise_schema.dump(exercise), 200)

# create an exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
    except ValidationError as err:
        return make_response({"errors": err.messages}, 400)

    new_exercise = Exercise(
        name = data["name"],
        category = data.get("category"),
        equipment_needed = data.get("equipment_needed")
    )

    db.session.add(new_exercise)
    db.session.commit()
    return make_response(exercise_schema.dump(new_exercise),201)

# delete an exercise
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response( {"error": "Exercise not found"}, 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response({"message": "Exercise deleted"}, 200)

# add an exercise to a workout
@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = workout_exercise_schema.load(request.get_json())

    new_workout_exercise = WorkoutExercise(
        workout_id = workout_id,
        exercise_id = exercise_id,
        reps = data.get("reps"),
        sets = data.get("sets"),
        duration_seconds = data.get("duration_seconds")
    )

    db.session.add(new_workout_exercise)
    db.session.commit()

    return make_response(workout_exercise_schema.dump(new_workout_exercise), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)