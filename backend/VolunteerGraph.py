
# Importing the matplotlb.pyplot
import random
from typing import List, Any

import matplotlib.pyplot as plt

from backend.AssetTypes import *

from backend.DataGenerator import NumtoDayHourConverter

EveryWeekday = [Request(LightUnit, 34, 13), Request(MediumTanker, 34, 13)
    , Request(MediumTanker, 82, 13), Request(HeavyTanker, 82, 13),
                Request(MediumTanker, 34 + 2 * 48, 13), Request(HeavyTanker, 34 + 2 * 48, 13),
                Request(MediumTanker, 34 + 3 * 48, 13), Request(HeavyTanker, 34 + 3 * 48, 13),
                Request(MediumTanker, 34 + 4 * 48, 13), Request(LightUnit, 34 + 4 * 48, 13)
                ]

def RequestPlot(Requests):
    fig, gnt = plt.subplots()
    widthScale=4
    # Setting Y-axis limits
    Ylim=250
    gnt.set_ylim(0, Ylim)
    # Setting X-axis limits
    gnt.set_xlim(0, 48*7*widthScale)
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('TimeBlock')
    gnt.set_ylabel('Asset')

    yticklist=[]

    yticklabels: List[str] = []
    xticklist=[]
    xticklabellist=[]

    for i in range(0,336):
        if i%48==0:
            xticklist.append(i*widthScale)
            xticklabellist.append((NumtoDayHourConverter(i)))



    gnt.set_xticks(xticklist)
    gnt.set_xticklabels(xticklabellist)
    # Setting graph attribute
    gnt.grid(True)

    j = 0
    for i in Requests:
        gnt.broken_barh([(i.StartTime*widthScale, i.Duration*widthScale)], (0 + j * Ylim/len(Requests), 10),
                        facecolors=(
                        random.randint(10, 240) / 255, random.randint(10, 240) / 255, random.randint(10, 240) / 255))
        yticklabels.append(i.AssetType.type)
        yticklist.append(0 + j * Ylim/len(Requests)+5)
        j += 1
    # Setting ticks on y-axis
    gnt.set_yticks(yticklist)

    fig.set_size_inches(18.5, 10.5)
    fig.savefig('Problem.png', dpi=100)

class Assignment():
    def __init__(self, VolunteerID, Start, Duration):
        self.VolunteerID = VolunteerID
        # no use now just there for informations sake
        self.Start = Start
        self.Duration = Duration

def VolunteerPlot(assignments):
    fig, gnt = plt.subplots()
    widthScale=4
    # Setting Y-axis limits
    Ylim=250
    gnt.set_ylim(0, Ylim)
    # Setting X-axis limits
    gnt.set_xlim(0, 48*7*widthScale)
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('TimeBlock')
    gnt.set_ylabel('Volunteer ID')

    yticklist=[]

    yticklabels: List[str] = []
    xticklist=[]
    xticklabellist=[]

    for i in range(0,336):
        if i%48==0:
            xticklist.append(i*widthScale)
            xticklabellist.append((NumtoDayHourConverter(i)))



    gnt.set_xticks(xticklist)
    gnt.set_xticklabels(xticklabellist)
    # Setting graph attribute
    gnt.grid(True)


    for i in assignments:
        gnt.broken_barh([(i.Start*widthScale, i.Duration*widthScale)], (0 + i.VolunteerID * Ylim/len(assignments), 10),
                        facecolors=(
                        random.randint(10, 240) / 255, random.randint(10, 240) / 255, random.randint(10, 240) / 255))
        yticklabels.append(str(i.VolunteerID))
        yticklist.append(0 + i.VolunteerID * Ylim/len(assignments)+5)

    # Setting ticks on y-axis
    gnt.set_yticks(yticklist)
    # Labelling tickes of y-axis
    gnt.set_yticklabels(yticklabels)
    # Declaring a bar in schedule
    # [(40, 50)] start and length
    # (30, 9) center and width
    fig.set_size_inches(36.5, 20.5)
    fig.savefig('Solution.png', dpi=100)
