#!/usr/bin/env python

import sys

def OppTurn():
	sys.stdout.flush()
	lr = sys.stdin.readline().rstrip()
	if lr == '1':
		card = sys.stdin.readline().rstrip()
		slot = sys.stdin.readline().rstrip()
	elif lr == '2':
		slot = sys.stdin.readline().rstrip()
		card = sys.stdin.readline().rstrip()

if sys.argv[1] == '1':
	OppTurn()

while 1:
	print 1
	print 'I'
	print 0
	OppTurn()
