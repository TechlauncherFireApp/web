
# TO-DO
# Pass the asset request Number into LicenseNo and change the name to something more instructive perhaps


class Asset():
    def __init__(self, LicenseNo, type, TotalReq, AdvancedReq):
        self.LicenceNo = LicenseNo
        # no use now just there for informations sake
        self.type = type
        self.AdvancedReq = AdvancedReq
        self.TotalReq = TotalReq

class Vehicle():
    def __init__(self, type, TotalReq, AdvancedReq,CrewLeaderReq,DriverReq):
        # no use now just there for informations sake
        self.type = type
        self.AdvancedReq = AdvancedReq
        self.TotalReq = TotalReq
        self.CrewLeaderReq=CrewLeaderReq
        self.DriverReq=DriverReq

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
# All Days of hte week
##solves all but this one with 60 volunteers generated it solved with 90 though
# This one is only weekends and EveryWeekday combined
EveryDayOfTheWeek = EveryWeekday+OnlyWeekends


def Test(Request):
    # A List of Requests
    for i in RequesttoRequirements(Request).keys():
        print(str(i) + ": " + str(RequesttoRequirements(Request)[i]))

