
"""
> weekly review ported over to terminal!
>>> display some number of reading links to do 
>>> be able to document what you worked on this week and stuff like that 
>>> prompt some questions to consider about that week 
>>> (far down the line) automatically pull up stats about the past week/days

<Check my tt stats // time stats from the time tracker app.>
"""


def screen_clear(): # clears screen
    print('\033[2J\033[H')
    return 



# weekly review, packaged in the terminal.
# takes in some stuff
# returns some important stuff 

# start firefox --private-window google.com google.com
def weekly_review(questions, urls, private_window=False):

    # private window opening is broken
    # "start firefox -private-window" opens a private window
    # but "start firefox -private-window -url [URL]" or "start firefox -private-window [URL]"
    # end up opening said URL in an already opened window (not private) of firefox
    # => cannot really open a link in private window yet.
    # 
    # specifying the exact path to the private_window program also doesnt work :////
    if private_window:
        print('Cannot open in private window yet.')
        print('Functionality not configured')
        return 
    
    import time
    import subprocess
    import random


    qs = random.sample(questions, k=random.randint(2, 3))
    rs = random.sample(readings, k=2)

    # format: MM/DDYYYY-MM-DD
    date = time.strftime("%m/%d%Y-%m-%d", time.localtime(time.time()))


    screen_clear()

    print(f"\n\n\t\t\t\t\t------ Weekly Review ({date[:5]}) ------\n")

    print('\tWR Questions:\n')
    print(f'\t-> {qs[0]}')
    print(f'\t-> {qs[1]}')

    if len(qs) == 3:
        print(f'\t-> {qs[2]}')

    print('\n\n\tWR Articles:\n')
    print(f"\t~> '{rs[0][1]}'")
    print(f"\t~> '{rs[1][1]}'\n\n")


    _blocker = input('\t(Press [Enter] when ready for articles....)')

    for r in rs:
        subprocess.run(f'start firefox {'-private-window' if private_window else ''} {r[0]}', shell=True) 

    
    # clear 2 prev line with the press enter when ready
    print('\033[1A\033[K\033[1A\033[K')

    _blocker = input('\t(Press [Enter] when ready to reflect....)')


    # Reflection part.


    screen_clear()
    print('\nList any notes about this weekly review down below')
    print('(Are there any [TODO]s you want to kick to later? Any features to try to implement in life?)\n')



    wr_reflections = []
    _line = 'a'
    c = 0

    while c < 3 and _line not in ['n', 'next']:
        _line = input('- ')

        # go to the right most '\t' and add in "- "
        tabs = 0
        for char in _line:
            if char == ' ':
                continue 

            if char == '\t':
                tabs += 1
                continue 

            break

        wr_reflections.append(_line[:tabs] + '- ' + _line[tabs:])

        c = (c + 1) * (_line == '')
        continue 

    # filter out the statements with "todo" in them and put them in a separate list
    todos = []
    for line in wr_reflections:
        if "todo" in line.lower():
            # write that down write that down!
            # add in a date so its easier to keep track of
            todos.append(line + f' || {date[5:]}')
 

    return wr_reflections, todos, date[5:]




if __name__ == '__main__':


    # parse some weekly review questions
    questions = []
    with open('wr_questions.txt', 'r') as f:
        questions = f.readlines()
    
        # data clean up
        _remove = []
        for i, q in enumerate(questions):
            if len(q) < 3 or q[0] == '#':
                # this is not a question or it is a comment
                _remove.append(i)
                continue

            if q[-1] == '\n':
                questions[i] = questions[i][:-1]
            continue 

        for ind in _remove[::-1]:
            questions.pop(ind)
        
    # urls of various readings i find v cool to revisit during weekly review
    readings = [
        ('https://taylor.town/make-important-things-inevitable', 'Inevitable (Taylor)'),
        ('https://taylor.town/between-time', 'Between Time (Taylor)'),
        ('https://sive.rs/kimo', 'There is No Speed Limit (Sivers)'),
        ('https://academics.hamilton.edu/documents/themundanityofexcellence.pdf', 'Mundanity of Excellence (Chambliss)'),  
        ('https://mindingourway.com/rest-in-motion/', 'Rest in Motion (Soares)')
    ]

    wr, todo, date = weekly_review(questions, readings)


    # append wr to top
    # append todo to the list.

    _contents = []
    with open('wr_log.txt', 'r') as f:
        _contents = f.readlines()
    
    with open('wr_log.txt', 'w') as f:
        # write a header 
        f.write('-'*35 + '\n')
        f.write(date + ' Weekly Review Contents:\n')
        f.write('-'*35 + '\n')

        for line in wr:
            f.write(line + '\n')

        f.write('\n\n') # should be a spacer
        f.write(''.join(_contents)) # everything from before
        

    with open('wr_todos.txt', 'r') as f:
        _contents = f.readlines()
    
    with open('wr_todos.txt', 'w') as f:
        f.write('Weekly Review [TODO] list:\n')
        f.write('-'*40 + '\n')

        for line in todo:
            f.write(line + '\n')


        if len(_contents) > 1:
            f.write(''.join(_contents[2:]))

    

    screen_clear()
    print('\n\nWeekly Review Complete :)')
    print('Thanks for investing some time into this.\n')


    
    

    