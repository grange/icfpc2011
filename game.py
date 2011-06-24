#!/usr/bin/env python
import sys
from eval import Board, ProgError, EvalError, OpLimitError

class GameState(object):
    def __init__(self, player, eval_=True, debug=False, collect_stats=False):
        self.player = int(player)
        self.eval = eval_
        self.debug = debug
        self.turn_number = 0

        self.b = Board(collect_stats=collect_stats)
        self.inv_b = Board(invert=self.b, collect_stats=collect_stats)
    
    def start(self):
        if self.player == 1:
            self._opp_turn()

    def evaluator_on_off(self, active):
        """If `active` eval is on, else it's off"""
        self.eval = active

    def turn(self, lr, slot, card):
        print lr
        if lr == 1:
            print card
            print slot
        else:
            print slot
            print card

        self.turn_number += 1

        sys.stdout.flush()

        if self.eval:
            try:
                self.b.turn(lr, slot, card)
            except Exception, e: # last resort
                if self.debug:
                    print >>sys.stderr, '-'*100, e
                    #raise

        self._opp_turn()
        if self.debug:
            print >>sys.stderr, ''
            print >>sys.stderr, 'BOARD:'
            print >>sys.stderr, self.b
            print >>sys.stderr, ''
            sys.stderr.flush()

    def _opp_turn(self):
        lr = sys.stdin.readline().rstrip()
        lr = int(lr)
        if lr == 1:
            card = sys.stdin.readline().rstrip()
            slot = sys.stdin.readline().rstrip()
        elif lr == 2:
            slot = sys.stdin.readline().rstrip()
            card = sys.stdin.readline().rstrip()
         
        if self.eval:
            try:
                self.inv_b.turn(lr, int(slot), card)
            except Exception, e:
                if self.debug:
                    print >>sys.stderr, '-'*100, e
                    raise

