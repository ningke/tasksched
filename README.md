tasksched
=========

HackerRank's Task Scheduling Problem

# This is a problem from hackerrank:

You have a long list of tasks that you need to do today. Task i is specified by the deadline by which you have to complete it (Di) and the number of minutes it will take you to complete the task (Mi). You need not complete a task at a stretch. You can complete a part of it, switch to another task and then switch back.

You've realized that it might not actually be possible complete all the tasks by their deadline, so you have decided to complete them so that the maximum amount by which a task's completion time overshoots its deadline is minimized.

Input:
The first line contains the number of tasks T. Each of the next T lines contains two integers Di and Mi.

Output:
Output T lines. The ith line should contain the minimum maximum overshoot you can obtain by optimally scheduling the first i tasks on your list. See the sample input for clarification.

Constraints:
1 <= T <= 100000
1 <= Di <= 100000
1 <= Mi <= 1000

Sample Input:
5
2 2
1 1
4 3
10 1
2 1

Sample Output:
0
1
2
2
3


# Solution

The key insight is that the task with a later deadline MUST be completed later
than a task with an earlier deadline - regardless how you break up the tasks.
Otherwise, the first task (the one with an earlier deadline) will overshoot its
own deadline by more than the second task overshoots its deadline.
So we can essentially just sort the tasks by their deadline and complete them in
that order. The problem description about breaking up tasks are just there to confuse
you. (why?)

However, since the problem requires you to do this incrementally, i.e., solve the
scheduling for tasks from 1 to n. The naive method above takes O(nlog(n)) for each
iteration, so it will take O((n^2)log(n)) in total, which is unacceptable: a solution
in Python only has 16 seconds to solve the problem. So a more efficient solution is
needed. This is turns out to be quite hard.

