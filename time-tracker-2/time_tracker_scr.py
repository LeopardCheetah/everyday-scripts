
################################

# Defaults that can be changed #


# makes it so that if its 2:43am 
# and i do a day recap, the date 
# of the day is still from the 
# previous day
hour_offset = 4             


################################


#############################################
# script -- don't change anything below pls #
#############################################


import time 
import os

import tscr as tt


# get the day recap
to_write = tt.time_tracker_script()


# format: YYYY-MM-DD
d = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60*60*hour_offset))

# format: YYYY-MM-DD HH:MM:SS (24h time)
t_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


path = f'day_recaps/{d[:7]}/{d}.txt' 



if os.path.isfile(path):
    # file exists, delete it
    os.remove(path)

# make new directory for tt
# is of the form yyyy-mm
if not os.path.isdir(path[:18]):
    os.mkdir(path[:18])


with open(path, "w") as f:
    f.write(f'{d}\n')
    f.write("File made at: "+t_formatted+'\n')
    for _ls in to_write:
        f.write('--------------------------------------' + '\n')
        for _l in _ls:
            f.write(_l + '\n')


print()
print()
print('done!')