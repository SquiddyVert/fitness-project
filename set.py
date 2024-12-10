# Authors: Samuel Franco and Dekang Lu
# Description: Set class
class Set:
    def __init__(self, reps = 0, weight = 0):
        self.reps = reps
        self.weight = weight

    def get_summary(self):
        return f"{self.reps} reps, {self.weight} lbs"
