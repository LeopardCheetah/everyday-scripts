# generate list of tasks of what to do
# can be run infinitely, no need to worry about data corruption or anything

import os
import time

def clear():
    print('\033[2J\033[H')
    return 

# does s contain (char) x?
def contains(s, x):
    _x = str(x)
    if len(_x) < 1 or len(_x) > 1:
        return 'Perhaps'
    
    for i in s:
        if i == _x:
            return True

    return False 

# n = how many days ago do you want the date of 
def get_day(n):
    d = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24*60*60*n))
    return d

# path = path to the script date thing;
def get_habit_s(path):
    h = ''
    with open(path, 'r') as f:
        fl = False 
        for line in f:
            if fl:
                h = line[3:].strip()
                break

            # remember to sync this with tscr.py
            if line.strip() != 'Semi-daily habit tracker tracking portion (e.g. 11234567, 346):':
                continue 
            
            fl = True
            continue 
    
    return h

##############################
# 08/10 - rewrite parts of this from scratch + remove whatever file stuff i have going on right now

# which tt days do u wanna take a look at?
# from 3 days ago? 5? 7?
num_of_prev_days = 5

num_habits = 7 # manual count



# first row == first habit
# first col == most recent day (hopefully yesterday)
# e.g. 7x3:
# 0 1 0
# 1 1 1 
# 0 0 1
# 0 0 1
# 1 0 1
# 0 1 1
# 0 1 0 

arr = [[0 for __ in range(num_of_prev_days)] for _ in range(num_habits)]


for day in range(num_of_prev_days, 0, -1): # n/n-1/.../1 days ago time tracking scripts
    path = f'../time-tracker-2/day_recaps/{get_day(day)}.txt'

    habs = ''
    try:
        habs = get_habit_s(path)
    except:
        # path error since file doesn't exist
        habs = ':(' 
    
    # as of 08/10/2025 h can now contain:
    # 1 = brush (max: 2)
    # 2 = instrumenting
    # 3 = reading
    # 4 = coding (cp/projects)
    # 5 = mathing (analysis/comp. math)
    # 6 = showering
    # 7 = outsiding (biking/walking)

    # wlog assume the 1s are together
    for c in [1, 2, 3, 4, 5, 6, 7]:
        if contains(habs, c):
            # (habit, day num)
            arr[c - 1][day - 1] = 1
            continue 

    # last whatever's tt results have been tracked!


################
################
tasks = ["[Brush, Brush]", "Instrumenting", "Reading", "proging (CP/Projects)", "Mathing (Analysis/Comp. Math)", "Showering", "Outsiding"]

# do task i ind i times a day
# 2 -> this should be done once every 2 days
task_freq = [1, 1, 1, 1, 2, 2, 1]

# default ramp up will just be for every 2 days something isn't done, add an exclam
# x -> Code -> Code -> Code!
exclam_ramp_up = [2, 2, 2, 2, 2, 2, 2]



#############################
#############################

# carry over arr array
# verification
if len(arr) != len(tasks):
    print("something has gone wrong -- the number of tasks being tracked and the number of tasks that have been logged are different")
    print(f"Len of arr: {len(arr)}")
    print(f"Len of tasks: {len(tasks)}")
    raise Exception(':<')

daily_h_to_print = []

for i, v in enumerate(tasks):
    # see if task first needs to be done 
    if 1 in arr[i][:task_freq[i] - 1]:
        # since the task was done within <task_freq days 
        # we can skip the task
        # yay
        continue 

    # task needs to be added
    # how many exclams?
    _last = arr[i].index(1) if 1 in arr[i] else len(arr[i])
    _exclams = _last // exclam_ramp_up[i]

    daily_h_to_print.append(v + '!'*_exclams)
    continue 

##########################
# final output section

clear()
print()
print()
print()
print(f'-------- (Boilerplate) Tasks to do ({get_day(0)[5:]}) --------')
print()
# something something print a list full of everything
# all habits with their exclam marks
for line in daily_h_to_print:
    print(line)
    print()
    continue 
print('---------------------------------------------------')
print()
print()

