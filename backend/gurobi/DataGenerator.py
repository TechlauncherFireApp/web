import random
from enum import Enum
import json
import os, shutil


# returns a list populated with the the hours in a week to be scheduled
from gurobi.Names import *


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

def NumberGenerator():
    tempnumber = "04"
    for j in range(8):
        tempnumber += str(random.randint(0, 9))
    return tempnumber


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

#establishing the two types of Firefighters
class FireFighter(Enum):
    advanced = "Advanced"
    basic = "Basic"
    crewleader="Crew Leader"
    driver="Driver"


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

    return AvailDict


# each volunteer has an Name,Experience level, preferred Hours, Availability
# is availability different
class Volunteer:
    def __init__(self, id,name, Explvl, prefHours,phonenumber,Availability):
        self.id=id
        self.name = name
        self.Explvl = Explvl
        self.prefHours = prefHours
        self.phonenumber=phonenumber
        self.Availability = Availability

#Randomly generating a group of different Volunteers
#THIS FUNCTION OCCASIONALLY ATTEMPTS TO ACCESS AN OUT OF BOUNDS INDEX, around line 110
def VolunteerGenerate(volunteerNo, folder_path):
    list_volunteers = []
    #generates twice as many advanced firefighters as basic
    for i in range(volunteerNo):
        #Generates a random name from the pool available
        Name=firstNames[random.randint(0,len(firstNames)-1)]+" "+lastNames[random.randint(0,len(lastNames)-1)]
        #50% are basic
        if(booleangenerator(50)):
            exp=FireFighter.basic
        #30% are just advanced
        elif(booleangenerator(60)):
            exp=FireFighter.advanced
        #14% are drivers
        elif(booleangenerator(70)):
            exp=FireFighter.driver
        #6% are crewleaders
        else:
            exp=FireFighter.crewleader
        #preferred hours between 6 and 14
        prefnum=random.randint(6, 14)
        #Generates an Availability
        AvailDict = AvailabilityGenerator()


        #generates a random australian phone number
        tempnumber = NumberGenerator()
        #adds the volunteer to the list with all the generated data
        list_volunteers.append(Volunteer(i,Name, exp,prefnum,tempnumber,AvailDict))
    VolunteerJson(list_volunteers, folder_path)
    return list_volunteers


def deleteContents(path):
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

# For each saved volunteer json file, compile their details into a Volunteer object, return a list of all these Volunteer objects
def LoadVolunteers(folder_path):
    list_volunteers = []
    # Get all files in path
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Load file, Convert to Volunteer, and append to list
        with open(file_path, 'r') as f:
            contents = json.load(f)
            file_volunteer = Volunteer(
                contents['id'], 
                contents['name'], 
                contents['Explvl'], 
                contents['prefHours'], 
                contents['phonenumber'], 
                contents['Availability']
            )
            list_volunteers.append(file_volunteer)
    return list_volunteers

def SetVolunteerNumber(folder_path, number, regenerate):
    if regenerate:
        VolunteerGenerate(number, folder_path)
        print("Generated new volunteers")
    else:
        number_volunteers = len(os.listdir(folder_path))
        if number_volunteers is not number:
            VolunteerGenerate(number, folder_path)
            print("Generated new volunteers")
