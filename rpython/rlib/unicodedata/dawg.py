# Original Algorithm:
# By Steve Hanov, 2011. Released to the public domain.
# Please see http://stevehanov.ca/blog/index.php?id=115 for the accompanying article.
#
# Adapted for RPython by cfbolz
#
# Based on Daciuk, Jan, et al. "Incremental construction of minimal acyclic finite-state automata."
# Computational linguistics 26.1 (2000): 3-16.
#
# Updated 2014 to use DAWG as a mapping; see
# Kowaltowski, T.; CL. Lucchesi (1993), "Applications of finite automata representing large vocabularies",
# Software-Practice and Experience 1993

from pprint import pprint
from collections import defaultdict
import sys
import time


# This class represents a node in the directed acyclic word graph (DAWG). It
# has a list of edges to other nodes. It has functions for testing whether it
# is equivalent to another node. Nodes are equivalent if they have identical
# edges, and each identical edge leads to identical states. The __hash__ and
# __eq__ functions allow it to be used as a key in a python dictionary.


class DawgNode(object):

    def __init__(self, dawg):
        self.id = dawg.next_id
        dawg.next_id += 1
        self.final = False
        self.edges = {}

        # Number of end nodes reachable from this one.
        self.count = 0

        self.linear_edges = None # later: list of (string, next_state)

    def __str__(self):
        if self.final:
            arr = ["1"]
        else:
            arr = ["0"]

        for (label, node) in sorted(self.edges.items()):
            arr.append(label)
            arr.append(str(node.id))

        return "_".join(arr)
    __repr__ = __str__

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def num_reachable_linear(self):
        # if a count is already assigned, return it
        if self.count:
            return self.count

        # count the number of final nodes that are reachable from this one.
        # including self
        count = 0
        if self.final:
            count += 1
        for label, node in self.linear_edges:
            count += node.num_reachable_linear()

        self.count = count
        return count


class Dawg(object):
    def __init__(self):
        self.previous_word = ""
        self.next_id = 0
        self.root = DawgNode(self)

        # Here is a list of nodes that have not been checked for duplication.
        self.unchecked_nodes = []

        # Here is a list of unique nodes that have been checked for
        # duplication.
        self.minimized_nodes = {}

        # Here is the data associated with all the nodes
        self.data = {}
        self.inverse = {}

    def insert(self, word, data):
        assert [0 <= ord(c) < 128 for c in word]
        if word <= self.previous_word:
            raise Exception("Error: Words must be inserted in alphabetical order.")
        if data in self.inverse:
            raise Exception("data %s is duplicate, got it for word %s and now %s" % (data, self.inverse[data], word))

        # find common prefix between word and previous word
        common_prefix = 0
        for i in range(min(len(word), len(self.previous_word))):
            if word[i] != self.previous_word[i]:
                break
            common_prefix += 1

        # Check the unchecked_nodes for redundant nodes, proceeding from last
        # one down to the common prefix size. Then truncate the list at that
        # point.
        self._minimize(common_prefix)

        self.data[word] = data
        self.inverse[data] = word

        # add the suffix, starting from the correct node mid-way through the
        # graph
        if len(self.unchecked_nodes) == 0:
            node = self.root
        else:
            node = self.unchecked_nodes[-1][2]

        for letter in word[common_prefix:]:
            next_node = DawgNode(self)
            node.edges[letter] = next_node
            self.unchecked_nodes.append((node, letter, next_node))
            node = next_node

        node.final = True
        self.previous_word = word

    def finish(self):
        # minimize all unchecked_nodes
        self._minimize(0)

        self._linearize_edges()

        topoorder, linear_data, inverse = self._topological_order()
        return self.compute_packed(topoorder), linear_data, inverse

    def _minimize(self, down_to):
        # proceed from the leaf up to a certain point
        for i in range(len(self.unchecked_nodes) - 1, down_to - 1, -1):
            (parent, letter, child) = self.unchecked_nodes[i]
            if child in self.minimized_nodes:
                # replace the child with the previously encountered one
                parent.edges[letter] = self.minimized_nodes[child]
            else:
                # add the state to the minimized nodes.
                self.minimized_nodes[child] = child
            self.unchecked_nodes.pop()

    def _lookup(self, word):
        node = self.root
        skipped = 0  # keep track of number of final nodes that we skipped
        index = 0
        while index < len(word):
            for label, child in node.linear_edges:
                if word[index] == label[0]:
                    if word[index:index + len(label)] == label:
                        if node.final:
                            skipped += 1
                        index += len(label)
                        node = child
                        break
                    else:
                        return None
                skipped += child.count
            else:
                return None
        return skipped

    def enum_all_nodes(self):
        stack = [self.root]
        done = set()
        while stack:
            node = stack.pop()
            if node.id in done:
                continue
            yield node
            done.add(node.id)
            for label, child in sorted(node.edges.items()):
                stack.append(child)

    def prettyprint(self):
        for node in sorted(self.enum_all_nodes(), key=lambda e: e.id):
            print("{}: ({}) {}{}".format(node.id, node, node.count, " final" if node.final else ""))
            for label, child in sorted(node.edges.items()):
                print("    {} goto {}".format(label, child.id))

    def _inverse_lookup(self, number):
        assert 0, "not working in the current form, but keep it as the pure python version of compact lookup"
        result = []
        node = self.root
        while 1:
            if node.final:
                if pos == 0:
                    return "".join(result)
                pos -= 1
            for label, child in sorted(node.edges.items()):
                nextpos = pos - child.count
                if nextpos < 0:
                    result.append(label)
                    node = child
                    break
                else:
                    pos = nextpos
            else:
                assert 0

    def _linearize_edges(self):
        # compute "linear" edges. the idea is that long chains of edges without
        # any of the intermediate states being final or any extra incoming or
        # outgoing edges can be represented by having removing them, and
        # instead using longer strings as edge labels (instead of single
        # characters)
        incoming = defaultdict(list)
        nodes = sorted(self.enum_all_nodes(), key=lambda e: e.id)
        for node in nodes:
            for label, child in sorted(node.edges.items()):
                incoming[child].append(node)
        for node in nodes:
            node.linear_edges = []
            for label, child in sorted(node.edges.items()):
                s = [label]
                while len(child.edges) == 1 and len(incoming[child]) == 1 and not child.final:
                    (c, child), = child.edges.items()
                    s.append(c)
                node.linear_edges.append((''.join(s), child))

    def _topological_order(self):
        # compute reachable linear nodes, and the set of incoming edges for each node
        order = []
        stack = [self.root]
        seen = set()
        while stack:
            # depth first traversal
            node = stack.pop()
            if node.id in seen:
                continue
            seen.add(node.id)
            order.append(node)
            for label, child in node.linear_edges:
                stack.append(child)

        # do a (slighly bad) topological sort
        incoming = defaultdict(set)
        for node in order:
            for label, child in node.linear_edges:
                incoming[child].add((label, node))
        no_incoming = [order[0]]
        topoorder = []
        positions = {}
        while no_incoming:
            node = no_incoming.pop()
            topoorder.append(node)
            positions[node] = len(topoorder)
            # use "reversed" to make sure that the linear_edges get reorderd
            # from their alphabetical order as little as necessary (no_incoming
            # is LIFO)
            for label, child in reversed(node.linear_edges):
                incoming[child].discard((label, node))
                if not incoming[child]:
                    no_incoming.append(child)
                    del incoming[child]
        # check result
        assert set(topoorder) == set(order)
        assert len(set(topoorder)) == len(topoorder)

        for node in order:
            node.linear_edges.sort(key=lambda element: positions[element[1]])

        for node in order:
            for label, child in node.linear_edges:
                assert positions[child] > positions[node]
        # number the nodes. afterwards every input string in the set has a
        # unique number in the 0 <= number < len(data). We then put the data in
        # self.data into a linear list using these numbers as indexes.
        topoorder[0].num_reachable_linear()
        linear_data = [None] * len(self.data)
        inverse = {} # maps value back to index
        for word, value in self.data.items():
            index = self._lookup(word)
            linear_data[index] = value
            inverse[value] = index

        return topoorder, linear_data, inverse

    def compute_packed(self, order):
        # assign offsets to every node
        for i, node in enumerate(order):
            # we don't know position of the edge yet, just use something big as
            # the starting position. we'll have to do further iterations anyway,
            # but the size is at least a lower limit then
            node.packed_offset = 2 ** 30 + i * 2 ** 10

        # due to the varint encoding of edge targets we need to run this to
        # fixpoint
        last_result = None
        while 1:
            result = bytearray()
            result_pp = bytearray()
            for node in order:
                offset = node.packed_offset = len(result)
                encode_varint_unsigned(number_add_bits(node.count, node.final), result)
                if len(node.linear_edges) == 0:
                    assert node.final
                    encode_varint_unsigned(0, result) # add a 0 saying "done"
                #result_pp.extend("%r # N pos=%s count=%s%s\n" % (bytes(result[offset:]), offset, node.count, " final" if node.final else ""))
                result_pp.extend("%r\n" % (bytes(result[offset:]), ))
                prev_printed = len(result)
                prev_child_offset = len(result)
                for edgeindex, (label, targetnode) in enumerate(node.linear_edges):
                    child_offset = targetnode.packed_offset
                    child_offset_difference = child_offset - prev_child_offset

                    info = number_add_bits(child_offset_difference, len(label) == 1, edgeindex == len(node.linear_edges) - 1)
                    if edgeindex == 0:
                        assert info != 0
                    encode_varint_unsigned(info, result)
                    prev_child_offset = child_offset
                    if len(label) > 1:
                        encode_varint_unsigned(len(label), result)
                    result.extend(label)
                    result_pp.extend(" %r\n" % (bytes(result[prev_printed:]), ))
                    prev_printed = len(result)
                node.packed_size = len(result) - node.packed_offset
            if result == last_result:
                break
            last_result = result
        self.packed = result
        self.packed_pp = result_pp
        return bytes(result)


# ______________________________________________________________________
# the following functions are used from RPython to interpret the packed
# representation

from rpython.rlib import objectmodel

def number_add_bits(x, *bits):
    for bit in bits:
        assert bit == 0 or bit == 1
        x = (x << 1) | bit
    return x

@objectmodel.specialize.arg(1)
@objectmodel.always_inline
def number_split_bits(x, n, acc=()):
    if n == 1:
        return x >> 1, x & 1
    if n == 2:
        return x >> 2, (x >> 1) & 1, x & 1
    assert 0, "implement me!"

def encode_varint_unsigned(i, res):
    # https://en.wikipedia.org/wiki/LEB128 unsigned variant
    more = True
    startlen = len(res)
    if i < 0:
        raise ValueError("only positive numbers supported", i)
    while more:
        lowest7bits = i & 0b1111111
        i >>= 7
        if i == 0:
            more = False
        else:
            lowest7bits |= 0b10000000
        res.append(chr(lowest7bits))
    return len(res) - startlen

@objectmodel.always_inline
def decode_varint_unsigned(b, index=0):
    res = 0
    shift = 0
    while True:
        byte = ord(b[index])
        res = res | ((byte & 0b1111111) << shift)
        index += 1
        shift += 7
        if not (byte & 0b10000000):
            return res, index

@objectmodel.always_inline
def decode_node(packed, node):
    x, node = decode_varint_unsigned(packed, node)
    node_count, final = number_split_bits(x, 1)
    return node_count, final, node

@objectmodel.always_inline
def decode_edge(packed, edgeindex, prev_child_offset, offset):
    x, offset = decode_varint_unsigned(packed, offset)
    if x == 0 and edgeindex == 0:
        raise KeyError # trying to decode past a final node
    child_offset_difference, len1, final_edge = number_split_bits(x, 2)
    child_offset = prev_child_offset + child_offset_difference
    if len1:
        size = 1
    else:
        size, offset = decode_varint_unsigned(packed, offset)
    return child_offset, final_edge, size, offset

@objectmodel.always_inline
def _match_edge(packed, s, size, node_offset, stringpos):
    if size > 1 and stringpos + size > len(s):
        # past the end of the string, can't match
        return False
    for i in range(size):
        if packed[node_offset + i] != s[stringpos + i]:
            # if a subsequent char of an edge doesn't match, the word isn't in
            # the dawg
            if i > 0:
                raise KeyError
            return False
    return True

def lookup(packed, data, s):
    return data[_lookup(packed, s)]

def _lookup(packed, s):
    stringpos = 0
    node_offset = 0
    skipped = 0  # keep track of number of final nodes that we skipped
    while stringpos < len(s):
        node_count, final, edge_offset = decode_node(packed, node_offset)
        if final:
            skipped += 1
        prev_child_offset = edge_offset
        edgeindex = 0
        while 1:
            child_offset, final_edge, size, edgelabel_chars_offset = decode_edge(packed, edgeindex, prev_child_offset, edge_offset)
            edgeindex += 1
            prev_child_offset = child_offset
            if _match_edge(packed, s, size, edgelabel_chars_offset, stringpos):
                # match
                stringpos += size
                node_offset = child_offset
                break
            if final_edge:
                raise KeyError
            child_count, _, _ = decode_node(packed, child_offset)
            skipped += child_count
            edge_offset = edgelabel_chars_offset + size
    node_count, final, _ = decode_node(packed, node_offset)
    if final:
        return skipped
    raise KeyError

def inverse_lookup(packed, inverse, x):
    pos = inverse[x]
    return _inverse_lookup(packed, pos)

def _inverse_lookup(packed, pos):
    from rpython.rlib import rstring
    result = rstring.StringBuilder(42) # max size is like 83
    node_offset = 0
    while 1:
        node_count, final, edge_offset = decode_node(packed, node_offset)
        if final:
            if pos == 0:
                return result.build()
            pos -= 1
        prev_child_offset = edge_offset
        edgeindex = 0
        while 1:
            child_offset, final_edge, size, edgelabel_chars_offset = decode_edge(packed, edgeindex, prev_child_offset, edge_offset)
            edgeindex += 1
            prev_child_offset = child_offset
            child_count, _, _ = decode_node(packed, child_offset)
            nextpos = pos - child_count
            if nextpos < 0:
                assert edgelabel_chars_offset >= 0
                result.append_slice(packed, edgelabel_chars_offset, edgelabel_chars_offset + size)
                node_offset = child_offset
                break
            elif not final_edge:
                pos = nextpos
                edge_offset = edgelabel_chars_offset + size
            else:
                raise KeyError
        else:
            raise KeyError

# ______________________________________________________________________
# some functions to efficiently encode the relatively dense
# charcode-to-position dictionary

MAXBLANK = 8
MINLIST = 5

def findranges(d):
    ranges = []
    for i in range(max(d)+1):
        if i in d:
            if not ranges:
                ranges.append((i,i))
                last = i
                continue
            if last + 1 == i:
                ranges[-1] = (ranges[-1][0], i)
            else:
                ranges.append((i,i))
            last = i
    return ranges

def collapse_ranges(ranges):
    collapsed = [ranges[0]]
    for i in range(1, len(ranges)):
        lows, lowe = collapsed[-1]
        highs, highe = ranges[i]
        if highs - lowe < MAXBLANK:
            collapsed[-1] = (lows, highe)
        else:
            collapsed.append(ranges[i])

    return collapsed


# ______________________________________________________________________
# code generation

empty_functions = """
def dawg_lookup(name):
    raise KeyError
def lookup_charcode(code):
    raise KeyError
"""

def build_compression_dawg(outfile, ucdata):
    outfile.print_comment("_" * 60)
    outfile.print_comment("output from build_compression_dawg")
    outfile.print_code('from rpython.rlib.rarithmetic import intmask, r_int32')
    outfile.print_code('from rpython.rlib.unicodedata.supportcode import signed_ord, _all_short, _all_ushort, _all_int32, _all_uint32')

    if not ucdata:
        outfile.print_code(empty_functions)
        return

    d = Dawg()
    for name, value in sorted(ucdata.items()):
        d.insert(name, value)
    packed, pos_to_code, reversedict = d.finish()
    print "size of dawg [KiB]", round(len(packed) / 1024, 2), len(pos_to_code)
    outfile.print_code("from rpython.rlib.unicodedata.dawg import _lookup as _dawg_lookup, _inverse_lookup")
    outfile.print_code("packed_dawg = (")
    outfile.print_uncounted(d.packed_pp)
    outfile.print_code(")")
    outfile._estimate_string("dawg", bytes(d.packed))
    outfile.print_listlike("pos_to_code", pos_to_code, "dawg pos_to_code")

    outfile.print_code("""
def lookup_charcode(c):
    pos = _charcode_to_pos(c)
    return _inverse_lookup(packed_dawg, pos)

def dawg_lookup(n):
    return pos_to_code(_dawg_lookup(packed_dawg, n))
    """)


    function = ["def _charcode_to_pos(code):", "    res = -1"]
    ranges = collapse_ranges(findranges(reversedict))
    prefix = ""
    for low, high in ranges:
        if high - low <= 5:
            for code in range(low, high + 1):
                if code in reversedict:
                    function.append(
                        "    %sif code == %d: res = %s" %
                        (prefix, code, reversedict[code]))
                    prefix = "el"
            continue

        name = "_charcode_to_pos_%d" % (low,)
        lst = []
        for code in range(low, high + 1):
            if code in reversedict:
                lst.append(reversedict[code])
            else:
                lst.append(-1)
        outfile.print_listlike(name, lst, "dawg inverse")
        function.append(
            "    %sif %d <= code <= %d: res = %s(code-%d)" % (
            prefix, low, high, name, low))
        prefix = "el"


    function.append("    if res == -1:")
    function.append("        raise KeyError(code)")
    function.append("    return res")
    outfile.print_code('\n'.join(function))
    outfile.print_comment("end output from build_compression_dawg")
    return d
