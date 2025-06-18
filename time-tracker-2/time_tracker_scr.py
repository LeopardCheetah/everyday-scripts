import time 
import os

# for those pulling from code base use this import
# import tt
import devdev as tt

############################
# see the script file to actually change prompt defaults and such
############################

# makes it so that if its 1:43am and i do a day recap, the date of the day is still from the previous day
hour_offset = 2 

#####
# get the day recap
to_write = tt.time_tracker_script()
######



t = time.localtime(time.time() - 60*60*hour_offset)

d = str(t.tm_year) + '-'
if t.tm_mon < 10:
    d += '0'
d += str(t.tm_mon) + '-'
if t.tm_mday < 10:
    d += '0'
d += str(t.tm_mday)

t_formatted = time.strftime(d+" %H:%M:%S", time.localtime())


path = f'day_recaps/{d}.txt' # change this to wherever you want to store files i guess

if os.path.isfile(path):
    # file exists, delete it
    os.remove(path)

with open(path, "w") as f:
    f.write(f'{d}\n')
    f.write("File made at: "+t_formatted+'\n')
    for _ls in to_write:
        f.write('--------------------------------------' + '\n')
        for _l in _ls:
            f.write(_l + '\n')
