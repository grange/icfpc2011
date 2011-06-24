#!/usr/bin/env python

from comb import *
import target_finder

tf = target_finder.TargetFinder(g, threshold=5, debug=DEBUG)

def Attack():
	s1.zero()

def Help():
	s0.zero()
	s0.left('succ')
	s0.left('succ')
	s0.left('succ')
	s0.left('get')
	s0.zero()

# help spell
# loop K(zero) help(zero)(zero) K(8192)

# slot 1 = 8192
s1 = comb(1)
s1.num(8192)

# slot 2 = 16384
# for future use in attack
s2 = comb(2)
s2.zero()
s2.left('succ')
s2.left('get')
s2.left('dbl')

# slot 1 = K(8192)
s1.k()

# slot 0 = help(zero)(zero)
s0 = comb(0)
s0.right('help')
s0.zero()
s0.zero()

# slot 0 = help(zero)(zero) K(8192)
s0.sk()
s0.consume(1)

# slot 1 = K(zero)
s1.reset()
s1.zero()
s1.k()

# slot 1 = K(zero) help(zero)(zero) K(8192)
s1.sk()
s1.consume(0)

# slot 0 = loop
s0.reset()
s0.loop()

# slot 0 = loop K(zero) help(zero)(zero) K(8192)
s0.sk()
s0.consume(1)

# cast help
s0.zero()

# slot 0 = slot to attack
# attack the most danger slot
s0.num(255 - tf.get())

# attack spell
# slot 3 = attack(zero)(255)(16384)
s3 = comb(3)
s3.right('attack')
s3.zero()
s3.consume(0)
s3.consume(2)

# zombie spell
# slot 3 = zombie(255)(help-spell-from-slot-1)
s3.right('zombie')
s3.consume(0)
s3.consume(1)

# at this point we did a fast attack on slot 0
# now do the real things

# rebuild help spell
# slot 0 = loop
s0.reset()
s0.loop()

# slot 0 = loop K(zero) help(zero)(zero) K(8192)
s0.sk()
s0.consume(1)

# slot 3 = help spell
s3.zero()
s3.left('get')

# cast help
s0.zero()

# attack spell with C and REP for arbitrary slot

# slot 2 = K(16384)
s2.k()

# slot 0 = S attack(zero) K(16384)
s0.right('attack')
s0.right('zero')
s0.left('S')
s0.consume(2)

# slot 0 = SK S attack(zero) K(16384) get(2)
s0.skx('get')
s0.skx('dbl')
s0.skx('succ')

# slot 2 = SK K(1)
# attacker lives in slot 1
s2.reset()
s2.num(1)
s2.k()
s2.sk()

# slot 1 = SK rep
s1.reset()
s1.rep()
s1.sk()

# combine attack spell in slot 1
s2.consume(0)
s1.consume(2)

s0.reset()
while 1:
	# slot 2 = slot to attack
	s2.num(255 - tf.get())
	Attack()

	s2.num(255 - tf.get())
	Attack()

	s2.num(255 - tf.get())
	Attack()

	Help()

	if g.turn_number > 100000:
		g.evaluator_on_off(False)

