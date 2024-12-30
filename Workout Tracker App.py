
import time
import json

class WorkoutTracker:
    def __init__(self):
        self.routines = {}
        self.current_routine = None
        self.current_exercise = None
        self.workout_timer = 0
        self.rest_timer = 0
        self.is_workout_timer_running = False
        self.is_rest_timer_running = False

    def save_routines(self, file_name="routines.json"):
        with open(file_name, 'w') as f:
            json.dump(self.routines, f)

    def load_routines(self, file_name="routines.json"):
        try:
            with open(file_name, 'r') as f:
                self.routines = json.load(f)
        except FileNotFoundError:
            print("No routines file found. Starting fresh.")

    def create_routine(self, name):
        if name in self.routines:
            print("Routine already exists.")
        else:
            self.routines[name] = []

    def delete_routine(self, name):
        if name in self.routines:
            del self.routines[name]
        else:
            print("Routine does not exist.")

    def add_exercise(self, routine_name, exercise_name):
        if routine_name in self.routines:
            self.routines[routine_name].append({"name": exercise_name, "sets": []})
        else:
            print("Routine not found.")

    def remove_exercise(self, routine_name, exercise_name):
        if routine_name in self.routines:
            self.routines[routine_name] = [ex for ex in self.routines[routine_name] if ex['name'] != exercise_name]
        else:
            print("Routine not found.")

    def add_set(self, routine_name, exercise_name, reps, weight=None):
        for exercise in self.routines.get(routine_name, []):
            if exercise["name"] == exercise_name:
                exercise["sets"].append({"reps": reps, "weight": weight})
                return
        print("Exercise not found.")

    def remove_set(self, routine_name, exercise_name, set_index):
        for exercise in self.routines.get(routine_name, []):
            if exercise["name"] == exercise_name:
                if 0 <= set_index < len(exercise["sets"]):
                    exercise["sets"].pop(set_index)
                else:
                    print("Set index out of range.")
                return
        print("Exercise not found.")

    def start_workout_timer(self):
        if not self.is_workout_timer_running:
            self.is_workout_timer_running = True
            print("Workout timer started.")
            self._run_timer("workout")

    def stop_workout_timer(self):
        self.is_workout_timer_running = False
        print(f"Workout timer stopped at {self.workout_timer} seconds.")

    def start_rest_timer(self, rest_duration):
        if not self.is_rest_timer_running:
            self.is_rest_timer_running = True
            print(f"Rest timer started for {rest_duration} seconds.")
            self.rest_timer = rest_duration
            while self.rest_timer > 0 and self.is_rest_timer_running:
                time.sleep(1)
                self.rest_timer -= 1
                print(f"Rest time left: {self.rest_timer} seconds")
            self.is_rest_timer_running = False
            print("Rest timer finished.")

    def stop_rest_timer(self):
        self.is_rest_timer_running = False
        print("Rest timer stopped.")

    def _run_timer(self, timer_type):
        if timer_type == "workout":
            while self.is_workout_timer_running:
                time.sleep(1)
                self.workout_timer += 1
                print(f"Workout time elapsed: {self.workout_timer} seconds.")

    def show_routines(self):
        for routine, exercises in self.routines.items():
            print(f"\nRoutine: {routine}")
            for exercise in exercises:
                print(f"  Exercise: {exercise['name']}")
                for i, s in enumerate(exercise['sets']):
                    weight = s.get("weight", "Bodyweight")
                    print(f"    Set {i+1}: {s['reps']} reps @ {weight}")

# Example Usage
tracker = WorkoutTracker()
tracker.load_routines()

tracker.create_routine("Leg Day")
tracker.add_exercise("Leg Day", "Squats")
tracker.add_set("Leg Day", "Squats", reps=10, weight="135 lbs")
tracker.add_set("Leg Day", "Squats", reps=8, weight="155 lbs")
tracker.show_routines()

tracker.start_workout_timer()
time.sleep(5)
tracker.stop_workout_timer()

tracker.start_rest_timer(10)

tracker.save_routines()
