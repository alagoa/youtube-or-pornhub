from __future__ import print_function
from collections import defaultdict
import glob


res = defaultdict(list)
path = "down*"
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
f = open('youtubedown', 'w')
for x0,x1,x2,x3,x4,x5,x6,x7,x8,x9 in zip(*res.values()):
    print(x0 + " " + x1 + " " + x2 + " " + x3 + " " + x4 + " " + x5 + " " + x6 + " " + x7 + " " + x8 + " " + x9, file=f)



