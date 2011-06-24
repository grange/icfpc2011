#!/usr/bin/env python

import unittest

import target_finder
import game
from eval import *

c = lambda: OpCounter()

class TestCardOps(unittest.TestCase):
    def test_primitive(self):
        b = Board()

        self.assertEqual(Zero(b)(ctr=c()), 0)
        with self.assertRaises(ProgError):
            Zero(b)(1, ctr=c())
        
        self.assertEqual(Succ(b)(Zero(b), ctr=c()), 1)
        self.assertEqual(Succ(b)(65535, ctr=c()), 65535)

        self.assertEqual(Dbl(b)(3, ctr=c()), 6)
        self.assertEqual(Dbl(b)(50000, ctr=c()), 65535)

    def test_get_and_op_counters(self):
        b = Board()
        b.prop[2].value = 567
        b.apply_right(4, Zero)
        b.apply_left(4, Succ)
        b.apply_left(4, Succ)
        b.apply_left(4, Get)
        self.assertEqual(b.prop[4].value, 567)

        mru = b.prop_mru('get')
        self.assertEqual(mru[0], (2, 0.25))
        self.assertEqual(mru[1][1], 0.0)

        mru = b.prop_mru('call')
        self.assertEqual(mru[0], (4, 5.0/4)) # I(Zero()) gives 2 calls
        self.assertEqual(mru[1][1], 0.0)

        mru = b.prop_mru('add')
        self.assertEqual(mru[0], (4, 1.0))
        self.assertEqual(mru[1][1], 0.0)

        b.apply_right(7, Zero)
        b.prop[7].health = 0
        dead, alive = b.prop_mru_dead_alive('call')
        self.assertEqual(dead[0], (7, 2.0/5))
        self.assertEqual(len(dead), 1)
        self.assertEqual(alive[0], (4, 5.0/5))
        self.assertEqual(alive[1][1], 0)
        self.assertEqual(len(alive), 255)

    def test_put(self):
        b = Board()
        b.prop[4].value = 555
        b.apply_left(4, Put)
        self.assertEqual(b.prop[4].value, I(b))
        
        mru = b.prop_mru('put')
        self.assertEqual(mru[0][0], 4)
        self.assertEqual(mru[0][1], 1.0)
        self.assertEqual(mru[1][1], 0.0)

    def test_s(self):
        b = Board()
        b.prop[0].value = Dbl(b)
        self.assertEqual(S(b)(Get(b), Succ(b), Zero(b), ctr=c()), 2)

    def test_k(self):
        b = Board()
        self.assertEqual(K(b)(100, 44, ctr=c()), 100)

    def test_inc(self):
        b = Board()
        b.apply_right(0, Zero)
        b.apply_left(0, Succ)
        b.apply_left(0, Succ)
        b.apply_left(0, Inc)
        self.assertEqual(b.prop[2].health, 10000+1)
        self.assertEqual(b.prop[0].value, I(b))

    def test_dec(self):
        b = Board()
        b.apply_right(0, Zero)
        b.apply_left(0, Succ)
        b.apply_left(0, Succ)
        b.apply_left(0, Dec)
        self.assertEqual(b.opp[255-2].health, 10000-1)
        self.assertEqual(b.prop[0].value, I(b))

    def test_attack(self):
        b = Board()
        # Too long to prepare properly
        self.assertEqual(Attack(b)(0, 2, 20, ctr=c()), I(b))
        self.assertEqual(b.prop[0].health, 10000-20)
        self.assertEqual(b.opp[255-2].health, 10000-20*9/10)

    def test_help(self):
        b = Board()
        # Too long to prepare properly
        self.assertEqual(Help(b)(0, 2, 20, ctr=c()), I(b))
        self.assertEqual(b.prop[0].health, 10000-20)
        self.assertEqual(b.prop[2].health, 10000+20*11/10)

    def test_copy(self):
        b = Board()
        k = K(b)
        b.opp[10].value = Attack(b)(k, ctr=c())
        b.prop[1].value = 255-10
        b.apply_left(1, Copy)
        self.assertEqual(b.prop[1].value, Attack(b)(K(b), ctr=c()))

        b.apply_right(1, Zero)
        self.assertNotEqual(b.prop[1].value, Attack(b)(K(b), ctr=c()))
        self.assertEqual(b.prop[1].value, Attack(b)(K(b), Zero(b), ctr=c()))
        self.assertEqual(b.opp[10].value, Attack(b)(K(b), ctr=c()))
        
        k(I(b), ctr=c()) # not sure if it really can happen, but still...
        self.assertNotEqual(b.prop[1].value, Attack(b)(K(b), ctr=c()))
        self.assertEqual(b.prop[1].value, Attack(b)(K(b), Zero(b), ctr=c()))

    def test_revive(self):
        b = Board()
        b.prop[3].health = 0
        b.prop[55].value = 3
        b.apply_left(55, Revive)
        self.assertEqual(b.prop[3].health, 1)
        self.assertEqual(b.prop[55].value, I(b))

        b.prop[3].health = 10
        b.prop[55].value = 3
        b.apply_left(55, Revive)
        self.assertEqual(b.prop[3].health, 10)
        self.assertEqual(b.prop[55].value, I(b))

    def test_zombie(self):
        b = Board()
        reset_global_op_counter()

        b.opp[253].health = 0
        b.opp[253].value = 100

        b.apply_right(5, Zero)
        b.apply_left(5, Succ)
        b.apply_left(5, Succ)
        b.apply_left(5, Zombie)
        b.apply_right(5, Zero) # will try to call 0(I)

        b.zombie_scan()
        self.assertEqual(b.opp[253].health, 0)
        self.assertEqual(b.opp[253].value, I(b))

    def test_zombie_inc(self):
        b = Board()
        reset_global_op_counter()

        b.opp[253].health = 0
        b.opp[253].value = 100
        Zombie(b)(2, S(b)(Inc(b), 0)) # FIXME: need to have 0 for inc

        #print 'Zombiescan'
        b.zombie_scan()
        self.assertEqual(b.opp[253].health, 0)
        self.assertEqual(b.opp[253].value, I(b))
        #self.assertEqual(b.opp[5].health, 10000-1)
        
        #b.opp[250].health = 0
        #Zombie(b)(5, Zero(b)) # will throw err internally
        #b.zombie_scan()
        #self.assertEqual(b.opp[250].health, 0)

        #self.assertEqual(b.opp[0].health, 10000-1)

    def test_slot_op_counter_micro(self):
        sc = SlotOpCounter(5)
        sc.end_turn()
        for turn in range(1, 10):
            for slot in range(2):
                for i in range(slot+1):
                    sc.inc(slot)
            sc.end_turn()
            mru = sc.mru()

            #print mru[0:3]
            # TODO: using == for floats, may fail randomly
            self.assertEqual(mru[0][0], 1)
            self.assertEqual(mru[1][0], 0)
            self.assertEqual(mru[2][1], 0.0)
            if turn >= 5:
                base = 1.
            else:
                base = float(turn) / (turn+1)

            self.assertEqual(mru[0][1], base*2)
            self.assertEqual(mru[1][1], base)

    def test_tree_size_micro(self):
        b = Board()

        tree = S(b)(K(b), Put(b))
        self.assertEqual(tree.tree_size(), 3)

        tree = S(b)(K(b), S(b)(K(b)(Put(b))))
        self.assertEqual(tree.tree_size(), 5)

        tree = S(b)(S(b)(K(b), Attack(b)), S(b)(K(b)(Put(b))))
        self.assertEqual(tree.tree_size(), 7)

    def test_tree_size(self):
        b = Board()

        b.opp[1].value = S(b)(K(b), Put(b))
        b.opp[3].value = S(b)(K(b), S(b)(K(b)(Put(b))))
        b.opp[6].value = S(b)(S(b)(K(b), Attack(b)), S(b)(K(b)(Put(b))))

        sizes = b.opp_tree_sizes()
        self.assertEqual(sizes[0], (6, 7))
        self.assertEqual(sizes[1], (3, 5))
        self.assertEqual(sizes[2], (1, 3))

        b.opp[3].health = 0
        dead, alive = b.opp_tree_sizes_dead_alive()
        self.assertEqual(dead[0], (3,5))
        self.assertEqual(alive[0], (6, 7))
        self.assertEqual(alive[1], (1, 3))
    
    def test_target_finder(self):
        g = game.GameState('1')
        b = g.b
        b.opp[1].value = S(b)(K(b), S(b)(K(b)(Put(b))))
        b.opp[2].health = 0
        b.opp[4].value = S(b)(K(b), Put(b))
        b.opp[6].value = S(b)(S(b)(K(b), Attack(b)), S(b)(K(b)(Put(b))))
        b.opp[10].health = -1
        b.opp[50].health = 0
        b.opp[90].health = 0
        b.opp[254].health = 0
        
        tf = target_finder.TargetFinder(g, threshold=5)
        i = tf.get()
        self.assertEqual(i, 6)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 1)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 255)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 253)
        b.opp[i].health = -1

        for i in range(256):
            b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 255)

        i = tf.get()
        self.assertEqual(i, 254)

    def test_advanced_target_finder(self):
        reset_global_op_counter()

        g = game.GameState('1')
        b = g.b
        b.opp[0].value = S(b)(K(b), S(b)(K(b))) # 4
        b.opp[1].value = S(b)(K(b), S(b)(K(b)(Put(b)))) # 5
        b.opp[2].health = 0
        b.opp[3].value = S(b)(K(b)) # 2
        b.opp[4].value = S(b)(K(b), Put(b)) # 3
        b.opp[6].value = S(b)(S(b)(K(b), Attack(b)), S(b)(K(b)(Put(b)))) # 7
        b.opp[8].value = S(b)(S(b)(K(b), Attack(b)(Zero(b))), S(b)(K(b)(Put(b)))) #8
        b.opp[9].health = -1
        b.opp[11].value = S(b)(S(b)(K(b), Attack(b)(Zero(b))), S(b)(K(b)(Put(b)))) #8
        b.opp[15].health = -1
        b.opp[50].health = 0
        b.opp[53].value = S(b)(K(b), S(b)(K(b)(Put(b)))) # 5
        b.opp[90].health = 0
        b.opp[254].health = 0
        
        tf = target_finder.AdvancedTargetFinder(g, thresholds=[15, 10, 7, 3, 0])

        print tf.get_zerg_rush()

        i = tf.get()
        self.assertEqual(i, 11)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 8)
        b.opp[i].health = 1 # couldn't kill or ressurected
            
        i = tf.get()
        self.assertEqual(i, 8)
        b.opp[i].health = -1
            
        b.opp[11].health = 100 # ressurected 11 but pos continue to dec

        i = tf.get()
        self.assertEqual(i, 6)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 11)
        b.opp[i].health = -1

        # bosses killed, next level, pos=6
        i = tf.get()
        self.assertEqual(i, 4)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 1)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 0)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 53)
        b.opp[i].health = -1


        b.opp[11].health = 100 # ressurected 11 but pos continue to dec

        i = tf.get()
        self.assertEqual(i, 11)
        b.opp[i].health = -1

        # next level, 0 to 3 -- everything other
        i = tf.get()
        self.assertEqual(i, 10)
        b.opp[i].health = -1
        
        i = tf.get()
        self.assertEqual(i, 7)
        b.opp[i].health = -1

        # now will try to emulate Eval fail
        for i in range(256):
            b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 6)
        b.opp[i].health = -1

        i = tf.get()
        self.assertEqual(i, 5)
        b.opp[i].health = -1


if __name__ == '__main__':
    unittest.main()

