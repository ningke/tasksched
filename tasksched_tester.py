# 
# Constraints:
# 1 <= T <= 100000
# 1 <= Di <= 100000
# 1 <= Mi <= 1000
#

import random

def test_case(ntasks):
    max_mi = 1000
    max_di = 100000
    mi = [i for i in range(1, max_mi + 1)]
    di = [i for i in range(1, max_di + 1)]
    print ntasks
    for i in xrange(ntasks):
        mi = random.randint(1, max_mi)
        di = random.randint(1, max_di)
        print di, mi

ntasks = int(raw_input())
test_case(ntasks)
