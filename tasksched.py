##
# From hackerrank:
#
# You have a long list of tasks that you need to do today. Task i is specified by the deadline by which you have to complete it (Di) and the number of minutes it will take you to complete the task (Mi). You need not complete a task at a stretch. You can complete a part of it, switch to another task and then switch back.

# You've realized that it might not actually be possible complete all the tasks by their deadline, so you have decided to complete them so that the maximum amount by which a task's completion time overshoots its deadline is minimized.
# 
# Input:
# The first line contains the number of tasks T. Each of the next T lines contains two integers Di and Mi.
# 
# Output:
# Output T lines. The ith line should contain the minimum maximum overshoot you can obtain by optimally scheduling the first i tasks on your list. See the sample input for clarification.
# 
# Constraints:
# 1 <= T <= 100000
# 1 <= Di <= 100000
# 1 <= Mi <= 1000
# 
# Sample Input:
# 5
# 2 2
# 1 1
# 4 3
# 10 1
# 2 1
# 
# Sample Output:
# 0
# 1
# 2
# 2
# 3
# 

##
# The key insight is that the task with a later deadline SHOULD be completed later
# than a task with an earlier deadline - regardless how you break up the tasks.
# Otherwise, the first task (the one with an earlier deadline) will overshoot its
# own deadline by more than the second task overshoots its deadline.
# So we can essentially just sort the tasks by their deadline and complete them in
# that order.
#

def task_sched(tasks):
    ''' Give a list of tasks ''tasks'', produce a schedule along with any overtime.
    Each task in ''tasks'' is a tuple of (tid, di, mi), where tid is the task id, di
    is the deadline, and mi is the minutes it takes to complete it. ''issorted'' tells
    if ''tasks'' are already sorted. '''
    sched = []
    tasks.sort(key=lambda t: t[1])
    #print ">>>", tasks
    maxover = float("-inf")
    starttime = 0
    curtime = 0
    for t in tasks:
        #print ">>> time %d: task %s" % (curtime, t)
        st = curtime
        et = curtime + t[2]
        sched.append((t[0], st, et)) 
        curtime += t[2]
        if et - t[1] > maxover:
            maxover = et - t[1]
            #print ">>> maxover is now %d" % (et - t[1])
    #print ">>>", sched
    return (maxover, sched)

##
# Test
#

if __name__ == "__main__":
    import sys
    # Get number of tasks
    ntasks = int(raw_input())
    #print ">>> %d tasks" % ntasks
    tasks = []
    res = []
    for idx in range(1, ntasks + 1):
        (di, mi) = raw_input().split()
        #print ">>> %s" % ([idx, int(di), int(mi)])
        tasks.append((idx, int(di), int(mi),))
        maxover, sched = task_sched(tasks)
        res.append((maxover, sched,))
    for r in res:
        print r[0]

