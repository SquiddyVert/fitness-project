# Authors: Samuel Franco and Dekang Lu
# Description: User Profile class

class Profile:
    def __init__(self, name,sex,age,height,weight):
        self.__name = name
        self.__sex = sex
        self.__age = age
        self.__height = height
        self.__weight = weight



    def getName(self):
        return self.__name
    
    def getSex(self):
        return self.__sex
    
    def getAge(self):
        return self.__age
    
    def getHeight(self):
        return self.__height
    
    def getWeight(self):
        return self.__weight
    
    def setName(self, name):
        self.__name = name

    def setSex(self, sex):
        self.__sex = sex

    def setAge(self, age):
        self.__age = age

    def setHeight(self, height):
        self.__height = height

    def setWeight(self, weight):
        self.__weight = weight
