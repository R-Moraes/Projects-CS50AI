import numpy as np
import string

x = ['work','travel', 'love', 'is','join','!','"','#']
for i in x:
    a = set(i)
    p = set(string.punctuation)
    r = a.difference(p)
    print(r)
    print(str(r))