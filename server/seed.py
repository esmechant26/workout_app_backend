#!/usr/bin/env python3
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Create exercises
    squat = Exercise(
        name="Squat",
        category="Strength",
        equipment_needed=True
    )

    pushup = Exercise(
        name="Push-up",
        category="Strength",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    db.session.add_all([squat, pushup, plank])
    db.session.commit()

    # Create workouts
    workout1 = Workout(
        duration_minutes=45,
        notes="Full body workout"
    )

    workout2 = Workout(
        duration_minutes=30,
        notes="Short workout"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    # Connect exercises to workouts
    workout_exercise1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=squat.id,
        reps=10,
        sets=3
    )

    workout_exercise2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushup.id,
        reps=12,
        sets=3
    )

    workout_exercise3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=plank.id,
        sets=3,
        duration_seconds=60
    )

    db.session.add_all([
        workout_exercise1,
        workout_exercise2,
        workout_exercise3
    ])

    db.session.commit()

    print("Database seeded!")