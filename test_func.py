# Authors: Samuel Franco and Dekang Lu
# Description: testing functions
import functions as func
import pytest
from exercise import Exercise
from set import Set

def test_calcBMI():
    result = func.calcBMI(72,200)
    assert 27.0 < result < 27.2

@pytest.mark.xfail(reason="Input should not be text!")
def test_matchBMI():
    func.matchBMI("5")

def test_exercise():
    newSet = Set()
    newEx = Exercise("pull up")
    newEx.addSet(newSet)
    assert len(newEx.sets) > 0
