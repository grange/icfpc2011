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

def Attack():
	Turn(2, 0, 'attack')
	Turn(2, 0, 'zero')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
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
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'get')
	Turn(1, 0, 'K')
	Turn(1, 0, 'S')
	Turn(2, 0, 'succ')
	Turn(2, 0, 'zero')

def Help():
	# copy help loop to slot 0
	Turn(2, 0, 'zero')
	Turn(1, 0, 'succ')
	Turn(1, 0, 'dbl')
	Turn(1, 0, 'dbl')
	Turn(1, 0, 'get')

	# do help
	Turn(2, 0, 'zero')


def buildno(n):
	if n==0:
		return ['zero']
	elif n%2==0:
		return ['dbl']+buildno(n/2)
	else:
		return ['succ']+buildno(n-1)

def feed2to1(i,j):
	arr=['get']+buildno(j)
	for mem in arr[:-1]:
		Turn(1,i,'K')
		Turn(1,i,'S')
		Turn(2,i,mem)
	Turn(2,i,arr[-1])
   


