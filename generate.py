from collections import defaultdict
import random


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def gen(self, symbol, tree_structure):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            generated = " ".join(self.gen(s, tree_structure) for s in expansion)
            if tree_structure:
                generated = '(' + symbol + ' ' + generated + ')'
            return generated

    def random_sent(self, tree_structure):
        return self.gen("ROOT", tree_structure)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def exit_with_msg(msg):
    print 'Error: ' + msg
    exit(0)


if __name__ == '__main__':
    import sys

    argv = sys.argv
    argc = len(argv) - 1
    if argc == 0:
        exit_with_msg('need grammar file')

    pcfg = PCFG.from_file(sys.argv[1])

    num_sentences = 1
    is_tree_structure = False
    sentence_num_token = '-n'
    tree_structure_token = '-t'

    if sentence_num_token in argv:  # -n
        num_sentences = int(argv[argv.index(sentence_num_token) + 1])
        if num_sentences < 1:
            exit_with_msg('number of sentences need to be a positive number')

    if tree_structure_token in argv:  # -t
        is_tree_structure = True

    # print sentences
    for _ in xrange(num_sentences):
        print pcfg.random_sent(is_tree_structure)
