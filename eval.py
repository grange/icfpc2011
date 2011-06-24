#!/usr/bin/env python

# zm == Zombie Mode
# zombie scan is done immidiately after any operation, 
# and not before player turn, as in docs

import array
import inspect
import copy
import sys
sys.setrecursionlimit(100000)

MAX_OPS = 1000

# lame globals bolted on
# ich habe kopfsterben
global_op_counter = None
def reset_global_op_counter(o=MAX_OPS):
    global global_op_counter
    global_op_counter = OpCounter(o)

global_total_ops = {
    'call': 0,
    'put': 0
}


def split_dead_and_alive(set_, com):
    dead = []
    alive = []
    for i,v in com:
        if set_[i].health <= 0:
            dead.append((i,v))
        else:
            alive.append((i,v))
    return dead, alive


class Board(object):
    def __init__(self, invert=None, debug=False, averager_window=100, collect_stats=True, _make_inverted=True):
        self.prop = invert.opp if invert else Set()
        self.opp = invert.prop if invert else Set()
        self.debug = debug # print field to stdout after every operation
        self.collect_stats = collect_stats

        def mk_counters():
            types = (
                'add',  # player adds card to slot
                'call', # number of calls made by functions in the slot
                'get',  # number of Gets from the slot
                'put',  # number of puts to the slot
            )
            return dict([(t, SlotOpCounter(averager_window)) for t in types])
        
        self.prop_counters = invert.opp_counters if invert else mk_counters()
        self.opp_counters = invert.prop_counters if invert else mk_counters()
        self.zombies = set()
        if _make_inverted:
            self.inv = Board(invert=self, debug=debug, averager_window=averager_window,
                    collect_stats=collect_stats, _make_inverted=False)

    def prop_inc(self, type_, slot, count=1):
        self.prop_counters[type_].inc(slot, count=count)

    def prop_mru(self, type_):
        """Gets array [(slot_no, avg_uses_per_turn), (..., ...), ...]
           that contains average usage of every slot. Average is calculated
           for 'averager_window' turns. Description of type_ see at mk_counters.
        """
        return self.prop_counters[type_].mru()

    def opp_mru(self, type_):
        """Get mru of oppenent, see prop_mru()"""
        return self.opp_counters[type_].mru()

    def prop_mru_dead_alive(self, type_):
        """Returns two arrays of opp_mru(), first for dead slots, second for alive"""
        return split_dead_and_alive(self.prop, self.prop_mru(type_))

    def opp_mru_dead_alive(self, type_):
        """Returns two arrays of prop_mru(), first for dead slots, second for alive"""
        return split_dead_and_alive(self.opp, self.opp_mru(type_))

    def opp_tree_sizes(self):
        """Returns list of tuples (slot, tree_size) sorted by tree_size"""
        pairs = [((1 if is_int(s.value) else s.value.tree_size()), i) for i,s in enumerate(self.opp)]
        return [(i,v) for v,i in sorted(pairs, reverse=True)]

    def opp_tree_sizes_dead_alive(self):
        """Returns two arrays of opp_tree_sizes(), first for dead slots, second for alive"""
        return split_dead_and_alive(self.opp, self.opp_tree_sizes())

    def _check_slot(self, i):
        if self.prop[i].health <= 0:
            raise ProgError('Slot %d is dead, cannot apply'%i)

    def _apply(self, lr, i, card_cls):
        if lr not in (1,2):
            raise Exception('lr invalid')

        #print >>sys.stderr, i
        if self.collect_stats:
            count0 = copy.copy(global_total_ops)

        try:
            self._check_slot(i)
            check_c(card_cls)
            self.prop_inc('add', i)

            if lr == 1:
                self.prop[i].value = card_cls(self)(self.prop[i].value, ctr=OpCounter())
            if lr == 2:
                check_f(self.prop[i].value)
                self.prop[i].value = self.prop[i].value(card_cls(self), ctr=OpCounter())

        except (EvalError, OpLimitError, ProgError), e:
            if self.debug:
                print >>sys.stderr, 'ERROR', e
            self.prop[i].value = I(self)
        finally:
            #print >>sys.stderr, global_total_ops
            if self.collect_stats:
                for k,v in global_total_ops.items():
                    #print >>sys.stderr, k, i, global_total_ops[k] - count0[k]
                    self.prop_inc(k, i, global_total_ops[k] - count0[k])

                for t, op_c in self.prop_counters.items():
                    op_c.end_turn()

            self.zombie_scan()
            if self.debug:
                if lr == 1:
                    print >>sys.stderr, 'Apply %s to slot %s' % (card_cls(self), i)
                if lr == 2:
                    print >>sys.stderr, 'Apply slot %d to %s' % (i, card_cls(self))
                print >>sys.stderr, self
                print >>sys.stderr 

    def apply_left(self, i, card_cls):
        self._apply(1, i, card_cls)

    def apply_right(self, i, card_cls):
        self._apply(2, i, card_cls)

    def zombie_scan(self):
        # I need to scan only inverted board
        zombies = sorted(list(self.inv.zombies))
        self.inv.zombies = set()
        for i in zombies:
            s = self.opp[i]
            #print i
            if s.health == -1:
                try:
                    check_f(s.value)
                    s.value(I(self.inv), zm=True, ctr=OpCounter())
                except (EvalError, OpLimitError, ProgError), e:
                    if self.debug:
                        print >>sys.stderr, e
                s.health = 0
                s.value = I(self.inv)


    def __repr__(self):
        lines = []
        w = 80
        def mkline(slot):
            not_changed = slot.health==10000 and repr(slot.value).strip()=='I'
            s = '%5d %s' % (slot.health, repr(slot.value))
            return not_changed, s + (' '*(w - len(s)))

        for i in range(256):
            c1, opp = mkline(self.opp[i])
            c2, prop = mkline(self.prop[i])
            if not c1 or not c2:
                lines.append('%3d %s%s' % (i, prop, opp))
        return '\n'.join(lines)

    def __str__(self):
        return repr(self)

    def turn(self, lr, i, card):
        cls = name_to_card[card]
        if lr==1:
            self.apply_left(i, cls)
        elif lr==2:
            self.apply_right(i, cls)
        else:
            raise ProgError('Unknown order: %d' % lr)


class Set(list):
    def __init__(self):
        for i in xrange(256):
            self.append(Slot(self))


class Slot(object):
    def __init__(self, set_):
        self.set_ = set_
        self.health = 10000
        self.value = I(set_)


class SlotOpCounter(object):
    """Counts number of operations in slots.
    Operations are arbitrary.
    """
    N = 256
    def __init__(self, n=10):
        """n is number of turns which are remembered."""
        self.n = n
        self.slices = [[0]*self.N]
        self.total = [0]*self.N

    def inc(self, i, count=1):
        self.slices[0][i] += count
        self.total[i] += count

    def end_turn(self):
        t = self.total
        if len(self.slices) > self.n:
            rm = self.slices[-1]
            self.slices = self.slices[:-1]
            for i in range(len(t)):
                t[i] -= rm[i]


        self.slices.insert(0, [0]*self.N)

    def mru(self):
        """Most recently used"""
        numbered = [(v,i) for i,v in enumerate(self.total)]
        numbered.sort(reverse=True)
        l = len(self.slices) - 1
        return [(i, float(v)/l) for v,i in numbered]


class OpCounter(object):
    """Counts number of operations in evaluation"""
    def __init__(self, ops=MAX_OPS):
        self.ops = ops

    def dec(self, count=1):
        """Should be called before actual evaluation"""
        self.ops -= count
        if self.ops < 0:
            raise OpLimitError("Operation limit reached")

class Card(object):
    args_n = None

    def __init__(self, board):
        self.board = board
        self.args = []

        if self.args_n == None:
            #print >>sys.stderr, 'ARGS OF', self.__class__
            args, varargs, keywords, defaults = inspect.getargspec(self.ev)
            self.__class__.args_n = len(args) - 1 - len(defaults)

    def __repr__(self):
        return '%s %s' % (self.__class__.__name__, ' '.join(map(repr, self.args)))

    def __str__(self):
        return repr(self)

    def __call__(self, *args, **kwargs):
        zm = kwargs.get('zm', False)
        ctr = kwargs.get('ctr', global_op_counter)
        #print 'CALL', self.args, args
        c = copy.copy(self)
        c.args = list(self.args)
        c.args.extend(args)

        ctr.dec(len(args))

        if len(c.args) > c.args_n:
            raise ProgError('Too many args for %s' % self)

        if len(c.args) < c.args_n:
            return c

        global_total_ops['call'] += 1
        
        #ctr.dec()
        return c.ev(*[(a if is_int(a) else a(zm=zm, ctr=ctr)) for a in c.args], zm=zm, ctr=ctr)

    def __copy__(self):
        c = self.__class__(self.board)
        c.args = list(self.args) #copy.copy(self.args)
        return c

    def __deepcopy__(self, memo):
        c = self.__class__(self.board)
        c.args = copy.deepcopy(self.args, memo)
        return c

    def __eq__(self, other):
        #print 'EQ', self, other
        return (self.__class__ == other.__class__ and
                self.args == other.args)

    def __ne__(self, other):
        #print 'NE', self, other
        return not self == other

    def tree_size(self):
        return sum([1] + [(1 if is_int(a) else a.tree_size()) for a in self.args])
        

class EvalError(Exception):
    pass

class OpLimitError(EvalError):
    pass

class ProgError(Exception):
    pass

# ---------------------------------------- Actual cards

def is_int(x):
    return isinstance(x, int) or isinstance(x, long)

def check_int(*args):
    for i, x in enumerate(args):
        if not is_int(x):
            raise EvalError('%s in not integer (%d-th var)' % (repr(x), i))

def check_c(c):
    if not issubclass(c, Card):
        raise EvalError('%s in not a subclass' % c)

def check_f(x):
    if not issubclass(x.__class__, Card):
        raise EvalError('%s in not a function' % x)

def check_slot_n(*args):
    for i, x in enumerate(args):
        if x < 0 and x > 255:
            raise EvalError('Card number %d is out of range (%d-th var)' % (x, i))


class I(Card):
    def ev(self, x, zm=False, ctr=None):
        return x


class Zero(Card):
    def ev(self, zm=False, ctr=None):
        return 0


class Succ(Card):
    def ev(self, x, zm=False, ctr=None):
        check_int(x)
        return min(x + 1, 65535)


class Dbl(Card):
    def ev(self, x, zm=False, ctr=None):
        check_int(x)
        # TODO: what if x is negative? No limit?
        return min(x*2, 65535)


class Get(Card):
    def ev(self, x, zm=False, ctr=None):
        check_int(x)
        check_slot_n(x)
        self.board.prop_inc('get', x)
        v = self.board.prop[x]
        if v.health <= 0:
            raise EvalError('Get: Slot %d is dead with health %d' % (x, v.health))
            
        return v.value


class Put(Card):
    def ev(self, x, zm=False, ctr=None):
        global_total_ops['put'] += 1
        return I(self.board)


class S(Card):
    # TODO test
    def ev(self, f, g, x, zm=False, ctr=None):
        check_f(f)
        h = f(x, zm=zm, ctr=ctr)
        check_f(g)
        y = g(x, zm=zm, ctr=ctr)
        check_f(h)
        return h(y, zm=zm, ctr=ctr) # that's  f(x)(g(x))


class K(Card):
    def ev(self, x, y, zm=False, ctr=None):
        return x


class Inc(Card):
    def ev(self, i, zm=False, ctr=None):
        check_int(i)
        check_slot_n(i)
        if not zm:
            slot = self.board.prop[i]
            if slot.health > 0 and slot.health < 65535:
                slot.health += 1
        else:
            # zombie was constucted on prop board, but
            # decrement should go to opponent
            slot = self.board.opp[i]
            if slot.health > 0:
                slot.health -= 1
            
        return I(self.board) 


class Dec(Card):
    def ev(self, i, zm=False, ctr=None):
        check_int(i)
        check_slot_n(i)

        if not zm:
            slot = self.board.opp[255-i]
            if slot.health > 0:
                slot.health -= 1
        else:
            # see comment in Inc
            slot = self.board.prop[255-i]
            if slot.health > 0 and slot.health < 65535:
                slot.health += 1
            
        return I(self.board) 


class Attack(Card):
    def ev(self, i, j, n, zm=False, ctr=None):
        check_int(i, n)
        check_slot_n(i)

        if not zm:
            attacker = self.board.prop[i]
            if n > attacker.health:
                raise EvalError('Attack: not enough health: h=%d, n=%d' % (attacker.health, n))

            attacker.health -= n

            check_int(j)
            check_slot_n(j)
            defender = self.board.opp[255-j]
            if defender.health > 0:
                defender.health = max(0, defender.health - n*9/10)
        else:
            # see comment in Inc
            attacker = self.board.opp[i]
            if n > attacker.health:
                raise EvalError('Attack: not enough health: h=%d, n=%d' % (attacker.health, n))

            attacker.health -= n

            check_int(j)
            check_slot_n(j)
            defender = self.board.prop[255-j]
            if defender.health > 0:
                defender.health = min(defender.health + n*9/10, 65535)

        return I(self.board)


class Help(Card):
    def ev(self, i, j, n, zm=False, ctr=None):
        check_int(i, n)
        check_slot_n(i)

        if not zm:
            src = self.board.prop[i]
            if n > src.health:
                raise EvalError('Not enough health, i=%d, h=%d' % (i, src.health))

            src.health -= n

            check_int(j)
            check_slot_n(j)
            recv = self.board.prop[j]
            if recv.health > 0:
                recv.health = min(recv.health + n*11/10, 65535)
        else:
            # boards reversed, see comment for Inc
            src = self.board.opp[i]
            if n > src.health:
                raise EvalError('Not enough health, i=%d, h=%d' % (i, src.health))

            src.health -= n

            check_int(j)
            check_slot_n(j)
            recv = self.board.opp[j]
            if recv.health > 0:
                recv.health = max(0, recv.health - n*11/10)

        return I(self.board)


class Copy(Card):
    def ev(self, i, zm=False, ctr=None):
        check_int(i)
        check_slot_n(i)
        return self.board.opp[255-i].value


class Revive(Card):
    def ev(self, i, zm=False, ctr=None):
        check_int(i)
        check_slot_n(i)
        s = self.board.prop[i]
        if s.health <= 0:
            s.health = 1
        return I(self.board)


class Zombie(Card):
    def ev(self, i, x, zm=False, ctr=None):
        check_int(i)
        check_slot_n(i)
        s = self.board.opp[255-i]
        self.board.inv.zombies.add(255-i)
        if s.health > 0:
            raise EvalError('Opponent slot %d is alive' % (255-i))

        s.health = -1
        s.value = x
        return I(self.board)


name_to_card = {
    'I': I,
    'zero': Zero,
    'succ': Succ,
    'dbl': Dbl,
    'get': Get,
    'put': Put,
    'S': S,
    'K': K,
    'inc': Inc,
    'dec': Dec,
    'attack': Attack,
    'help': Help,
    'copy': Copy,
    'revive': Revive,
    'zombie': Zombie
}

if __name__ == '__main__':
    b = Board()
    print Zero(b)
    print Succ(b)(Zero(b)), '== 1'
    print Get(b)(Zero(b))
    print Put(b)(Zero(b))
    print S(b)(Get(b), Succ(b))
    print S(b)(Get(b), Succ(b), Zero(b))
    print K(b)(Inc(b), Zero(b))

    print 'attack'
    b.prop[0].health = 20
    b.opp[255].health = 50
    print Attack(b)(Zero(b), Zero(b), Dbl(b)(Succ(b)(Zero(b))))
    print b.prop[0].health, b.opp[255].health

    print
    print 'help'
    b.prop[1].health = 100
    b.prop[2].health = 3
    print Help(b)(1, 2, 50)
    print b.prop[1].health, b.prop[2].health

    print
    print 'copy'
    b.opp[2].value = 3
    print Copy(b)(100)
    print Copy(b)(2)

    print
    print 'revive'
    b.prop[2].health = -1
    print Revive(b)(2)
    print b.prop[2].health

    print
    print 'zombie'
    b.opp[2].health = 0
    print Zombie(b)(253, Attack(b))
    print b.opp[2].health, b.opp[2].value

