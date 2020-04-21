import gurobipy as gp
import random
from gurobipy import GRB
import sys
from enum import Enum
#taken from https://gist.github.com/benhorgen/4494868
firstNames = ["Adam", "Alex", "Aaron", "Ben", "Carl", "Dan", "David", "Edward", "Fred", "Frank", "George", "Hal", "Hank", "Ike",
 "John", "Jack", "Joe", "Larry", "Monte", "Matthew", "Mark", "Nathan", "Otto", "Paul", "Peter", "Roger", "Roger",
 "Steve", "Thomas", "Tim", "Ty", "Victor", "Walter"]

lastNames =["Anderson", "Ashwoon", "Aikin", "Bateman", "Bongard", "Bowers", "Boyd", "Cannon", "Cast", "Deitz", "Dewalt", "Ebner",
 "Frick", "Hancock", "Haworth", "Hesch", "Hoffman", "Kassing", "Knutson", "Lawless", "Lawicki", "Mccord", "McCormack",
 "Miller", "Myers", "Nugent", "Ortiz", "Orwig", "Ory", "Paiser", "Pak", "Pettigrew", "Quinn", "Quizoz", "Ramachandran",
 "Resnick", "Sagar", "Schickowski", "Schiebel", "Sellon", "Severson", "Shaffer", "Solberg", "Soloman", "Sonderling",
 "Soukup", "Soulis", "Stahl", "Sweeney", "Tandy", "Trebil", "Trusela", "Trussel", "Turco", "Uddin", "Uflan", "Ulrich",
 "Upson", "Vader", "Vail", "Valente", "Van Zandt", "Vanderpoel", "Ventotla", "Vogal", "Wagle", "Wagner", "Wakefield",
 "Weinstein", "Weiss", "Woo", "Yang", "Yates", "Yocum", "Zeaser", "Zeller", "Ziegler", "Bauer", "Baxster", "Casal",
 "Cataldi", "Caswell", "Celedon", "Chambers", "Chapman", "Christensen", "Darnell", "Davidson", "Davis", "DeLorenzo",
 "Dinkins", "Doran", "Dugelman", "Dugan", "Duffman", "Eastman", "Ferro", "Ferry", "Fletcher", "Fietzer", "Hylan",
 "Hydinger", "Illingsworth", "Ingram", "Irwin", "Jagtap", "Jenson", "Johnson", "Johnsen", "Jones", "Jurgenson",
 "Kalleg", "Kaskel", "Keller", "Leisinger", "LePage", "Lewis", "Linde", "Lulloff", "Maki", "Martin", "McGinnis",
 "Mills", "Moody", "Moore", "Napier", "Nelson", "Norquist", "Nuttle", "Olson", "Ostrander", "Reamer", "Reardon",
 "Reyes", "Rice", "Ripka", "Roberts", "Rogers", "Root", "Sandstrom", "Sawyer", "Schlicht", "Schmitt", "Schwager",
 "Schutz", "Schuster", "Tapia", "Thompson", "Tiernan", "Tisler"]


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
    def __init__(self, name, Explvl, prefHours,phonenumber,Availability):
        self.name = name
        self.Explvl = Explvl
        self.prefHours = prefHours
        self.phonenumber=phonenumber
        self.Availability = Availability

def NumberGenerator():
    tempnumber = "04"
    for j in range(8):
        tempnumber += str(random.randint(0, 10))
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
    decisionThreshold=0
    #i is a string format Monx/x
    for i in shiftpopulator():
        decisionVar=random.randrange(0, 12, 2) / 10
        if(i[0:3]=="Mon" or i[0:3]=="Tue" or i[0:3]=="Wed" or i[0:3]=="Thu" or i[0:3]=="Fri"):
            #int(i[3:5] gives us the time in integer form
            if(int(i[3:5])>=17 and int(i[3:5])<=23):
                decisionVar*=2.5
            elif(int(i[3:5])>=7 and int(i[3:5])<=16):
                decisionVar*=2
            # for 0 to 8 a decision is made using the generated number without multipliers
        #covers Saturday and Sunday
        else:
            if (int(i[3:5]) >= 8 and int(i[3:5]) <= 23):
                decisionVar *= 2.5
            #for 0 to 8 a decision is made using the generated number without multipliers so the else function
            #is implicit
        #the dictionary is assigned True or False
        if(decisionVar<1):
            AvailDict[i]=False
        else:
            AvailDict[i]=True
    return AvailDict
#Randomly generating a group of different Volunteers
def volunteerGenerate(volunteerNo):
    list = []
    #generates twice as many advanced firefighters as basic
    for i in range(volunteerNo):
        #Generates a random name from the pool available
        Name=firstNames[random.randint(0,32)]+" "+lastNames[random.randint(0,150)]
        #Generates an experience at a ratio i.e how many more basic firefighters than advanced
        #for example 3 means 3 times as many advanced firefighters are
        ratio=3
        expgenerator=random.randint(1, ratio)
        exp=FireFighter.advanced
        if(expgenerator<ratio):
            exp=FireFighter.basic
        #preferred hours between 6 and 14
        prefnum=random.randint(6, 14)
        #Generates an Availability
        AvailDict = SmarterAvailabilityGenerator()


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

VolunteerTest(2)


# Model
#m = gp.Model("assignment")