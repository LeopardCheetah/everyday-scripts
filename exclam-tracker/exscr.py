# generate list of tasks of what to do
# can be run infinitely, no need to worry about data corruption or anything

import os
import time

def clear():
    print('\033[2J\033[H')
    return 

def contains(s, x):
    # does s contain x?
    if len(x) < 1 or len(x) > 1:
        return 'Perhaps'
    
    for i in s:
        if i == x:
            return True

    return False 

# n = how many days ago do you want the date of 
def get_day(n):
    t = time.localtime(time.time() - 24*60*60*n)
    d = str(t.tm_year) + '-'
    if t.tm_mon < 10:
        d += '0'
    d += str(t.tm_mon) + '-'
    if t.tm_mday < 10:
        d += '0'
    d += str(t.tm_mday)

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

            if line.strip() != 'Enter how your habits have been: (e.g. abgh, bcefgh)':
                continue 
            
            fl = True
            continue 
    
    return h

##############################
# load from file + update with last night's information
# format:
# [task] -x--x-- 3
# means task was not done 1/3/4/6/7 days ago but was done 2/5 days ago, task had 3 exclam marks as of yesterday

mem = []
with open('exmem.txt', 'r') as f:
    for li in f:
        a, b, c = li.strip().split()
        mem.append([a, b, c])

for k in range(7, 0, -1): # 7/6/.../1 days ago time tracking scripts
    path = f'../time-tracker-2/day_recaps/{get_day(k)}.txt'

    h = ''
    try:
        h = get_habit_s(path)
    except:
        h = ':(' # path error or whatever
    

    # here h can only have a/b/c/d/e/f/g/h (maybe none!)

    # reminder:
    # a = brush
    # b = music related stuff
    # c = read
    # d = code smth
    # e = mathing
    # f = shwr
    # g = go outside for a walk
    # h = drive
    for c in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        if contains(h, c):
            # yippee!
            mem[ord(c) - ord('a')][1] = 'x' + mem[ord(c) - ord('a')][1][:-1]
            continue 

        # not yippee
        mem[ord(c) - ord('a')] [1] = '-' + mem[ord(c) - ord('a')][1][:-1]

    # last whatever's tt results have been tracked!


################
################

# now that memory has been written in + updated with (presumably) last night's stuff, generate list of tasks (with exclamation marks) to do.

# taska
ta = "[Brush, Brush]"
tb = "Music stuff"
tc = "Read"
td = "Code"
te = "Analysis work" # math
# f/g not really 'tracked'
th = "Drive"


# 2 => once two of the same exclam marks are seen, ramp it up
# e.g. 
# drive! -> drive! -> drive!! -> drive!! -> drive!!!
exclam_baseline = [0, 1, 2, 2, 1, 2]
exclam_ramp_up = [0, 2, 2, 1, 2, 2]

habits_to_upd = ['', ta, tb, tc, td, te, th]



# process last night's results + update the "count"
mem.insert(0, ('', '', '')) # padding to make indices easier

countdx = -1 # countindex for the two upper lists
for idx in range(len(mem)):
    if idx == 0 or idx == 6 or idx == 7:
        continue # untracked; filler + habits f/g

    countdx += 1

    if exclam_ramp_up[countdx] == 0:
        mem[idx][2] = str(exclam_baseline[countdx])
        continue 

    _last = 0
    if 'x' not in mem[idx][1]:
        _last = 8 
    else:
        _last = mem[idx][1].find('x')

    mem[idx][2] = str(exclam_baseline[countdx] + _last // exclam_ramp_up[countdx])
    continue 



##################
##################
# print things to do
mem.pop(0) # remove spacer

exclam_final_list = [-1] # spacer for down there
for _idx in range(len(mem)):
    if int(mem[_idx][2]) < 0:
        continue 
    exclam_final_list.append(int(mem[_idx][2]))

clear()
print(f'-------- (Boilerplate) Tasks to do ({get_day(0)[5:]}) --------')
print()
for _index in range(1, 7):
    print(habits_to_upd[_index] + '!'*exclam_final_list[_index])

print()
print('---------------------------------------------------')






# write new memory to file
os.remove('exmem.txt')
with open('exmem.txt', 'w') as f:
    # just write
    for _ls in mem:
        f.write(f'{_ls[0]} {_ls[1]} {_ls[2]}\n')