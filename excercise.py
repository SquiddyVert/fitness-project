# Authors: Samuel Franco and Dekang Lu
# Description: storing the exercise class
class exercise:
    def __init__(self, name):
        self.name = name
        self.sets = []

    def addSet(self, exerciseSet):
        self.sets.append(exerciseSet)

    def get_summary(self):
        summary = f"{self.name}:\n"
        for index, exerciseSet in enumerate(self.sets, 1):
            summary += f"  Set {index}: {exerciseSet.get_summary()}\n"
        return summary
