from datetime import date
import time

t = time.localtime(time.time() - 60*60*2)

d = str(t.tm_year) + '-'
if t.tm_mon < 10:
    d += '0'
d += str(t.tm_mon) + '-'
if t.tm_mday < 10:
    d += '0'
d += str(t.tm_mday)

print(d)

