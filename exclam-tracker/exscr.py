# generate list of tasks of what to do
# can be run infinitely, no need to worry about data corruption or anything

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
    _d = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24*60*60*n))
    return _d

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
num_of_prev_days = 7

num_habits = 5 # manual count



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
    path = f'../time-tracker-2/day_recaps/{get_day(day)[:7]}/{get_day(day)}.txt'

    habs = ''
    try:
        habs = get_habit_s(path)
    except:
        # path error since file doesn't exist
        habs = ':(' 
    
    # as of 08/10/2025 h can now contain:
    # 1 = brush (max: 2)
    # 2 = instrumenting
    # 3 = reading/exploring
    # 4 = coding (cp/projects)
    # 5 = mathing (analysis/comp. math)
    # 6 = showering
    # 7 = outsiding (biking/walking)

    # wlog assume the 1s are together
    # for c in [i + 1 for i in range(num_habits)]:

    for c in [1, 3, 4, 6, 7]: # manual since the htracker got cooked lol
        if contains(habs, c):
            # (habit, day num)
            arr[[1, 3, 4, 6, 7].index(c)][day - 1] = 1
            continue 
    
    # now that proging/math are together...
    if contains(habs, 5):
        arr[4][day - 1] = 1

    # last whatever's tt results have been tracked!


################
################
# make these tasks more concrete
tasks = [
    "[Brush | Brush], Floss, Anki", 
    "Reading - 1 Chapter/2 RL Articles", 
    "proging (CP/Projects)/Mathing (Analysis/Comp. Math) - >45 min", 
    "Showering", 
    "Outsiding"
]


# 2 -> this should be done once every 2 days
task_freq = [1, 1, 1, 2, 1]

# default ramp up will just be for every 1 days something isn't done, add an exclam
# x -> Code -> Code -> Code!
exclam_ramp_up = [1, 2, 2, 1, 1]



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





#####################################
#######################################
# new: figure out how much time ive spent playing poker/prog and how much time ive spent mathing/chess and display available amount of time
# note: inputs should be parsable -> either in [xx]h[yy]m or [yy]m or [yy] (integer, in minutes)
# otherwise assume defaults
# prog/math: 0/0, poker/chess: 90/90

rollover_max = 300 # max: rollover 5h from previous months
poker_time = 0
chess_time = 0
last_timestamp = 0

# parse input 
with open('exscr_memory.txt', 'r') as f:
    for _line in f:
        _description, _v = '', ''
        try:
            _description, _v = _line.strip().split() # should be 2 parts
            _v = int(_v)
            _description = _description.lower() # should not be an issue
        except:
            continue # ????            


        if "last-timestamp:" in _description:
            last_timestamp = _v
            continue 
        
        if "poker" in _description:
            poker_time = _v
            continue 

        if "chess" in _description:
            chess_time = _v
            continue 

        continue # shrug

# manually convert to number of days missing
# assumption: ex t is not gonna be run past 12am so like yeah
# NOTE: this is meant to be run in PST (-7) so like there's an hour offset
pst_offset = -7
_days_to_parse = (int(time.time() + pst_offset*60*60) // (24*60*60)) - (int(last_timestamp + pst_offset*60*60) // (24*60*60))


for d in range(_days_to_parse, 0, -1):
    # use time.localtime to get date
    # go from back to front

    _tt_file = get_day(d) + '.txt'
    # _tt_file = time.strftime('%Y-%m-%d.txt', time.localtime(time.time() - (d)*24*60*60))

    # new addition!
    _tt_file = _tt_file[:7] + r'/' + _tt_file

    # fetch file
    _ls = []
    with open('../time-tracker-2/day_recaps/' + _tt_file, 'r') as f:
        _ls = f.readlines()


    # hardcoded
    _prompts = ['How much time was spent on prog/ee?\n', 'How much time was spent on poker?\n', 'How much time was spent on math?\n', 'How much time was spent on chess?\n']
    for _i, _p in enumerate(_prompts):
        _base = 90 if _i % 2 else 0
        _s = ''

        try:
            _s = _ls[_ls.index(_p) + 1]
            _s = _s[4:-1]

            # forgive me me in the future for sinning
            # and putting more if statements in the else or something
            if 'm' not in _s and 'h' not in _s:
                _base = int(_s)
            elif 'm' not in _s:
                # parse BEFORE the h
                # so things like 2h5 -> 2h
                # maybe
                _base = 60*int(_s[:_s.index('h')])
            elif 'h' not in _s:
                _base = int(_s[:_s.index('m')])
            else:
                # parse both h and m
                # WLOG its 2h5m not 5m2h
                _base = 60*int(_s[:_s.index('h')]) + int(_s[_s.index('h') + 1:_s.index('m')])

        except:
            pass

        # do some parsing in extraordinary cases
        # yyyy-mm-dd.txt
        if _tt_file[8:10] == '01':
            # first of the day, rate limit the time
            poker_time = max(rollover_max, poker_time)
            chess_time = max(rollover_max, chess_time)


        # basically case breaking
        # poker-math, chess-prog
        # i = 0 -> prog,
        # i = 1 -> poker
        # i = 2 -> math
        # i = 3 -> chess
        if _i == 0: 
            chess_time += ((_base + 1) // 2) # round up the time
            continue 
        if _i == 1:
            poker_time -= _base
            continue
        if _i == 2:
            poker_time += ((_base + 1) // 2)
            continue 
        if _i == 3:
            chess_time -= _base
            continue

        continue

    # done!

# done!
# now just write to file -- printing is done later!

#
# last-timestamp: 1759647446
# poker-prog 0
# chess-math -120
#
with open('exscr_memory.txt', 'w') as f:
    f.write(f'last-timestamp: {int(time.time())}\n')
    f.write(f'poker-prog {poker_time}\n')
    f.write(f'chess-math {chess_time}')



    


##########################
# final output section

clear()
print()
print()
print(f'-------- (Boilerplate) Tasks to do ({get_day(0)[5:]}) --------')
print()
# something something print a list full of everything
# all habits with their exclam marks
for line in daily_h_to_print:
    print(line)
    continue 
print()
print('             -------------------------             ') # 13 chars on each side, total len = 51

# print poker/chess available timings
print()
print(f'Available poker time: \t {poker_time}m')
print(f'Available chess time: \t {chess_time}m')

print()
print('---------------------------------------------------')
print()

