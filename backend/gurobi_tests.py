from gurobi.AssetTypes import *
from gurobi.Scheduler import *
from gurobi.DataGenerator import *

# File for testing guobi backend functions
# Moved the test code here so that the api interface doesn't run it

# For AssetTypes
def Test(Request):
    # A List of Requests
    for i in RequesttoRequirements(Request).keys():
        print(str(i) + ": " + str(RequesttoRequirements(Request)[i]))

# Test(EveryWeekday)

# For Scheduler
# print(Schedule(v, EveryWeekday))


# For DataGenerator
def VolunteerTest(number):
    Volunteers=VolunteerGenerate(number, 'volunteers')
    for i in Volunteers:
            print("ID: " + str(i.id))
            print("Name: "+ i.name)
            print("preferred Hours: "+str(i.prefHours))
            print("Experience level: "+str(i.Explvl))
            print("Phone Number: "+i.phonenumber)
            print("Availability: ")
            # for j in shiftpopulator():
            #     print(j+": "+str(i.Availability[j]))
            print("\n")

# VolunteerTest(200)
# LoadVolunteers('volunteers')