import random
import json
import os, shutil
import datetime
from backend.gurobi.AssetTypes import *

# returns a list populated with the the hours in a week to be scheduled
def shiftpopulator():
    results = []
    # weeknumber can be added if need be by adding an extra forloop and the code could be very similar to the hours
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    blocks = range(48)
    for i in days:
        for j in blocks:
            # concatenating the day string with the hour to generate the label for an hour that is to be scheduled
            results.append(i + str(j))
    return results



#turns shift strings into timeblocks
def DayHourtoNumConverter(DayHour):
    #totalblocks of time per day
    totalblocks=48
    #Starts from monday
    Timeblock=0
    if(DayHour[0:3]=="Tue"):
        Timeblock+=1*totalblocks
    if (DayHour[0:3] == "Wed"):
        Timeblock += 2*totalblocks
    if (DayHour[0:3] == "Thu"):
        Timeblock += 3*totalblocks
    if (DayHour[0:3] == "Fri"):
        Timeblock += 4*totalblocks
    if (DayHour[0:3] == "Sat"):
        Timeblock += 5*totalblocks
    if (DayHour[0:3] == "Sun"):
        Timeblock += 6*totalblocks
    Timeblock+=int(DayHour[3:5])
    return Timeblock
def NumtoDayHourConverter(Num):
    #totalblocks of time per day
    totalblocks=48
    DayHour=""
    #Starts from monday
    if(Num<totalblocks*1):
        DayHour += "Mon"
    elif(Num<totalblocks*2):
        DayHour += "Tue"
    elif (Num < totalblocks * 3):
        DayHour += "Wed"
    elif (Num < totalblocks * 4):
        DayHour += "Thu"
    elif (Num < totalblocks * 5):
        DayHour += "Fri"
    elif (Num < totalblocks * 6):
        DayHour += "Sat"
    else:
        DayHour += "Sun"
    DayHour += str(Num%totalblocks)

    return DayHour
#returns true Percent% of the time
def booleangenerator(Percent):
    if(Percent>=random.randint(1, 100)):
        return True
    else:
        return False



def AvailabilityGenerator():
    AvailDict = {}
    #arbitrary false declaration so the value assigned in the loop stays on
    generatedbool=False
    for j in shiftpopulator():
        # i is timeblock
        i=DayHourtoNumConverter(j)
        # 240 corressponds to 12am on a saturday so i<240 represents weekdays
        if(i<240):
            if(i%48==0):
                #at 12 am to 9am on weekdays generates a true 10% of the time for the set of volunteers generated
                generatedbool=booleangenerator(10)
            if (i % 48 == 18):
                #at 9am to 5pm on weekdays generates a true 20% of the time for the set of volunteers
                generatedbool = booleangenerator(20)
            if (i % 48 == 34):
                #  5pm onwards on weekdays generates a true 80% of the time for the set of volunteers
                generatedbool = booleangenerator(80)
        #weekdays
        else:
        # weekends
            if (i % 48 == 0):
                # at 12 am to 9am on weekends generates a true 10% of the time for the set of volunteers generated
                generatedbool = booleangenerator(10)
            if (i % 48 == 18):
                # at 9am onwards on weekends generates a true 80% of the time for the set of volunteers
                generatedbool = booleangenerator(80)

        #assigns the generated boolean
        #converts to the string format for now
        AvailDict[j]=generatedbool

    return AvailabilityConverter(AvailDict)



def next_monday():
    i=0
    while((datetime.datetime.today()+datetime.timedelta(days=i)).weekday()!=0):
        i+=1
    return  (datetime.datetime.today()+ datetime.timedelta(days=i)).replace(hour=0,minute=0,second=0,microsecond=0)




def AvailabilityConverter(AvailabilityDict):
    """Takes availabilities in boolean and timeblock representation and changes it to a list of days and starttimes"""

    Days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    #the
    MondayTime=next_monday()
    #this is a boolean that tracks the start of a shift in order to convert into a set of tuples
    #with a start and end
    NewShiftCheck=False
    timepairs=[]
    #this will hold the time pairs
    TimePairList=list()

    for shift in shiftpopulator():
        Timeblocknumber=DayHourtoNumConverter(shift)
        # This represents the start of a time pair the case that a person has started being available
        if (AvailabilityDict[shift] and not NewShiftCheck):
            NewShiftCheck = True
            timepairs.append(MondayTime+datetime.timedelta(hours=(Timeblocknumber%48) / 2))

        # This represents the end of a time pair
        if (not AvailabilityDict[shift] and NewShiftCheck):
            NewShiftCheck = False
            timepairs.append(MondayTime+datetime.timedelta(hours=(Timeblocknumber%48) / 2))
            TimePairList.append(timepairs)
            timepairs=[]
    return TimePairList


def deleteContents(path):
    import os, shutil
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
#generates number volunteers in the volunteers folder
def VolunteerJson(Volunteers, folder_path):
    #Converting the enums into strings for JSon
    for i in Volunteers:
        i.Explvl=i.Explvl.value
    j=0
    #this is to ensure that the volunteers from previous runs of the file are being deleted
    deleteContents(folder_path)

    for i in Volunteers:
        with open(folder_path + '/volunteer'+str(j)+'.json', 'w') as fp:
            json.dump(i.__dict__, fp)
        j += 1

