class SEGTreeNode(object):
    def __init__(self, leftchild, rightchild, index, valfunc):
        self.lc, self.rc = leftchild, rightchild
        if leftchild == None or rightchild == None:
            # leaf node
            self.interval = (index, index)
            assert(valfunc and hasattr(valfunc, '__call__'))
            self.maxnode = self
        else:
            self.interval = (leftchild.interval[0], rightchild.interval[1])
            keyfunc = lambda x : valfunc(x.maxnode.interval[0])
            self.maxnode = max(leftchild, rightchild, key=keyfunc).maxnode


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

def segtree_build_bottomup(left, right, valfunc):
    ''' Builds in bottom-up fasion: starting from leaf nodes, each node is paired
    with the next one, an unpaired node gets "promoted" to the next level. '''
    def _pair_nodes(nodes):
        res = []
        num = len(nodes)
        i = 0
        while num > 1:
            lc, rc = nodes[i], nodes[i + 1]
            res.append(SEGTreeNode(lc, rc, None, valfunc))
            i += 2
            num -= 2
        if num == 1:
            # push in the "odd" node
            res.append(nodes[i])
        return res
    # Build leaf nodes:
    nodes = [SEGTreeNode(None, None, i, valfunc) \
                 for i in xrange(left, right + 1)]
    while len(nodes) > 1:
        nodes = _pair_nodes(nodes)
    return nodes[0]

def segtree_find_leaf(root, idx):
    ''' Find an return a leaf node with index ''idx''. '''
    if root.idx and root.idx == idx:
        return root
    elif idx < root.interval[0] or idx > root.interval[1]:
        raise RuntimeError("index %d outside of segment tree" % idx)
    midleft = root.lc.interval[1]
    if idx <= midleft:
        return segtree_find_leaf(root.lc, idx)
    else:
        return segtree_find_leaf(root.rc, idx)

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
            assert(node.interval[0] == node.interval[1])
        else:
            keyfunc = lambda x : valfunc(x.maxnode.interval[0])
            node.maxnode = max(node.lc, node.rc, key=keyfunc).maxnode

def segtree_print(root):
    _segtree_print([(root, "")])

def _segtree_print(nodes):
    while len(nodes):
        n, decor = nodes.pop(0)
        if n.lc:
            nodes.append((n.lc, "L"))
        if n.rc:
            nodes.append((n.rc, "R"))
        print "%s:%s:(max=%s)" % (decor, n.interval, n.maxnode.interval)

negative_infinity_func = lambda idx: float("-inf")

if __name__ == "__main__":
    l1 = [9, 2, 6, 3, 1, 5, 0, 7, 6]
    size = len(l1)
    # Initialize tree with negative infinity
    print "Building top-down:"
    t1 = segtree_build_topdown(1, size, negative_infinity_func)
    #print "Building bottom-up:"
    #t1 = segtree_build_bottomup(1, size, negative_infinity_func)
    segtree_print(t1)
    value_func = lambda idx: l1[idx - 1]
    for i, v in enumerate(l1):
        segtree_update(t1, i+1, value_func)
    print "After updates:"
    segtree_print(t1)
