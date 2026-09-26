from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
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
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.String)

    # Workout has many WorkoutExercises (one to many)
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")

    # workout has many Exercises through WorkoutExercises (many to many)
    exercises = db.relationship("Exercise", secondary="workout_exercises", viewonly=True)

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