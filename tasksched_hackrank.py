#import cProfile

class SEGTreeNode(object):
    def __init__(self, leftchild, rightchild, index, valfunc):
        self.lc, self.rc = leftchild, rightchild
        if leftchild == None or rightchild == None:
            # leaf node
            self.interval = (index, index)
            self.maxnode = self
        else:
            self.interval = (leftchild.interval[0], rightchild.interval[1])
            #keyfunc = lambda x : valfunc(x.maxnode.interval[0])
            #self.maxnode = max(leftchild, rightchild, key=keyfunc).maxnode
            lv = valfunc(leftchild.maxnode.interval[0])
            rv = valfunc(rightchild.maxnode.interval[0])
            if lv > rv:
                self.maxnode = leftchild.maxnode
            else:
                self.maxnode = rightchild.maxnode


def segtree_build_topdown(left, right, valfunc):
    ''' Build a segment tree starting in the range from ''left'' to ''right'',
    inclusively. Build the tree in top-down fasion. '''
    if left == right:
        node = SEGTreeNode(None, None, left, valfunc)
        return node
    mid = (right + 1 - left) / 2 + left - 1
    lc = segtree_build_topdown(left, mid, valfunc)
    rc = segtree_build_topdown(mid + 1, right, valfunc)
    return SEGTreeNode(lc, rc, None, valfunc)

def segtree_update(root, idx, valfunc):
    ''' Update the value of a leaf node with index ''idx''. '''
    # First find the path leading to the leaf node with index ''idx''.
    node = root
    path = [root]
    while True:
        if node.lc is None:
            break
        midleft = node.lc.interval[1]
        if idx > midleft:
            path.append(node.rc)
            node = node.rc
        else:
            path.append(node.lc)
            node = node.lc
    # Now update each node affected
    prev = None
    for node in reversed(path):
        if node.lc is None:
            # leaf node: do nothing
            pass
        else:
            #keyfunc = lambda x : valfunc(x.maxnode.interval[0])
            #node.maxnode = max(node.lc, node.rc, key=keyfunc).maxnode
            lv = valfunc(node.lc.maxnode.interval[0])
            rv = valfunc(node.rc.maxnode.interval[1])
            if (lv > rv):
                node.maxnode = node.lc.maxnode
            else:
                node.maxnode = node.rc.maxnode

negative_infinity_func = lambda idx: float("-inf")

class BinaryIndexedTree(object):
    def __init__(self, size=0):
        self.elems = [(0, 0) for i in xrange(size)]
        self.size = size

    def calc(self, idx, val):
        ''' Calculate the responsibility for index ''idx'' with value ''val''.
        Assuming that indices less then ''idx'' already has the correct values. '''
        # Responsibility for ''idx'' is the the sum of frequencies from idx to
        # idx - 2^r + 1. So idx in binary is 1bbb100 then this is the sum from
        # 1bbb100 down to 1bbb001.
        resp = val
        target_idx = idx - (idx & -idx) # the frequecy of target is not included
        i = idx - 1
        while i > target_idx:
            resp += self.elems[i-1][1]
            i -= (i & -i)
        self.elems[idx - 1] = (val, resp)

    def update(self, idx, val):
        ''' Build the tree with a list of values for each node. ''idx'' is 1 based. '''
        if idx > self.size:
            # fill the intervening elements with zeros
            for i in xrange(self.size, idx):
                self.elems.append((0, None))
            # Calculate responsibilities for new elements
            for i in xrange(self.size + 1, idx + 1):
                self.calc(i, 0)
            self.size = idx
        oldfreq, resp = self.elems[idx-1]
        change = val - oldfreq
        self.elems[idx - 1] = (val, resp)
        self._update(idx, change)

    def _update(self, idx, change):
        ''' Update tree at idx with change. '''
        if change == 0:
            return
        while idx <= self.size:
            freq, resp = self.elems[idx-1]
            self.elems[idx - 1] = (freq, resp + change)
            idx += (idx & -idx)

    def sum(self, idx):
        ''' The sum at idx. '''
        sum = 0
        while idx > 0:
            sum += self.elems[idx-1][1]
            idx -= (idx & -idx)
        return sum


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

    def prep(self):
        ''' Prepare for scheduling for all tasks one by one. '''
        # rank by deadline
        #self._tasks_by_rank = sorted(self._tasks_by_id, key=lambda t: t[1])
        self._tasks_by_id.sort(key=lambda t: t[1])
        self._tasks_by_rank = self._tasks_by_id
        del(self._tasks_by_id)
        # build an index from task id => task rank, rank starts from 1 also
        self._id2rank_map = self.ntasks * [None]
        for i, t in enumerate(self._tasks_by_rank):
            self._id2rank_map[t[0] - 1] = i
        # initialize trees
        self._bitree = BinaryIndexedTree(self.ntasks)
        self._segtree = segtree_build_topdown(1, ntasks, negative_infinity_func)

    def sched(self):
        for idx in xrange(1, self.ntasks + 1):
            rank = self._id2rank_map[idx - 1] + 1
            di, mi = self._tasks_by_rank[rank - 1][1:]
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
                    return valcache[node_rank]
                node_idx, node_di, node_mi = self._tasks_by_rank[node_rank - 1]
                if node_idx > idx:
                    res = float("-inf")
                else:
                    res = self._bitree.sum(node_rank) - node_di
                valcache[node_rank] = res
                return res
            segtree_update(self._segtree, rank, valfunc)
            maxrank = self._segtree.maxnode.interval[0]
            maxover = valfunc(maxrank)
            if maxover < 0:
                maxover = 0
            print maxover


##
# Test
#
if __name__ == "__main__":
    # Get number of tasks
    ntasks = int(raw_input())
    tschedr = TaskScheduler()
    for idx in xrange(1, ntasks + 1):
        (di, mi) = raw_input().split()
        newtask = (idx, int(di), int(mi))
        tschedr.add(newtask)
    tschedr.prep()
    tschedr.sched()
    #cProfile.run('tschedr.sched()', 'xprof.txt')
