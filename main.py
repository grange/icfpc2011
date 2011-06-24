#!/usr/bin/python
class value(str):
    pass
class Slot():
    def __init__(self):
        self.health=10000
        self.value='I'
        
class Set(list):
    def __init__(self):
        for i in xrange(500):
            self.append(Slot())
Our=Set()
Opp=Set()
import sys
OurPlayer=sys.argv[1]
while 1:
    instr=sys.stdin.readline()
    instr=sys.stdin.readline()
    instr=sys.stdin.readline()
    sys.stdout.write('1\n')
    sys.stdout.write('I\n')
    sys.stdout.write('0\n')
