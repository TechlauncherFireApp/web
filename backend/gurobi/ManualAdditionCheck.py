from backend.gurobi.Scheduler import *

def NameToAsset(Name):
    if(Name=="Light Unit"):
        return LightUnit
    if(Name=="Medium Tanker"):
        return MediumTanker
    if(Name=="Heavy Tanker"):
        return HeavyTanker



def ManualAdditionCheck(asset_request, assigned_volunteers):
    # for vehicle in RecommendationList:
    #Loading the type of vehicle
    Type=asset_request.AssetType
    TotalNum=0
    AdvancedNum=0
    DriverNum=0
    CrewLeaderNum=0

    for Vol in assigned_volunteers:

        #adds one to the total
        TotalNum+=1
        if (Vol.Explvl == FireFighter.basic.value):
            print(Vol.Explvl)
            #if Volunteer assigned to a job they're not qualified for
            if(Vol.role!="Crew Member"):
                print(Vol.name+ " id "+str(Vol.id)+" not qualified for "+Vol.role)
                return False,Vol.name+ " id "+str(Vol.id)+" not qualified for "+Vol.role

        if (Vol.Explvl == FireFighter.advanced.value):
            AdvancedNum += 1
            #if Volunteeer assigned to a job they're not qualified for
            if(Vol.role!="Crew Member"):
                print(Vol.name+ " id "+str(Vol.id)+" not qualified for "+Vol.role)
                return False,Vol.name+ " id "+str(Vol.id)+" not qualified for "+Vol.role

        if(Vol.Explvl == FireFighter.crewleader.value):
            CrewLeaderNum += 1

        if (Vol.Explvl == FireFighter.driver.value):
            DriverNum += 1
            # if Volunteeer assigned to a job they're not qualified for
            if (Vol.role == "CrewLeader" or Vol.role == "CrewLeader/Driver"):
                print(Vol.name + " id " + str(Vol.id) + " not qualified for " + Vol.role)
                return False,Vol.name + " id " + str(Vol.id) + " not qualified for " + Vol.role


    #if theres too many
    if(Type.TotalReq < TotalNum):
        print("There are not enough volunteers on "+asset_request.AssetType+" on Request Number "+str(asset_request.RequestNo))
        return False,"There are not enough volunteers on "+asset_request.AssetType+" on Request Number "+str(asset_request.RequestNo)
    # if theres too few
    if (Type.TotalReq > TotalNum):
        print("There are too many  volunteers on " + asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo))
        return False,"There are too many  volunteers on " + asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo)
    #checks number of CrewLeaders
    if (Type.CrewLeaderReq > CrewLeaderNum):
        print(asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo)+"does not have a CrewLeader")
        return False, asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo)+"does not have a CrewLeader"

    #Checks Number of drivers
    if (Type.DriverReq > CrewLeaderNum + DriverNum):
        print(asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo) + "does not have a Driver")
        return False, asset_request.AssetType + " on Request Number " + str(
            asset_request.RequestNo) + "does not have a Driver"
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