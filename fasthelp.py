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

#first, put S(K(help(zero)(zero))) into 1
Right(1,'zero')
Left(1,'help')
Right(1,'zero')
Left(1,'K')
Left(1,'S')
#put 8192) into 0
Right(0,'zero')
Left(0,'succ')
for i in xrange(13):
	Left(0,'dbl')
#now store 16384 in 4 for future attack
Right(3,'dbl')
SKx(3,'get')
Right(3,'zero')
Left(0,'K')
#combine
SKx(1,'get')
Right(1,'zero')
#now build S(K(S(get)(I))) in 0
Left(0,'put')
Right(0,'get')
Left(0,'S')
Right(0,'I')
SK(0)
#build S(K(K(zero))) in 2
Right(2,'zero')
Left(2,'K')
SK(2)
#feed 2 to 0

SKx(2,'get')
SKx(2,'succ')
Right(2,'zero')
#finalize
SKx(0,'get')
SKx(0,'succ')
SKx(0,'succ')
Right(0,'zero')
#at this point 0 has recursive help function, let's store it in 4
Right(4,'get')
Right(4,'zero')
#now let's compose attackizer without explicit C-combinator
#K-ize 16384 in 3
Left(3,'K')
#initalize 0
Left(0,'put')
#make S(attack(zero)) in 0
Right(0,'zero')
Left(0,'attack')
Left(0,'S')
# feed 4 (K(16384)) to 0
SKx(0,'get')
SKx(0,'succ')
SKx(0,'dbl')
SKx(0,'succ')
Right(0,'zero')
#append get and succ on the right
SKx(0,'get')
SKx(0,'succ')
#now 0 has (S(K((K(S(attack(z))(K(16384))))(get)))(succ))
#let's build S(K(K(zero))) in 2
#initialize 
Left(2,'put')
Right(2,'zero')
Left(2,'K')
SK(2)
#build S(K(S(put)(get))) in 1
Left(1,'put')
Right(1,'S')
Right(1,'put')
Right(1,'get')
SK(1)

#feed 0 to 2
SKx(2,'get')
Right(2,'zero')
#feed 2 to 1

SKx(1,'get')
SKx(1,'succ')
SKx(1,'succ')
Right(1,'zero')
#we're done, attack is in 1, help is in 4
#test: help 0, 
Left(0,'put')
Right(0,'zero')
Left(0,'succ')
Left(0,'dbl')
Left(0,'dbl')
Left(0,'get')
Right(0,'zero')
#attack!
Right(0,'zero')
Left(0,'succ')
Left(0,'get')
Left(1,'put')
Right(1,'zero')
Left(1,'succ')
Right(0,'zero')
Left(1,succ)
Right(0,'zero')



