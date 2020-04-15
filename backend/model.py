#!/usr/bin/env python3.7

# Copyright 2020, Gurobi Optimization, LLC

# Assign workers to shifts; each worker may or may not be available on a
# particular day. If the problem cannot be solved, use IIS to find a set of
# conflicting constraints. Note that there may be additional conflicts besides
# what is reported via IIS.

import gurobipy as gp
import random
from gurobipy import GRB
import sys


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


# returns a list of volunteers named Volunteer0 to VolunteerN
# name generator for testing
def volunteerList(volunteerNo):
    list = []
    for i in range(volunteerNo):
        list.append("Volunteer" + str(i))
    return list


# each volunteer has an Name,Experience level, preferred Hours, Availability
#is availability different
class Volunteer:
    def __init__(self, name, Explvl,prefHours):
        self.name = name
        self.Explvl = Explvl
        self.prefHours=prefHours
        AvailDict = {}
        for i in shiftpopulator():
            #generates 1 every 1/12 shift
            AvailDict[i]=(int)(random.randrange(0, 12, 2)/10)
        self.Availability=AvailDict

#John=Volunteer("John","Basic",10)
for i in volunteerList(13):
    print(i)


