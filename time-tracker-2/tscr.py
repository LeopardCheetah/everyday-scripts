import os
import time
# from io import StringIO
# import sys

#############
## round 2 ##
#############

def clear(): # clears screen
    print('\033[2J\033[H')
    return 


# all this io and rerouting stdin works but its too complicated and unnecessary
# we're just gonna make our thing not be able to backspace through lines
# before = sys.stdin
# sys.stdin = StringIO()
# StringIO.write("some test text")
# StringIO.write("some more text")
# s = input()
# print(s, type(s))


# the simple and dirty way -- use input()!

#############################################################################
# user defined variables



# lp = line prefix
lp_a = '>>'

lp_b = '->'
lp_c = '->'
lp_d = '-@>'
lp_e = '+>'
lp_f = '><>'

lp_w = '~>'
lp_x = '=>'
lp_y = '-[>'

# p = prompt
# these are the list of things I'M tracking
# customize to ur liking
p_a = 'What did you do today?\nDid you do a "big thing"?'
p_a2 = 'Anything else come to mind about what happened today?'

p_b = 'Semi-daily habit tracker tracking portion (e.g. 11234567, 346):'
p_c = "Approx amount of time spent gaming/Amount of time 'wasted'? (e.g. 90m/90m)"
p_c2 = 'How much time was spent on prog/ee?'
p_d = 'What time did you wake up today?'
p_e = 'How much time/distance did you spend biking today? (e.g. 30m/4mi)'
p_f = 'Mood (1-10)?'
p_ft = 'Mood comments:'

p_w = 'How are you feeling currently? Worries/Anxieties/Happies/Thoughts~:'
p_x = 'Anything going on tomorrow? Anything to kick to tomorrow?'
p_y = 'Anything else? (Misc.)'

# signifies to move on to the next section
default_section_enders = ['n', 'next', 'next section']

# [' ']/['  '] spacer to split one liners + frqs
default_lp = [''] + [lp_a, lp_a] + [' '] + [lp_b, lp_c, lp_c, lp_d, lp_e, lp_f, lp_f] + ['  '] + [lp_w, lp_x, lp_y]
default_p  = [''] + [p_a, p_a2]  + [' '] + [p_b,  p_c,  p_c2, p_d,  p_e,  p_f,  p_ft] + ['  '] + [p_w,  p_x,  p_y]


# ok i lied there's more user variables but i dont wanna kwargs this so go find them yourself

############### everything below here is NOT user-changeable and is the script
#############################################################################

for i, v in enumerate(default_lp):
    default_lp[i] = v + ' '

# print(default_lp.index('  '), default_lp.index('   ')) -> 3, 11

def time_tracker_script(_lp=default_lp, _p=default_p, section_enders=default_section_enders):
    med_time = 5
    refl_time = 7

    # everything to write
    to_write = []
    _section_text = []


    _c = 1 # counter to track which "state" we're on + which prompt we should be using


    # first batch of open-ended questions
    while _c < default_lp.index('  '):
        if _c == 2:
            # add meditation/reflection section that's built in to do stuff
            clear()
            print('Would you like to meditate or just simply reflect (look out the window) today?')
            _answer = input('[m/r] >> ').strip().lower()

            while _answer not in ['m', 'r']:
                print()
                print('That was not a valid response!')
                time.sleep(1)

                print('Again, would you like to meditate or just simply reflect today?')
                _answer = input('[m/r] >> ').strip().lower()
                continue 

            # some config based on which one you chose
            secs = 60*med_time if _answer == 'm' else 60*refl_time
            secs = min(secs, 999) # ensure secs < 1000
            secs = max(0, secs) # ensure non-negativity

            word = 'meditating' if _answer == 'm' else 'reflecting'


            # ok do some terminal trickery kinda
            clear()
            print(f'Have fun {word}! :)')
            print(f'(Note: Try not to look at the screen during this time -- close your eyes or look outside instead!)')
            print()

            # average buffer flush
            print(f'Seconds remaining:', end='', flush=True)
            print("% 4d"%secs, end='', flush=True)
            time.sleep(1)

            # display time left
            for s in range(secs - 1, 0, -1):
                # print(s)

                # move 4 left + clear then print with padding
                print('\033[4D\033[0J', end='', flush=True)
                print("% 4d"%s, end='', flush=True)
                time.sleep(1)
                continue 


            print('\033[4D\033[0J', end='', flush=True)
            print("   None :)", flush=True)
            print()
            # block for input
            _ = input('>> Press any key to continue.....')
            # continue on normally!



        _nl_counter = 0
        _section_text = []
        clear()

        print(_p[_c])
        _section_text.append(_p[_c])

        _in = input(_lp[_c]).strip()
        while _in not in section_enders and _nl_counter < 2:          
            _nl_counter = _nl_counter + 1 if _in == '' else 0

            _section_text.append(_lp[_c] + _in)
            _in = input(_lp[_c]).strip()
            continue 

        to_write.append(_section_text)
        _c += 1 
        continue


    
    _c += 1 # skip spacer
    _nl_counter = 0
    _section_text = []
    



    clear()
    # one liner sections
    while _c < default_lp.index('   '):
        print(_p[_c])
        _in = input(_lp[_c]).strip()
        to_write.append([_p[_c], _lp[_c] + _in])
        _c += 1
        print()
        continue 



    _c += 1 # skip spacer separating one liners from more frqs


    # last few frq sections
    while _c < len(default_lp):
        _nl_counter = 0
        _section_text = []
        clear()
        print(_p[_c])
        _section_text.append(_p[_c])

        _in = input(_lp[_c]).strip()
        while _in not in section_enders and _nl_counter < 2:          
            _nl_counter = _nl_counter + 1 if _in == '' else 0

            _section_text.append(_lp[_c] + _in)
            _in = input(_lp[_c]).strip()
            continue 

        to_write.append(_section_text)
        _c += 1 
        continue 

    # done!
    return to_write
