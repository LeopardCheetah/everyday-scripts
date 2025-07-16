# write to habit_progress.txt
# if this code fails maybe make a blank file called "habit_progress.txt" and proceed from there

import os
import time

# t is a timestamp (seconds from epoch)
# return yyyy-mm-dd, if the day is a sunday or not
def get_date_is_sunday(t):
    return time.strftime("%Y-%m-%d", time.localtime(t)), time.strftime("%u", time.localtime(t)) == '7'

def get_habit_str(path):

    h = ''
    try:
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
            pass # end file opening thing
    
        return h
    except:
        return ':(' # path error or whatever

############################################
############################################


# habit_progress.txt structure:
# line 1: seconds from the epoch detailing when this file was last written
# line 2: --------------
# line 3+: habits;
# habits will look like this:

'''
[Habit 1]: xx-n xx-x--n --nxx-n ....... 
xxx-xxn .......

[Habit 2]: ...
'''
# new line gaps only happen between habits
# new lines only happen every year, and things are written back to front; e.g.:
'''
[Habit 3]: x--n
n-x......
'''
# we can deduce that the last x (the x in 'n-x') was written on 12/29, the - on 12/30, the n on 12/31
# then the n in the upper line on 1/1, the two dashes on 1/2 and 1/3, and the x on 1/4


# ok enough specification garbage
last_written_time = -1
habit_logs = [[]]

with open('habit_progress.txt', 'r') as _f:

    last_written_time = int(_f.readline()[:-1])
    _buffer = _f.readline() # dashes

    _flag = False 
    while not _flag:
        _line = _f.readline()
        
        if _line == '': # file end
            _flag = True
            continue 

        if _line == '\n':
            habit_logs.append([])
            continue
        
        habit_logs[-1].append(_line[:-1])


# assume all data written to the last_written_time is correct (besides that day)
# if file was last written to at 04/05/2006 then assume all habits are correct up to 04/05/2006 (but not 04/05)

base_time = time.time()
days_to_cover = int((base_time - last_written_time) // (24*60*60))

# get length of the first x/-/n line of the first habit
_c = habit_logs[0][0].split(':')[1][1:].index(' ')

for _idx in range(days_to_cover, 0, -1): # n, n-1, n-2, ..., 1
    _date, _is_sunday = get_date_is_sunday(base_time - 24*60*60*_idx)
    _path = f'../time-tracker-2/day_recaps/{_date}.txt'
    _days_habits = get_habit_str(_path)

    if _date[-5:] == '01-01':
        # yikes a year switch; we'll do this manually

        _h_name_len = habit_logs[_hidx][0].index(':') 
        
        # get rid of the habit barcode thing in one line
        # and add it to this new line

        _hname = habit_logs[_hidx][0][:_h_name_len]
        habit_logs[_hidx][0] = habit_logs[_hidx][0][_h_name_len + 2:]

        habit_logs[_hidx].insert(0, '')

        _result = ''
        if _days_habits == ':(':
            _result = 'n'
        elif chr(ord('a') + _hidx) in _days_habits:
            _result = 'x'
        elif chr(ord('a') + _hidx) not in _days_habits:
            _result = '-'
        else:
            _result = '?' # not sure how you get here but ok
        
        habit_logs[_hidx][0] = _hname + ':' + ' ' + _result
        continue # i think this works!!
    
    
    for _hidx in range(len(habit_logs)):
        # _habit is actually a list so only use the string _habit[0]
        if type(habit_logs[_hidx]) != type([]):
            continue # some error

        if len(habit_logs[_hidx]) != 1:
            continue # some other error?

        _hs = habit_logs[_hidx][0]
        _h_name_len = _hs.index(':') 

        _result = ''
        if _days_habits == ':(':
            _result = 'n'
        elif chr(ord('a') + _hidx) in _days_habits:
            _result = 'x'
        elif chr(ord('a') + _hidx) not in _days_habits:
            _result = '-'
        else:
            _result = '?' # not sure how you get here but ok


        # part the red sea rq
        _hs = _hs[:_h_name_len + 2] + _result + _hs[_h_name_len + 2:]

        if _is_sunday:
            _hs = _hs[:_h_name_len + 2] + ' ' + _hs[_h_name_len + 2:]
            
        habit_logs[_hidx][0] = _hs
        continue 
    
    
# now write everything
with open('habit_progress.txt', 'w') as f:
    # write time, lines
    f.write(str(int(base_time)) + '\n')
    f.write('--------------------------------\n')

    # write habits
    for h in habit_logs:
        for s in h:
            f.write(s + '\n')
        
        f.write('\n')

# yippee we're done