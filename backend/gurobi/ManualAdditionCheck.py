from backend.gurobi.Scheduler import *

def NameToAsset(Name):
    if(Name=="Light Unit"):
        return LightUnit
    if(Name=="Medium Tanker"):
        return MediumTanker
    if(Name=="Heavy Tanker"):
        return HeavyTanker



def ManualAdditionCheck(RecommendationList):
    for vehicle in RecommendationList:
        #Loading the type of vehicle
        Type=NameToAsset(vehicle["asset_class"])
        TotalNum=0
        AdvancedNum=0
        DriverNum=0
        CrewLeaderNum=0



        for Vol in vehicle["volunteers"]:
            #adds one to the total
            TotalNum+=1
            if (Vol["volunteer_explvl"] == FireFighter.basic.value):
                #if Volunteer assigned to a job they're not qualified for
                if(Vol['role']!="Crew Member"):
                    print(Vol["volunteer_name"]+ " id "+str(Vol["volunteer_id"])+" not qualified for "+Vol['role'])
                    return False,Vol["volunteer_name"]+ " id "+str(Vol["volunteer_id"])+" not qualified for "+Vol['role']

            if (Vol["volunteer_explvl"] == FireFighter.advanced.value):
                AdvancedNum += 1
                #if Volunteeer assigned to a job they're not qualified for
                if(Vol['role']!="Crew Member"):
                    print(Vol["volunteer_name"]+ " id "+str(Vol["volunteer_id"])+" not qualified for "+Vol['role'])
                    return False,Vol["volunteer_name"]+ " id "+str(Vol["volunteer_id"])+" not qualified for "+Vol['role']

            if(Vol["volunteer_explvl"]==FireFighter.crewleader.value):
                CrewLeaderNum += 1

            if (Vol["volunteer_explvl"] == FireFighter.driver.value):
                DriverNum += 1
                # if Volunteeer assigned to a job they're not qualified for
                if (Vol['role'] == "Crew Leader" or Vol['role'] == "CrewLeader/Driver"):
                    print(Vol["volunteer_name"] + " id " + str(Vol["volunteer_id"]) + " not qualified for " + Vol[
                        'role'])
                    return False,Vol["volunteer_name"] + " id " + str(Vol["volunteer_id"]) + " not qualified for " + Vol[
                        'role']


        #if theres too many
        if(Type.TotalReq < TotalNum):
            print("There are not enough volunteers on "+vehicle["asset_class"].type+" on Request Number "+str(vehicle["asset_id"]))
            return False,"There are not enough volunteers on "+vehicle["asset_class"].type+" on Request Number "+str(vehicle["asset_id"])
        # if theres too few
        if (Type.TotalReq > TotalNum):
            print("There are too many  volunteers on " + vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"]))
            return False,"There are too many  volunteers on " + vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"])
        #checks number of CrewLeaders
        if (Type.CrewLeaderReq > CrewLeaderNum):
            print(vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"])+"does not have a CrewLeader")
            return False, vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"])+"does not have a CrewLeader"

        #Checks Number of drivers
        if (Type.DriverReq > CrewLeaderNum + DriverNum):
            print(vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"]) + "does not have a Driver")
            return False, vehicle["asset_class"].type + " on Request Number " + str(
                vehicle["asset_id"]) + "does not have a Driver"
            #  AdvancedReq
            # TotalReq
            # self.CrewLeaderReq = CrewLeaderReq
            # self.DriverReq = DriverReq
    #If none of hte conditions are breached return True
    print("Valid Assignment")
    return True,"Valid Assignment"

#Below is how I tested it
# Reco,Volly=Schedule(VolunteerGenerate(1000,"Volunteers"),EveryWeekday)
# ManualAdditionCheck(Reco)