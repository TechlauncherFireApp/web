import random
import services.gurobi.data_generator as dg


def random_availability_generator():
    available_dict = {}
    for i in dg.shift_populator():
        available_dict[i] = False

        # generates a 0 or 1 and that gets converted to true or false using an if function
        if (int)(random.randrange(0, 12, 2) / 10) == 1:
            available_dict[i] = True
    return available_dict


# A more realistic availability
# an availability for all the timeblocks is returned
def smarter_availability_generator():
    available_dict = {}
    # i is a string format Monx/x
    for i in dg.shift_populator():
        # equates to a True 2/7 on average
        decision = random.randrange(0, 12, 2) / 10
        if i[0:3] == "Mon" or i[0:3] == "Tue" or i[0:3] == "Wed" or i[0:3] == "Thu" or i[0:3] == "Fri":
            # int(i[3:5] gives us the block number in integer form 34 coressponds to 5pm
            # 46 corresponds to 11pm
            if int(i[3:5]) >= 34 and int(i[3:5]) <= 46:
                # equates to a True 5/7 on average
                decision *= 2.5
                # 9am to 4:59pm
            elif 18 <= int(i[3:5]) <= 32:
                # equates to a True 4/7 on average
                decision *= 2
            # for 0 to 8 a decision is made using the generated number without multipliers
        # covers Saturday and Sunday
        else:
            # 8am to 11pm
            if 16 <= int(i[3:5]) <= 46:
                # equates to a True 5/7 on average
                decision *= 2.5
            # for 0 to 8 a decision is made using the generated number without multipliers so the else function
            # is implicit
        # the dictionary is assigned True or False
        if decision < 1:
            available_dict[i] = False
        else:
            available_dict[i] = True
    return available_dict
