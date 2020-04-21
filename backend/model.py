import gurobipy as gp
import random
from gurobipy import GRB
import sys
from enum import Enum


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

def VolunteerTest(number):
    Volunteers=volunteerGenerate(number)
    for i in Volunteers:
            print("preferred Hours: "+str(i.prefHours))
            print("Experience level: "+str(i.Explvl))
            print(i.name+" Availability: ")
            for j in shiftpopulator():
                print(j+": "+str(i.Availability[j]))

            print("\n")

VolunteerTest(3)



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
# each volunteer has an Name,Experience level, preferred Hours, Availability
# is availability different
class Volunteer:
    def __init__(self, name, Explvl, prefHours):
        self.name = name
        self.Explvl = Explvl
        self.prefHours = prefHours
        AvailDict = {}
        for i in shiftpopulator():
          AvailDict[i] = False
          #generates a 0 or 1 and that gets converted to true or false using an if function
          if (int)(random.randrange(0, 12, 2) / 10)==1:
              AvailDict[i] =True
        self.Availability = AvailDict




# Model
m = gp.Model("assignment")