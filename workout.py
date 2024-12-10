# Authors: Samuel Franco and Dekang Lu
# Description: Workout class
class Workout:
    def __init__(self, date):
        self.date = date
        self.exercises = []

    def addExercise(self, exercise):
        self.exercises.append(exercise)

    def getSummary(self):
        summary = f"Workout Date: {self.date}\n"
        for exercise in self.exercises:
            summary += exercise.get_summary() + "\n"
        return summary
