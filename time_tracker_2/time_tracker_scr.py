from datetime import date
import os

# for those pulling from code base use this import
# import tt
import devdev as tt

############################
# see the script file to actually change prompt defaults and such
############################



#####
# get the day recap
to_write = tt.time_tracker_script()
######


day = date.today().isoformat()

path = f'day_recaps/{day}.txt' # change this to wherever you want to store files i guess

if os.path.isfile(path):
    # file exists, delete it
    os.remove(path)

with open(path, "w") as f:
    f.write(f'{day}\n')
    for _ls in to_write:
        f.write('--------------------------------------' + '\n')
        for _l in _ls:
            f.write(_l + '\n')
