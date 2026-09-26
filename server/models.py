from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    # Exercise has many WorkoutExercises (one to many)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise")

    # Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship("Workout", secondary="workout_exercises", viewonly=True)

class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    # date the workout was created
    date = db.Column(db.DateTime, server_default=db.func.now())
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String)

    # Workout has many WorkoutExercises (one to many)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")

    # workout has many Exercises through WorkoutExercises (many to many)
    exercises = db.relationship("Exercise", secondary="workout_exercises", viewonly=True)

    # validation ensuring duration_minutes is greater than 0
    @validates("duration_minutes")
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is not None and duration_minutes <=0:
            raise ValueError("Duration must be greater than 0.")
        return duration_minutes

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workout.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # WorkoutExercise belongs to a Workout (many to one)
    workout = db.relationship("Workout", back_populates="workout_exercises")

    # WorkoutExercises belongs to an Exercise (many to one)
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # validations ensuring that the values of reps, sets, and duration_seconds are greater than 0
    @validates("reps")
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than 0.")
        return reps

    @validates("sets")
    def validate_sets(self, key, sets):
        if sets is not None and sets <=0:
            raise ValueError("Sets must be greater than 0.")
        return sets

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, duration_seconds):
        if duration_seconds is not None and duration_seconds <=0:
            raise ValueError("Duration must be greater than 0.")
        return duration_seconds

# Marshmallow Schemas for each model, mirror table constraints/validations
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    # name must exist (equal to or longer than 1 character)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str()
    equipment_needed = fields.Bool()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime(dump_only=True)
    # duration must exist (equal to or longer than 1 min)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()
    exercises = fields.Nested(ExerciseSchema, many=True, dump_only=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    # reps, sets, and duration may or may not exist. if they do, they must be equal to or more than 1
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

# serialization / deserialization
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)