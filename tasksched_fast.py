import bitree
import segtree

##
# See tasksched.py for problem description and algorithm.
#
class TaskScheduler(object):
    def __init__(self):
        self._tasks_by_id = []
        self._tasks_by_rank = []
        self._id2rank_map = []
        self.ntasks = 0

    def add(self, tsk):
        ''' Each task ''tsk'' is a tuple of (task_index, deadline, duration). '''
        self._tasks_by_id.append(tsk)
        self.ntasks += 1

    def _task_by_id(self, id):
        return self._tasks_by_id(id - 1)

    def _task_by_rank(self, rank):
        return self._tasks_by_rank[rank - 1]

    def _id2rank(self, id):
        ''' both task id and task rank are 1 based. '''
        return (self._id2rank_map[id - 1] + 1)

    def prep(self):
        ''' Prepare for scheduling for all tasks one by one. '''
        # rank by deadline
        self._tasks_by_rank = sorted(self._tasks_by_id, key=lambda t: t[1])
        # build an index from task id => task rank, rank starts from 1 also
        self._id2rank_map = self.ntasks * [None]
        for i, t in enumerate(self._tasks_by_rank):
            self._id2rank_map[t[0] - 1] = i
        #print self._tasks_by_id
        #print self._tasks_by_rank
        #print self._id2rank_map
        # initialize trees
        self._bitree = bitree.BinaryIndexedTree(self.ntasks)
        self._segtree = segtree.segtree_build_topdown(1, ntasks, segtree.negative_infinity_func)

    def sched(self):
        cache_stats = [0, 0] # (hits, misses)
        for idx in xrange(1, self.ntasks + 1):
            rank = self._id2rank(idx)
            di, mi = self._task_by_rank(rank)[1:]
            #print ">>>>>>"
            #print "task idx %d rank %d mi %d di %d" % (idx, rank, mi, di)
            # Now insert this task by its rank into the bitree and segtree
            self._bitree.update(rank, mi)
            # All we need to do now is to insert the new task into the segment tree now.
            # Since all tasks after the new task will be delayed by the mi of task.
            # We'll update the tree dynamically, meaning the value stored in the
            # segment tree is supplied a function (v.s. a statically value). This way
            # the *relative* rank of segment tree nodes are preserved, even though it
            # doesn't have the value directly.
            # Because we may need the same "sum" for a node repeatedly in the update
            # process, we will cache the results here: this is important because
            # if we don't we will end up with O(log(n)^2) for each update:
            # O(log(n)) for depth of segment tree and O(log(n)) for each bitree summing
            # function.
            valcache = {}
            def valfunc(node_rank):
                if node_rank in valcache:
                    cache_stats[0] += 1
                    return valcache[node_rank]
                cache_stats[1] += 1
                node_idx, node_di, node_mi = self._task_by_rank(node_rank)
                if node_idx > idx:
                    # Don't count tasks that haven't been inserted.
                    res = float("-inf")
                else:
                    res = self._bitree.sum(node_rank) - node_di
                valcache[node_rank] = res
                return res
            segtree.segtree_update(self._segtree, rank, valfunc)
            maxrank = self._segtree.maxnode.interval[0]
            #self._bitree.display()
            #segtree.segtree_print(self._segtree)
            #print "max idx %d rank %d over %d" % (self._task_by_rank(maxrank)[0], maxrank, valfunc(maxrank))
            maxover = valfunc(maxrank)
            if maxover < 0:
                maxover = 0
            print maxover
        print "cache hits: %d cache misses %d" % (cache_stats[0], cache_stats[1])


##
# Test
#
if __name__ == "__main__":
    import sys
    # Get number of tasks
    ntasks = int(raw_input())
    #print ">>> %d tasks" % ntasks
    tschedr = TaskScheduler()
    for idx in xrange(1, ntasks + 1):
        (di, mi) = raw_input().split()
        newtask = (idx, int(di), int(mi))
        #print ">>> %s" % (newtask)
        tschedr.add(newtask)
    tschedr.prep()
    tschedr.sched()
