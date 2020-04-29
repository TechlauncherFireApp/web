from enum import Enum


# class Asset(Enum):
#     LightUnit="LU"
#     MediumUnit = "MU"
#     HeavyUnit= "HU"




class Asset():
    def __init__(self, name,TotalReq,AdvancedReq):
        self.name = name
        self.AdvancedReq = AdvancedReq
        self.TotalReq = TotalReq

#the AssetTypes
LightUnit = Asset("Light Unit",3,3)
MediumTanker= Asset("Medium Tanker",3,2)
HeavyTanker=Asset("Heavy Tanker",5,4)

#StartTime and Duration in timeblocks
class Request():
    def __init__(self, AssetType, StartTime, Duration):
        self.AssetType = AssetType
        self.StartTime = StartTime
        self.Duration = Duration




def RequesttoRequirements(Requests):
    """Takes in a list of Requests as an input and then generates a dictionary with Timeblock as the key and a tuple of
     (TotalRequired,AdvancedRequired)"""
    TotalRequirementDict = {}
    AdvancedRequirementDict={}
    for l in Requests:
        #This ensures we fill up all the hours that run between the starttime and the duration with the information
        #about the advanced and basic requirements
        for k in range(l.StartTime, l.StartTime + l.Duration + 1):
            #checks if
            if k not in TotalRequirementDict:
                TotalRequirementDict[k] = l.AssetType.TotalReq
            else:
                #print("gets here")
                TotalRequirementDict[k] += l.AssetType.TotalReq
    for l in Requests:
        for k in range(l.StartTime, l.StartTime + l.Duration + 1):
            #checks if
            if k not in AdvancedRequirementDict:
                AdvancedRequirementDict[k] = l.AssetType.AdvancedReq
            else:
                #print("gets here")
                AdvancedRequirementDict[k] += l.AssetType.AdvancedReq


    #the following code combines the two dictionaries and gives us the tuple form
    ds = [TotalRequirementDict, AdvancedRequirementDict]
    resultDict = {}
    for k in TotalRequirementDict.keys():
        resultDict[k] = tuple(d[k] for d in ds)

    return resultDict

#1700 monday onwards for 6.5hours
SingleRequest=[Request(LightUnit, 34, 13)]
#1700 monday onwards for 6.5hours but two asset types
TwoAssetTypeRequest=[Request(LightUnit, 34, 13),Request(MediumTanker, 34, 13)]
#Multiple Days
MultipleDaysRequest = [Request(LightUnit, 34, 13),Request(MediumTanker, 34, 13)
    , Request(MediumTanker, 82, 13), Request(HeavyTanker, 82, 13)]
def Test():
    # A List of Requests

    for i in range(25):
        print(str(i)+": "+str(RequesttoRequirements(MultipleDaysRequest)[i]))


