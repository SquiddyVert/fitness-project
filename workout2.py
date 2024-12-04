class Workout:
    def __init__(self,name,set,rep,time,weight,tired):
        self._name = name
        self._sets = set
        self._reps = rep
        self._time = time
        self._weight = weight
        self._tiredScale = tired
    
    def getName(self):
        return self._name 
    def getSets(self):
        return self._sets 
    def getReps(self):
        return self._reps 
    def getTime(self):
        return self._time 
    def getWeight(self):
        return self._weight 
    def getTired(self):
        return self._tiredScale 
    
    def setName(self,input):
        self._name = input
    def setSets(self,input):
        self._sets = input
    def setReps(self,input):
        self._reps = input
    def setTime(self,input):
        self._time = input 
    def setWeight(self,input):
        self._weight = input
    def setTired(self,input):
        self._tiredScale = input