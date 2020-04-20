import gurobipy as gp
import random
from gurobipy import GRB
import sys
from enum import Enum


# returns a list populated with the the hours in a week to be scheduled
def shiftpopulator():
    list = []
    # weeknumber can be added if need be by adding an extra forloop and the code could be very similar to the hours
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = range(24)
    for i in days:
        for j in hours:
            # concatenating the day string with the hour to generate the label for an hour that is to be scheduled
            list.append(i + str(j))
    return list

#establishing the two types of Firefighters
class FireFighter(Enum):
    basic = "Basic"
    advanced = "Advanced"


# returns a list of volunteers named Volunteer0 to VolunteerN
# name generator for testing
def volunteerList(volunteerNo):
    list = []
    for i in range(volunteerNo):
        list.append("Volunteer" + str(i))
    return list


# each volunteer has an Name,Experience level, preferred Hours, Availability
# is availability different
class Volunteer:
    def __init__(self, name, Explvl, prefHours):
        self.name = name
        self.Explvl = Explvl
        self.prefHours = prefHours
        AvailDict = {}
        for i in shiftpopulator():
            # generates 1 every 1/12 shift
            AvailDict[i] = (int)(random.randrange(0, 12, 2) / 10)
        self.Availability = AvailDict



#Randomly generating a group of different Volunteers
def volunteerGenerate(volunteerNo):
    list = []
    for i in range(volunteerNo):
        expgenerator=random.randrange(0, 4, 1)
        exp=FireFighter.advanced
        if(expgenerator<3):
            exp=FireFighter.basic

        list.append(Volunteer("Volunteer" + str(i),exp,random.randrange(6,14,1)))
    return list

Volunteers=volunteerGenerate(25)

# Model
m = gp.Model("assignment")