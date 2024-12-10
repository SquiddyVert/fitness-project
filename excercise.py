# Authors: Samuel Franco and Dekang Lu
# Description: storing the Excercise class
class Excercise:
    def __init__(self, name):
        self.name = name
        self.sets = []

    def addSet(self, excerciseSet):
        self.sets.append(excerciseSet)

    def get_summary(self):
        summary = f"{self.name}:\n"
        for index, excerciseSet in enumerate(self.sets, 1):
            summary += f"  Set {index}: {excerciseSet.get_summary()}\n"
        return summary
