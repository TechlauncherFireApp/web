import random
import datetime
from backend.gurobi.DataGenerator import *
from backend.gurobi.Scheduler import *
#Simpler datageneration
#returns true Percent% of the time
def booleangenerator(Percent):
    if(Percent>=random.randint(1, 100)):
        return True
    else:
        return False
#use datagenerator change volunteers into dictionary


def SimpleVolunteerGenerate(Number):
    Volunteers=list()
    for i in range(Number):
        volunteer=dict()
        volunteer["ID"]=i
        volunteer["prefHours"]=random.randint(6, 14)
        volunteer["possibleRoles"]=["basic"]
        if(booleangenerator(40)):
            volunteer["possibleRoles"].append("advanced")
        if (booleangenerator(30)):
            volunteer["possibleRoles"].append("crewLeader")
        if (booleangenerator(20)):
            volunteer["possibleRoles"].append("driver")

        volunteer["availabilities"]=AvailabilityGenerator()
        Volunteers.append(volunteer)
    return Volunteers

#The request dictionary for A request with only one Assetclass
SingleRequest = [{'shiftID':0,'assetClass':'lightUnit',
                      'timeframe':(next_monday()+datetime.timedelta(hours=17),next_monday()+datetime.timedelta(hours=24))}]
#The volunteer dictionary for A request with only one Assetclas
SingleRequestVolunteers=[{'ID':0,'prefhours':7,
                          'possibleroles':['advanced'],
                          'availabilities':[(next_monday()+datetime.timedelta(hours=17),next_monday()+datetime.timedelta(hours=24))]},
                         {'ID': 1, 'prefhours': 7,
                          'possibleroles': ['crewLeader','driver'],
                          'availabilities': [(next_monday() + datetime.timedelta(hours=17),
                                              next_monday() + datetime.timedelta(hours=24))]}
                         ]

def SingleTest():
    Results=Schedule(SingleRequestVolunteers,SingleRequest)
    for result in Results:
        #Will return Assertion Errors if the criteria is not met exactly.
        assert(result['shiftID']==0)
        assert (result['assetClass'] == SingleRequest['assetClass'])
        assert (result['timeframe']==SingleRequest['timeframe'])
        assert(result['volunteers'][0]['ID']==1 and result['volunteers'][0]['role']==['driver','crewLeader'])
        assert (result['volunteers'][1]['ID'] == 0 and result['volunteers'][0]['role'] == ['advanced'])
    print("Passed")
# 1700 monday onwards for 6.5hours but two asset types
TwoAssetTypeRequest=[{'shiftID':0,'assetClass':'lightUnit',
                      'timeframe':(next_monday()+datetime.timedelta(hours=17),next_monday()+datetime.timedelta(hours=24))},
                     {'shiftID': 1, 'assetClass': 'mediumTanker',
                      'timeframe': (
                      next_monday() + datetime.timedelta(hours=41), next_monday() + datetime.timedelta(hours=48))},
                     ]

TwoAssetTypeRequestVolunteers=[{'id':0,'prefhours':7,
                          'possibleroles':['advanced'],
                          'availabilities':[(next_monday()+datetime.timedelta(hours=17),next_monday()+datetime.timedelta(hours=24))]},
                         {'id': 1, 'prefhours': 7,
                          'possibleroles': ['crewLeader','driver'],
                          'availabilities': [(next_monday() + datetime.timedelta(hours=17),
                                              next_monday() + datetime.timedelta(hours=24))]},
                               {'id': 2, 'prefhours': 7,
                          'possibleroles': ['crewLeader'],
                          'availabilities': [(next_monday() + datetime.timedelta(hours=41),
                                              next_monday() + datetime.timedelta(hours=48))]},
{'id': 3, 'prefhours': 7,
                          'possibleroles': ['driver'],
                          'availabilities': [(next_monday() + datetime.timedelta(hours=41),
                                              next_monday() + datetime.timedelta(hours=48))]},
{'id': 4, 'prefhours': 7,
                          'possibleroles': ['basic'],
                          'availabilities': [(next_monday() + datetime.timedelta(hours=41),
                                              next_monday() + datetime.timedelta(hours=48))]}

                         ]

