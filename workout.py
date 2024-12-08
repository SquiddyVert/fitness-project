class Workout:
    def __init__(self, date):
        self.date = date
        self.excercises = []

    def addExcercise(self, excercise):
        self.exercises.append(excercise)

    def getSummary(self):
        summary = f"Workout Date: {self.date}\n"
        for exercise in self.exercises:
            summary += exercise.get_summary() + "\n"
        return summary