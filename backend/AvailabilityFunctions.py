#Generates a random Availability
from backend.DataGenerator import *
import random

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