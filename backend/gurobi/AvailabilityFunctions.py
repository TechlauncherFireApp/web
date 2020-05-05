#Generates a random Availability
import random
import backend.gurobi.DataGenerator as dg

def randomAvailabilityGenerator():
    AvailDict = {}
    for i in dg.shiftpopulator():
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
    for i in dg.shiftpopulator():
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
