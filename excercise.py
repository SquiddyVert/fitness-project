class Excercise:
    def __init__(self, name):
        self.name = name
        self.sets = []

    def addSet(self, excerciseSet):
        self.sets.append(excerciseSet)

    def get_summary(self):
        summary = f"Exercise: {self.name}\n"
        for excerciseSetNum, excerciseSetInfo in enumerate(self.sets, 1):
            summary += f"  Set {excerciseSetNum}: {excerciseSetInfo.get_summary()}\n"
        return summary