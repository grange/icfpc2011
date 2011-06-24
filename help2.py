#!/usr/bin/env python

import sys

def Turn(lr, slot, card):
	print lr
	if lr == 1:
		print card
		print slot
	else:
		print slot
		print card
	OppTurn()

def OppTurn():
	sys.stdout.flush()
	lr = sys.stdin.readline().rstrip()
	if lr == '1':
		card = sys.stdin.readline().rstrip()
		slot = sys.stdin.readline().rstrip()
	elif lr == '2':
		slot = sys.stdin.readline().rstrip()
		card = sys.stdin.readline().rstrip()

def Attack0():
	Turn(2, 0, 'attack')
	Turn(2, 0, 'zero')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'dbl')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'dbl')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')

def Attack():
	# restore attack func
	Left(0, 'put')
	Right(0, 'zero')
	Left(0, 'succ')
	Left(0, 'succ')
	Left(0, 'succ')
	Left(0, 'get')

	# attack!
	Right(0, 'zero')

	# next slot
	Left(1, 'succ')

	# attack!
	Right(0, 'zero')

	# next slot
	Left(1, 'succ')

	# attack!
	Right(0, 'zero')

	# next slot
	Left(1, 'succ')

def Help():
	# restore help func
	Left(0, 'put')
	Right(0, 'zero')
	Left(0, 'succ')
	Left(0, 'succ')
	Left(0, 'get')

	# do help
	Right(0, 'zero')

if sys.argv[1] == '1':
	OppTurn()

def Left(slot, card):
	print 1
	print card
	print slot

def Right(slot, card):
	print 2
	print slot
	print card

def SK(slot):
	Left(slot, 'K')
	Left(slot, 'S')

def SKx(slot, x):
	Left(slot, 'K')
	Left(slot, 'S')
	Right(slot, x)

def InfLoop(slot):
	Right(slot, 'S')
	Right(slot, 'get')
	Right(slot, 'I')

def Rep(slot):
	Right(slot, 'S')
	Right(slot, 'put')
	Right(slot, 'get')

# build help value 8192
Right(0, 'zero')
Left(0, 'succ')
for i in xrange(13):
	Left(0, 'dbl')

# K-ize help value
Right(1, 'K')
SKx(1, 'get')
Right(1, 'zero')

# double help value and save to slot 4
Left(0, 'dbl')
Right(4, 'get')
Right(4, 'zero')

# build help func
Left(0, 'put')
Right(0, 'help')
Right(0, 'zero')
Right(0, 'zero')
SK(0)
SKx(0, 'get')
SKx(0, 'succ')
Right(0, 'zero')

# K-zero-ize help func
Left(1, 'put')
Right(1, 'K')
Right(1, 'zero')
SK(1)
SKx(1, 'get')
Right(1, 'zero')

# put help func under infinite loop
Left(0, 'put')
InfLoop(0)
SK(0)
SKx(0, 'get')
SKx(0, 'succ')
Right(0, 'zero')

# save help code to slot 2
Right(2, 'zero')
Left(2, 'get')

# do first help
Right(0, 'zero')

# put slot to attack to slot 1
Left(1, 'put')
Right(1, 'zero')
Left(1, 'succ')
for i in xrange (7):
	Left(1, 'dbl')
for i in xrange (127):
	Left(1, 'succ')

Attack0()
Attack0()
Help()
Attack0()
Attack0()
Attack0()

# build C combinator
Right(0, 'S')
Left(0, 'K')
Left(0, 'S')
Right(0, 'K')
Left(0, 'K')
Left(0, 'S')
Right(0, 'S')
Left(0, 'S')

Left(1, 'put')
Right(1, 'K')
Right(1, 'K')

SKx(0, 'get')
SKx(0, 'succ')
Right(0, 'zero')

# start attack func
Left(1, 'put')
Right(1, 'attack')
Right(1, 'zero')

# apply C combinator to attack func
SKx(0, 'get')
SKx(0, 'succ')
Right(0, 'zero')

# continue attack arguments
SKx(0, 'get')
SKx(0, 'dbl')
SKx(0, 'dbl')
SKx(0, 'succ')
Right(0, 'zero') # 16384
SKx(0, 'get')
SKx(0, 'succ')

# K-zero-ize attack func
Left(1, 'put')
Right(1, 'K')
Right(1, 'zero')
SK(1)
SKx(1, 'get')
Right(1, 'zero')

# put attack func under repeater
Left(0, 'put')
Rep(0)
SK(0)
SKx(0, 'get')
SKx(0, 'succ')
Right(0, 'zero')

# save attack func to slot 3
Right(3, 'get')
Right(3, 'zero')

while 1:
	# zero target number
	Left(1, 'put')
	Right(1, 'zero')

	for i in xrange(85):
		Help()
		Attack()

	Help()
	Attack()
