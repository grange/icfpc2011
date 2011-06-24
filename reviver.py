#!/usr/bin/env python

from comb import *
import target_finder

#tf = target_finder.TargetFinder(g, threshold=5, debug=DEBUG)
tf = target_finder.AdvancedTargetFinder(g, thresholds=[40, 20, 10, 4, 0], debug=DEBUG)

def Attack():
	s1.zero()

def Zombie():
	s4.zero()

def Help():
	while g.b.prop[0].health < 8192:
		Heal(0)
		Guard([0,1,2,3])

	s0.zero()
	s0.left('succ')
	s0.left('succ')
	s0.left('succ')
	s0.left('get')
	s0.zero()

def Revive(slot):
	for i in xrange(5, 256):
		if g.b.prop[i].health > 0:
			break;
	if g.b.prop[i].health > 0:
		s = comb(i)
		s.num(slot)
		s.left('revive')

def Guard(slots):
	for s in slots:
		if g.b.prop[s].health == 0:
			Revive(s)

def Heal(slot):
	for i in xrange(5, 256):
		if g.b.prop[i].health > 0:
			break;
	if g.b.prop[i].health > 0:
		s = comb(i)
		s.num(slot)
		s.left('inc')

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
s0.num(255 - tf.get_zerg_rush())

Guard([0, 1, 2, 3])

# attack spell
# slot 3 = attack(zero)(255)(16384)
s3 = comb(3)
s3.right('attack')
s3.zero()
s3.consume(0)
s3.consume(2)

Guard([0, 1, 2, 3])

# zombie spell
# slot 3 = zombie(255)(help-spell-from-slot-1)
s3.right('zombie')
s3.consume(0)
s3.consume(1)

Guard([0, 1, 2, 3])

# at this point we did a fast attack on slot 0
# now do the real things

# rebuild help spell
# slot 0 = loop
s0.reset()
s0.loop()

Guard([0, 1, 2, 3])

# slot 0 = loop K(zero) help(zero)(zero) K(8192)
s0.sk()
s0.consume(1)

Guard([0, 1, 2, 3])

# slot 3 = help spell
s3.zero()
s3.left('get')

Guard([0, 1, 2, 3])

# cast help
s0.zero()

Guard([0, 1, 2, 3])

# attack spell with C and REP for arbitrary slot

# slot 2 = K(16384)
s2.k()

Guard([0, 1, 2, 3])
if g.b.prop[0].health < 49152:
	Help()

# slot 0 = S attack(zero) K(16384)
s0.right('attack')
s0.right('zero')
s0.left('S')
s0.consume(2)

Guard([0, 1, 2, 3])

# slot 0 = SK S attack(zero) K(16384) get(2)
s0.skx('get')
s0.skx('dbl')
s0.skx('succ')

Guard([0, 1, 2, 3])

# slot 2 = SK K(1)
# attacker lives in slot 1
s2.reset()
s2.num(1)
s2.k()
s2.sk()

Guard([0, 1, 2, 3])

# slot 1 = SK rep
s1.reset()
s1.rep()
s1.sk()

Guard([0, 1, 2, 3])

# combine attack spell in slot 1
s2.consume(0)
s1.consume(2)

Guard([0, 1, 2, 3])
if g.b.prop[0].health < 49152:
	Help()

# zombie spell with C and REP for arbitrary slot

# slot 2 = K(I)
s2.reset()
s2.k()

Guard([0, 1, 2, 3])

# slot 0 = S zombie K(I)
s0.reset()
s0.right('zombie')
s0.left('S')
s0.consume(2)

Guard([0, 1, 2, 3])

# slot 0 = SK S zombie K(I) get(2)
s0.skx('get')
s0.skx('dbl')
s0.skx('succ')

Guard([0, 1, 2, 3])

# slot 2 = SK K(4)
# zombifier lives in slot 4
s2.reset()
s2.num(4)
s2.k()
s2.sk()

Guard([0, 1, 2, 3])

# slot 4 = SK rep
s4 = comb(4)
s4.rep()
s4.sk()

Guard([0, 1, 2, 3])

# combine zombie spell in slot 4
s2.consume(0)
s4.consume(2)

s0.reset()
while 1:
	Guard([0, 1, 2, 3])
	if g.b.prop[0].health < 49152:
		Help()

	# get slot to attack
	t = tf.get()
	s2.num(255 - t)
	Attack()

	# zombify if it's dead and had anything
	if g.b.opp[t].health == 0 and g.b.opp[t].value != I(g.b):
		Zombie()

	if g.b.prop[1].value == I(g.b) or g.b.prop[3] == I(g.b):
		# we're mostly dead
		break

	if g.turn_number > 80000:
		# evaluator gone mad
		g.evaluator_on_off(False)
		break

while 1:
	for i in xrange(0, 256):
		Revive(i)
