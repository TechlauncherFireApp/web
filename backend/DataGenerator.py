import random
from enum import Enum
import json


# returns a list populated with the the hours in a week to be scheduled
from backend.Names import firstNames, lastNames


def shiftpopulator():
    list = []
    # weeknumber can be added if need be by adding an extra forloop and the code could be very similar to the hours
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    blocks = range(48)
    for i in days:
        for j in blocks:
            # concatenating the day string with the hour to generate the label for an hour that is to be scheduled
            list.append(i + str(j))
    return list

def NumberGenerator():
    tempnumber = "04"
    for j in range(8):
        tempnumber += str(random.randint(0, 9))
    return tempnumber
#Generates a random Availability
def randomAvailabilityGenerator():
    AvailDict = {}
    for i in shiftpopulator():
        AvailDict[i] = False

        # generates a 0 or 1 and that gets converted to true or false using an if function
        if (int)(random.randrange(0, 12, 2) / 10) == 1:
            AvailDict[i] = True
    return AvailDict
#A more realistic availability
#an availability for all the timeblocks is returned
def SmarterAvailabilityGenerator():
    AvailDict = {}
    #i is a string format Monx/x
    for i in shiftpopulator():
        #equates to a True 2/7 on average
        decisionVar=random.randrange(0, 12, 2) / 10
        if(i[0:3]=="Mon" or i[0:3]=="Tue" or i[0:3]=="Wed" or i[0:3]=="Thu" or i[0:3]=="Fri"):
            #int(i[3:5] gives us the block number in integer form 34 coressponds to 5pm
            #46 coressponds to 11pm
            if(int(i[3:5])>=34 and int(i[3:5])<=46):
                #equates to a True 5/7 on average
                decisionVar*=2.5
                #9am to 4:59pm
            elif(int(i[3:5])>=18 and int(i[3:5])<=32):
                #equates to a True 4/7 on average
                decisionVar*=2
            # for 0 to 8 a decision is made using the generated number without multipliers
        #covers Saturday and Sunday
        else:
            #8am to 11pm
            if (int(i[3:5]) >= 16 and int(i[3:5]) <= 46):
                #equates to a True 5/7 on average
                decisionVar *= 2.5
            #for 0 to 8 a decision is made using the generated number without multipliers so the else function
            #is implicit
        #the dictionary is assigned True or False
        if(decisionVar<1):
            AvailDict[i]=False
        else:
            AvailDict[i]=True
    return AvailDict
#Splits the days into chunks and generates availabilities
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
    basic = "Basic"
    advanced = "Advanced"
# each volunteer has an Name,Experience level, preferred Hours, Availability
# is availability different
class Volunteer:
    def __init__(self, name, Explvl, prefHours,phonenumber,Availability):
        self.name = name
        self.Explvl = Explvl
        self.prefHours = prefHours
        self.phonenumber=phonenumber
        self.Availability = Availability

#Randomly generating a group of different Volunteers
#THIS FUNCTION OCCASIONALLY ATTEMPTS TO ACCESS AN OUT OF BOUNDS INDEX, around line 110
def volunteerGenerate(volunteerNo):
    list = []
    #generates twice as many advanced firefighters as basic
    for i in range(volunteerNo):
        #Generates a random name from the pool available
        Name=firstNames[random.randint(0,len(firstNames))]+" "+lastNames[random.randint(0,len(lastNames))]
        #Generates an experience at a ratio i.e how many more basic firefighters than advanced
        #for example 3 means 3 times as many advanced firefighters are
        ratio=3
        expgenerator=random.randint(1, ratio)
        exp="Advanced"
        if(expgenerator<ratio):
            exp="Basic"
        #preferred hours between 6 and 14
        prefnum=random.randint(6, 14)
        #Generates an Availability
        AvailDict = AvailabilityGenerator()


        #generates a random australian phone number
        tempnumber = NumberGenerator()
        #adds the volunteer to the list with all the generated data
        list.append(Volunteer(Name, exp,prefnum,tempnumber,AvailDict))
    return list

def VolunteerTest(number):
    Volunteers=volunteerGenerate(number)
    for i in Volunteers:
            print("Name: "+ i.name)
            print("preferred Hours: "+str(i.prefHours))
            print("Experience level: "+str(i.Explvl))
            print("Phone Number: "+i.phonenumber)
            print("Availability: ")
            for j in shiftpopulator():
                print(j+": "+str(i.Availability[j]))
            print("\n")
#generates number volunteers in the volunteers folder
def VolunteerJson(number):
    Volunteers=volunteerGenerate(number)
    j=0
    for i in Volunteers:
        with open('Volunteers/'+'Volunteer'+str(j)+'.json', 'w') as fp:
            json.dump(i.__dict__, fp)
        j += 1




VolunteerJson(3)


# Model
#m = gp.Model("assignment")