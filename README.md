# Workout API

## Project Description
Workout API is a Flask REST API for creating and managing workouts and exercises. Users can create, view, and delete workouts and exercises, as well as add exercises to workouts with reps, sets, and duration.

## Tech Stack
The application uses SQLAlchemy to manage database models and relationships, Marshmallow for serialization, deserialization, and schema validation, and Flask-Migrate for database migrations.

## Installation
Clone the repository and navigate into the project directory.

Install the project dependencies:

pipenv install
cd server
flask db upgrade
python seed.py
flask run --port 5555

Seed the database:
python seed.py

The seed file clears the existing database records and creates sample workouts, exercises, and workout-exercise relationships.

## Running the Application
From the `server` directory, start the Flask application with:

```bash
flask run --port 5555
```

The API will then be available locally on port `5555`.

## API Endpoints

### Workouts
**GET `/workouts`**
Returns a list of all workouts.
**GET `/workouts/<id>`**
Returns a single workout by ID along with its associated exercises.
**POST `/workouts`**
Creates a new workout.

Example request data:
```json
{
  "duration_minutes": 45,
  "notes": "Full body workout"
}
```

**DELETE `/workouts/<id>`**
Deletes a workout by ID.

### Exercises
**GET `/exercises`**
Returns a list of all exercises.
**GET `/exercises/<id>`**
Returns a single exercise by ID along with its associated workouts.
**POST `/exercises`**
Creates a new exercise.

Example request data:

```json
{
  "name": "Squat",
  "category": "Strength",
  "equipment_needed": true
}
```

**DELETE `/exercises/<id>`**
Deletes an exercise by ID.

### Workout Exercises
**POST `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`**
Adds an existing exercise to an existing workout. Reps, sets, and duration can be provided for the exercise.

Example request data:

```json
{
  "reps": 10,
  "sets": 3,
  "duration_seconds": 60
}
```

## Validation
The API includes validation at the database, model, and schema levels.

- Exercise names are required and unique.
- Workout duration must be greater than zero.
- Reps must be greater than or equal to one.
- Sets must be greater than or equal to one.
- Exercise duration must be greater than or equal to one when provided.
- Workout and exercise foreign keys are required for workout-exercise records.

Invalid request data is rejected with an error response.

## Dependencies
Project dependencies are listed in the `Pipfile` and can be installed with:

```bash
pipenv install
```

Major dependencies include Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow, and SQLAlchemy.

## Tests
API functionality can be tested using Flask's test client. The application supports testing successful requests, validation errors, and missing resources.

If automated test files are included with the project, they can be run from the project environment using the appropriate test command.
