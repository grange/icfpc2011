#!/usr/bin/env python
import sys
import itertools

from eval import is_int, Attack

class TargetFinder(object):
    def __init__(self, game, threshold, debug=False):
        self.game = game
        self.board = game.b
        self.threshold = threshold
        self.scan_i = 0 # if evaluator failes, do attack scan
        self.debug = debug

    def _get(self):
        dead, alive = self.board.opp_tree_sizes_dead_alive()

        if len(alive) == 0 or (not self.game.eval): # eval f*kup
            self.scan_i = (self.scan_i-1) % 256
            return self.scan_i
            
        if alive[0][1] >= self.threshold:
            return alive[0][0]

        nums = [i for i,v in alive]
        return max(nums)

    def get(self):
        i = self._get()
        if self.debug:
            print >>sys.stderr, '-'*80, 'will attack', i
        return i

    # More flexible, but slow
    #rest = alive[::-1]
    #important = []
    #while len(rest):
    #    if rest[-1][1]>=threshold:
    #        important.append(rest.pop())
    #    else:
    #        break
            
    #print >>sys.stderr, 'Imp', important
    #print >>sys.stderr, 'Res', rest


class AdvancedTargetFinder(object):
    def __init__(self, game, thresholds=[100, 50, 15, 5, 0], debug=False):
        self.game = game
        self.board = game.b
        self.thresholds = thresholds
        self.debug = debug
        self.pos = 0 # last target position

    def _get_first__attack(self, alive):
        try:
            def has_attack(val):
                if is_int(val):
                    return False

                #print >>sys.stderr, val.__class__
                if val.__class__ == Attack:
                    return True
                
                for i in val.args:
                    if not is_int(i):
                        x = has_attack(i)
                        if x:
                            return x

                return False
            
            #print >>sys.stderr, self.board
            with_attack = set()
            for i, slot in enumerate(self.board.opp):
                if has_attack(slot.value):
                    with_attack.add(i)

            slots = [(i,v) for i,v in alive if i in with_attack]
            max_v = max([v for i,v in slots])
            idxs = [i for i,v in slots if v == max_v]
            return idxs[0]
        except: # well... not sure that my brain is not damaged, better be safe
            pass

        return None

    def _get_first__maxsize(self, alive):            
            self.pos = alive[0][0]
            return self.pos

    def get_zerg_rush(self):
        try:
            max_health = 13405
            dead, alive = self.board.opp_tree_sizes_dead_alive()

            targets = [(i, v) for i, v in alive if self.board.opp[i].health <= max_health]
            if len(targets) == 0: # just in impossible case
                targets = alive

            self.pos = self._get_first__attack(targets)
            if self.pos == None:
                self.pos = self._get_first__maxsize(targets)
                return self.pos
            else:
                return self.pos
        except:
            return self.get()

    def _get(self):
        dead, alive = self.board.opp_tree_sizes_dead_alive()
        
        if len(alive) == 0 or (not self.game.eval): # eval f*kup, do seq scan
            self.pos = (self.pos - 1) % 255
            return self.pos

        alive.reverse()
        groups = []
        for i, t in enumerate(self.thresholds):
            groups.append([])
            while len(alive):
                if alive[-1][1] >= t:
                    groups[i].append(alive.pop())
                else:
                    break

        for i_g, g in enumerate(groups):
            if len(g) == 0:
                continue

            # Now we need to find closest target. Proper way would be to find
            # distance between available num and every index. But Mihal is asleep.
            # So closest one would be considered with lesser or equal number
            g = [i for i,v in g]
            left = filter(lambda x: x <= self.pos, g)
            right = filter(lambda x: x > self.pos, g)
            #print >>sys.stderr, 'L/R', sorted(left), sorted(right)
            if len(left):
                self.pos = max(left)
                return self.pos
            else:
                self.pos = max(right)
                return self.pos

    def get(self):
        i = self._get()
        if self.debug:
            print >>sys.stderr, '-'*80, 'will attack', i
        return i

