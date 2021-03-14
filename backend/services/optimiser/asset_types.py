from enum import Enum


# establishing the  types of Firefighters
class FireFighter(Enum):
    advanced = "Advanced"
    basic = "Basic"
    crewleader = "Crew Leader"
    driver = "Driver"


# A class representing the requirement of the vehicles
class Vehicle():
    def __init__(self, type, TotalReq, AdvancedReq, CrewLeaderReq, DriverReq):
        self.type = type
        self.AdvancedReq = AdvancedReq
        self.TotalReq = TotalReq
        self.CrewLeaderReq = CrewLeaderReq
        self.DriverReq = DriverReq


# Converts the qualifications and years of experiences into roles they can perform
def qualification_to_role_qualification(years, qualification_boolean):
    if years >= 3 and qualification_boolean["Advanced Firefighting Qualification"]:
        if years >= 4 and qualification_boolean["Crew Leader Course"]:
            if (qualification_boolean["Heavy Rigid Vehicle License"]
                    and qualification_boolean["Tanker Driving training"]
                    and qualification_boolean["Urgent Duty Driving Training"]
                    and qualification_boolean["Advanced Pumping Skills"]):
                return FireFighter.driver
            else:
                return FireFighter.crewleader
        return FireFighter.advanced
    else:
        return FireFighter.basic


# The Fleet
LightUnit = Vehicle("Light Unit", 2, 1, 1, 0)
MediumTanker = Vehicle("Medium Tanker", 3, 0, 1, 1)
HeavyTanker = Vehicle("Heavy Tanker", 5, 2, 1, 1)


# StartTime and Duration in timeblocks
class Request():
    def __init__(self, RequestNo, AssetType, StartTime, EndTime):
        self.RequestNo = RequestNo
        self.AssetType = AssetType
        self.StartTime = StartTime
        self.EndTime = EndTime
        self.Duration = EndTime - StartTime


def request_to_requirements(Requests):
    """Takes in a list of Requests as an input and then generates a dictionary with Timeblock as the key and a tuple of
     (TotalRequired,AdvancedRequired)"""
    total_requirements = {}
    advanced_requirements = {}
    crew_leader_requirements = {}
    driver_requirements = {}
    for l in Requests:
        # This ensures we fill up all the hours that run between the starttime and the duration with the information
        # about the advanced and basic requirements
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in total_requirements:
                total_requirements[k] = l.AssetType.TotalReq
            else:
                # print("gets here")
                total_requirements[k] += l.AssetType.TotalReq
    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in advanced_requirements:
                advanced_requirements[k] = l.AssetType.AdvancedReq
            else:
                # print("gets here")
                advanced_requirements[k] += l.AssetType.AdvancedReq

    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in crew_leader_requirements:
                crew_leader_requirements[k] = l.AssetType.CrewLeaderReq
            else:
                # print("gets here")
                crew_leader_requirements[k] += l.AssetType.CrewLeaderReq

    for l in Requests:
        for k in range(l.StartTime, l.EndTime):
            # checks if
            if k not in driver_requirements:
                driver_requirements[k] = l.AssetType.DriverReq
            else:
                # print("gets here")
                driver_requirements[k] += l.AssetType.DriverReq

    # the following code combines the two dictionaries and gives us the tuple form
    ds = [total_requirements, advanced_requirements, crew_leader_requirements, driver_requirements]
    resultDict = {}
    for k in total_requirements.keys():
        resultDict[k] = tuple(d[k] for d in ds)

    return resultDict


# Request Scenarios
# 1700 monday onwards for 6.5hours
SingleRequest = [Request(1, LightUnit, 34, 47)]

# 1700 monday onwards for 6.5hours but two asset types
TwoAssetTypeRequest = [Request(1, LightUnit, 34, 47), Request(2, MediumTanker, 34, 47)]

# Multiple Days
MultipleDaysRequest = [Request(1, LightUnit, 34, 48), Request(2, MediumTanker, 34, 48)
    , Request(3, MediumTanker, 82, 96), Request(4, HeavyTanker, 82, 96)]

# OnlyWeekends
OnlyWeekends = [Request(11, MediumTanker, 18 + 5 * 48, 18 + 5 * 48 + 24),
                Request(12, LightUnit, 18 + 5 * 48, 18 + 5 * 48 + 24),
                Request(13, MediumTanker, 18 + 6 * 48, 18 + 6 * 48 + 10),
                Request(14, LightUnit, 18 + 6 * 48, 18 + 6 * 48 + 24)]
# All Weekdays
EveryWeekday = [Request(1, LightUnit, 34, 47), Request(2, MediumTanker, 34, 47)
    , Request(3, MediumTanker, 82, 95), Request(4, HeavyTanker, 82, 95),
                Request(5, MediumTanker, 34 + 2 * 48, 34 + 2 * 48 + 13),
                Request(6, HeavyTanker, 34 + 2 * 48, 34 + 2 * 48 + 13),
                Request(7, MediumTanker, 34 + 3 * 48, 34 + 3 * 48 + 13),
                Request(8, HeavyTanker, 34 + 3 * 48, 34 + 3 * 48 + 13),
                Request(9, MediumTanker, 34 + 4 * 48, 34 + 4 * 48 + 13),
                Request(10, LightUnit, 34 + 4 * 48, 34 + 4 * 48 + 13)
                ]
# All Days of the week
# This one is only weekends and EveryWeekday combined
EveryDayOfTheWeek = EveryWeekday + OnlyWeekends
