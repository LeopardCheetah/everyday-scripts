# refined, some comments removed (besides user inputs)


#############################################################################
# user defined variables cuz im fancy now
# lp = line prefix
lp_a = '>>'
lp_b = '->'
lp_c = '->'
lp_d = '><>'
lp_e = '=>'
lp_f = 'o>'

# p = prompt
p_a = 'What notable things were done today?'
p_b = 'Enter how your habits have been: (e.g. abgh, bcefgh)'
p_c = 'How much time do you think you spent gaming today? (e.g. 90, 1h30m)'
p_d = 'Mood?'
p_e = 'Anything going on tomorrow? Anything to kick to tomorrow?'
p_f = 'Anything else? (Misc.)'

# signifies to move on to the next section
default_section_enders = ['n', 'next', 'next section']


default_lp = ['', lp_a+' ', lp_b+' ', lp_c+' ', lp_d+' ', lp_e+' ', lp_f+' ']
default_p = ['', p_a, p_b, p_c, p_d, p_e, p_f]

############### everything below here is NOT user-changeable but the script
#############################################################################


import os

def clear():
    print('\033[2J\033[H')
    return 



def time_tracker_script(_lp=default_lp, _p=default_p, section_enders=default_section_enders):
    to_write = []
    _section_text = []

    # state 1 --> on notable things done
    # state 2/3/4 --> habit progress + estimated time on video games + mood indicator (1-10) 
    # state 5 --> for tmrw
    # state 6 --> other stuff (misc)
    _state = 0



    _state = 1
    clear()
    print(_p[_state])
    _section_text.append(_p[_state])

    _in = input(_lp[_state]).strip()
    while _in not in section_enders:
        _section_text.append(_lp[_state]+_in)
        _in = input(_lp[_state]).strip()


    to_write.append(_section_text)
    _section_text = []



    # part 2/3/4 -- one liners
    clear()
    for _s in [2, 3, 4]:
        _state = _s
        print(_p[_state])
        _in = input(_lp[_state]).strip()
        to_write.append([_p[_state], _lp[_state]+_in])
        print()



    clear()
    _state = 5
    print(_p[_state])
    _section_text.append(_p[_state])

    _in = input(_lp[_state]).strip()
    while _in not in section_enders:
        _section_text.append(_lp[_state]+_in)
        _in = input(_lp[_state]).strip()


    to_write.append(_section_text)
    _section_text = []




    clear()
    _state = 6
    print(_p[_state])
    _section_text.append(_p[_state])

    _in = input(_lp[_state]).strip()
    while _in not in section_enders:
        _section_text.append(_lp[_state]+_in)
        _in = input(_lp[_state]).strip()


    to_write.append(_section_text)

    #####
    
    return to_write
