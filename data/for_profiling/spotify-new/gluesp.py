from __future__ import print_function
from collections import defaultdict
import glob


res = defaultdict(list)
path = "spot*"
for filename in glob.glob(path):
    with open(filename, 'r') as f:
        i = 0
        j = 0
        for line in f:
            j += 1
            if not line.strip():
                i += 1
            res[filename].append(line.rstrip())
        print (filename + " " + str(i) + " " + str(j))
#print res
f = open('spotifydown', 'w')
for x0,x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12,x13,x14,x15,x16,x17,x18,x19 in zip(*res.values()):
    print(x0 + " " + x1 + " " + x2 + " " + x3 + " " + x4 + " " + x5 + " " + x6 + " " + x7 + " " + x8 + " " + x9 + " " + x10  + " " + x11 + " " + x12 + " " + x13 + " " + x14 + " " + x15 + " " + x16 + " " + x17 + " " + x18 + " " + x19, file=f)
