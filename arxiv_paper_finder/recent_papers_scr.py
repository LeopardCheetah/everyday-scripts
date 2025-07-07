# get some recent papers

import requests
import time 


categories_to_search = ['math.HO', 'math.GM', 'cs.DS', 'cs.GT', 'cs.CC', 'math.CA', 'cs.CC', 'cs.CR', 'math.NA', 'math.NT', '']


# parses the massive atom file thingy majig
# returns list of lists of [id, title, summary, author(s)] for each paper
# author(s) will also be a list
def arxiv_atom_parser(atom_str):
    _new_str = atom_str.replace('\t', '')
    _lines = atom_str.split('\n')

    papers_info = []
    _temp_paper_info = []
    _entry = False
    _title = False
    _title_s = ''
    _summary = False
    _summary_s = ''
    _author = False
    _author_ls = []

    for _idx in range(len(_lines)):
        _lines[_idx] = _lines[_idx].strip() # parsing
      

        if '<entry>' in _lines[_idx]:
            _entry = True
            continue 

        if '<id>' in _lines[_idx] and _entry: # 2nd conditional to filter out the first entry in the api call
            # log doi
            _doi = _lines[_idx][25:-5]
            _temp_paper_info.append(_doi)
            continue 

        if '<id>' in _lines[_idx]:
            continue # idk why ur here buddy
        
        if '<title>' in _lines[_idx] and _entry: # might be one line, might be two
            if '</title>' in _lines[_idx]:
                _title_s = _lines[_idx][7:-8]
                _temp_paper_info.append(_title_s)
                _title_s = ''
                continue 

            _title = True # multi-line title
            _title_s = _lines[_idx][7:]
            continue 

        if _title:
            if '</title>' in _lines[_idx]:
                # end it here
                _title = False 
                _title_s += ' ' + _lines[_idx][:-8]
                _temp_paper_info.append(_title_s)
                _title_s = ''
                continue 

            # just continue on i guess
            _title_s += ' ' + _lines[_idx]
            continue 


        # do the same thing with summary
        if '<summary>' in _lines[_idx] and _entry: # at least one line
            _summary = True # multi-line title
            _summary_s = _lines[_idx][9:]
            continue 

        if _summary and '</summary>' not in _lines[_idx]:
            # continue parsing
            _summary_s += ' ' + _lines[_idx]
            continue 

        if '</summary>' in _lines[_idx]:
            # no text here since it seems this its only line 
            # just add everything in and wrap up
            _summary = False
            _temp_paper_info.append(_summary_s)
            _summary_s = ''
            continue 

        
        # author
        if '<author>' in _lines[_idx] and _entry:
            # only thing in the line, no need to do anything else
            _author = True
            continue 
        
        if '</author>' in _lines[_idx]:
            _author = False
            continue
        
        if _author:
            # assuming the name tag is in there
            _author_ls.append(_lines[_idx][6:-7])
            continue 

        if '</entry>' in _lines[_idx]:
            # wrap up
            _entry = False
            _temp_paper_info.append(_author_ls)
            _author_ls = []

            _temp_paper_info[2] = _temp_paper_info[2].strip() # some weird spaces

            papers_info.append(_temp_paper_info)
            _temp_paper_info = []
            continue 

        continue 
    
    return papers_info



_search_start_day = time.strftime('%Y%m%d', time.localtime(time.time()  - 24*60*60*14 + 2*60*60)) # in case i do this between 12-2am
_search_end_day = time.strftime('%Y%m%d', time.localtime(time.time() + 2*60*60))



# note: idk why params fuck up here but you cant use them
# something to do with the + signs
# TODO -- fix this later
params = {'search_query': 'cat:math.NT+AND+submittedDate:[202506010001+TO+202507070001]'}
# YYYYMMDD
l = 'https://export.arxiv.org/api/query'
r = requests.get(l + '?' + 'search_query=cat:math.NT+AND+submittedDate:[202506010001+TO+202507070001]' + '&' + 'max_results=3')


print()
print(r.url, r.status_code)
print()
big_ls = arxiv_atom_parser(r.text)

for ls in big_ls:
    print(ls)
    print()

time.sleep(3) # to prevent requests going too fast
s = 'https://export.arxiv.org/api/query?search_query=cat:math.NT+AND+submittedDate:%5B202506010001+TO+202507070001%5D 200'