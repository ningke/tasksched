class BinaryIndexedTree(object):
    def __init__(self, size=0):
        self.elems = [(0, 0) for i in xrange(size)]
        self.size = size

    def _set_elem(self, idx, freq, resp):
        ''' Sets the element at ''idx'' with its freqency ''freq'' and responsibility
        ''resp''. '''
        self.elems[idx - 1] = (freq, resp)

    def _get_elem(self, idx):
        return self.elems[idx - 1]

    def calc(self, idx, val):
        ''' Calculate the responsibility for index ''idx'' with value ''val''.
        Assuming that indices less then ''idx'' already has the correct values. '''
        # Responsibility for ''idx'' is the the sum of frequencies from idx to
        # idx - 2^r + 1. So idx in binary is 1bbb100 then this is the sum from
        # 1bbb100 down to 1bbb001.
        resp = val
        target_idx = idx - (idx & -idx) # the frequecy of target is not included
        i = idx - 1
        #print "target %d i %d" % (target_idx, i)
        while i > target_idx:
            resp += self._get_elem(i)[1]
            i -= (i & -i)
        self._set_elem(idx, val, resp)
        #print "elem at %d => %s" % (idx, self._get_elem(idx))

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
        oldfreq, resp = self._get_elem(idx)
        change = val - oldfreq
        self._set_elem(idx, val, resp)
        self._update(idx, change)

    def _update(self, idx, change):
        ''' Update tree at idx with change. '''
        if change == 0:
            return
        while idx <= self.size:
            freq, resp = self._get_elem(idx)
            self._set_elem(idx, freq, resp + change)
            idx += (idx & -idx)

    def sum(self, idx):
        ''' The sum at idx. '''
        sum = 0
        while idx > 0:
            sum += self._get_elem(idx)[1]
            idx -= (idx & -idx)
        return sum

    def display(self):
        print "size is %d" % self.size
        for i, v in enumerate(self.elems):
            print "%d: %s %d" % (i+1, v, self.sum(i+1))


if __name__ == "__main__":
    import random

    vals = [1, 0, 2, 1, 1, 3, 0, 4, 2, 5, 2, 2, 3, 1, 0, 2]
    bt = BinaryIndexedTree(len(vals))
    indices = [i for i in xrange(0, len(vals))]
    random.seed(373813)
    random.shuffle(indices)
    for i in indices:
        print "Update: %d -> %d" % (i+1, vals[i])
        bt.update(i + 1, vals[i])
    bt.display()
