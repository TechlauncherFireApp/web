from enum import Enum

#establishing the  types of Firefighters
class FireFighter(Enum):
    advanced = "Advanced"
    basic = "Basic"
    crewleader="Crew Leader"
    driver="Driver"

#A class representing the requirement of the vehicles
class Vehicle():
    def __init__(self, type, TotalReq, AdvancedReq,CrewLeaderReq,DriverReq):
        self.type = type
        self.AdvancedReq = AdvancedReq
        self.TotalReq = TotalReq
        self.CrewLeaderReq=CrewLeaderReq
        self.DriverReq=DriverReq


# Converts the qualifications and years of experiences into roles they can perform
def QualificationtoRoleqaulification(Years, QualificationBoolean):
    if (Years >= 3 and QualificationBoolean["Advanced Firefighting Qualification"]):
        if (Years >= 4 and QualificationBoolean["Crew Leader Course"]):
            if (QualificationBoolean["Heavy Rigid Vehicle License"]
                    and QualificationBoolean["Tanker Driving training"]
                    and QualificationBoolean["Urgent Duty Driving Training"]
                    and QualificationBoolean["Advanced Pumping Skills"]):
                return FireFighter.driver
            else:
                return FireFighter.crewleader
        return FireFighter.advanced
    else:
        return FireFighter.basic


# The Fleet
LightUnit = Vehicle( "Light Unit", 2, 1,1,0)
MediumTanker = Vehicle( "Medium Tanker", 3, 0,1,1)
HeavyTanker = Vehicle( "Heavy Tanker", 5, 2,1,1)


# StartTime and Duration in timeblocks
class Request():
    def __init__(self,RequestNo, AssetType, StartTime, EndTime):
        self.RequestNo=RequestNo
        self.AssetType = AssetType
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Duration = EndTime - StartTime



def RequesttoRequirements(Requests):
    """Takes in a list of Requests as an input and then generates a dictionary with Timeblock as the key and a tuple of
     (TotalRequired,AdvancedRequired)"""
    TotalRequirementDict = {}
    AdvancedRequirementDict = {}
    CrewLeaderRequirementDict={}
    DriverRequirementDict={}
    for l in Requests:
        # This ensures we fill up all the hours that run between the starttime and the duration with the information
        # about the advanced and basic requirements
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in TotalRequirementDict:
                TotalRequirementDict[k] = l.AssetType.TotalReq
            else:
                # print("gets here")
                TotalRequirementDict[k] += l.AssetType.TotalReq
    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in AdvancedRequirementDict:
                AdvancedRequirementDict[k] = l.AssetType.AdvancedReq
            else:
                # print("gets here")
                AdvancedRequirementDict[k] += l.AssetType.AdvancedReq

    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in CrewLeaderRequirementDict:
                CrewLeaderRequirementDict[k] = l.AssetType.CrewLeaderReq
            else:
                # print("gets here")
                CrewLeaderRequirementDict[k] += l.AssetType.CrewLeaderReq

    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in DriverRequirementDict:
                DriverRequirementDict[k] = l.AssetType.DriverReq
            else:
                # print("gets here")
                DriverRequirementDict[k] += l.AssetType.DriverReq

    # the following code combines the two dictionaries and gives us the tuple form
    ds = [TotalRequirementDict, AdvancedRequirementDict,CrewLeaderRequirementDict,DriverRequirementDict]
    resultDict = {}
    for k in TotalRequirementDict.keys():
        resultDict[k] = tuple(d[k] for d in ds)

    return resultDict


# Request Scenarios
# 1700 monday onwards for 6.5hours
SingleRequest = [Request(1,LightUnit, 34, 47)]

# 1700 monday onwards for 6.5hours but two asset types
TwoAssetTypeRequest = [Request(1,LightUnit, 34, 47), Request(2,MediumTanker, 34, 47)]

# Multiple Days
MultipleDaysRequest = [Request(1,LightUnit, 34, 48), Request(2,MediumTanker, 34, 48)
    , Request(3,MediumTanker, 82, 96), Request(4,HeavyTanker, 82, 96)]

# OnlyWeekends
OnlyWeekends = [Request(11,MediumTanker, 18 + 5 * 48, 18 + 5 * 48+24), Request(12,LightUnit, 18 + 5 * 48, 18 + 5 * 48+24),
                Request(13,MediumTanker, 18 + 6 * 48,18 + 6 * 48+ 10), Request(14,LightUnit, 18 + 6 * 48,18 + 6 * 48+ 24)]
# All Weekdays
EveryWeekday = [Request(1,LightUnit, 34, 47), Request(2,MediumTanker, 34, 47)
    , Request(3,MediumTanker, 82, 95), Request(4,HeavyTanker, 82, 95),
                Request(5,MediumTanker, 34 + 2 * 48, 34 + 2 * 48+13), Request(6,HeavyTanker, 34 + 2 * 48, 34 + 2 * 48+13),
                Request(7,MediumTanker, 34 + 3 * 48, 34 + 3 * 48 + 13), Request(8,HeavyTanker, 34 + 3 * 48, 34 + 3 * 48 + 13),
                Request(9,MediumTanker, 34 + 4 * 48, 34 + 4 * 48 + 13), Request(10,LightUnit, 34 + 4 * 48, 34 + 4 * 48 + 13)
                ]
# All Days of the week
# This one is only weekends and EveryWeekday combined
EveryDayOfTheWeek = EveryWeekday+OnlyWeekends