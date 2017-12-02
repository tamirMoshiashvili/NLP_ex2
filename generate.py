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

    def gen(self, symbol):
        if self.is_terminal(symbol):
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        return self.gen("ROOT")

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

    pcfg = PCFG.from_file(sys.argv[1])

    argc = len(sys.argv) - 1
    if argc > 3 or argc == 0 or argc == 2:
        exit_with_msg('invalid number of arguments')

    numSentences = 0
    if argc == 1:
        numSentences = 1
    elif sys.argv[2] != '-n':
        exit_with_msg('wrong format - ' + sys.argv[2] + ', valid format is -n')
    else:
        numSentences = int(sys.argv[3])
        if numSentences < 1:
            exit_with_msg('number of sentences need to be a positive value')

    # print sentences
    for _ in xrange(numSentences):
        print pcfg.random_sent()
