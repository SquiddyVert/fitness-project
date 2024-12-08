class Set:
    def __init__(self, reps, weight):
        self.reps = reps
        self.weight = weight

    def get_summary(self):
        return f"{self.reps} reps, {self.weight} lbs"