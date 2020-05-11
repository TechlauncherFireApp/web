from gurobi.AssetTypes import *
from gurobi.Scheduler import *

# File for testing guobi backend functions
# Moved the test code here so that the api interface doesn't run it

# For AssetTypes
def Test(Request):
    # A List of Requests
    for i in RequesttoRequirements(Request).keys():
        print(str(i) + ": " + str(RequesttoRequirements(Request)[i]))

Test(EveryWeekday)

# For Scheduler
print(Schedule(v, EveryWeekday))
