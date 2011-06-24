#!/usr/bin/env python
from meta import *
if sys.argv[1] == '1':
	OppTurn()

Turn(2,0,'S')
Turn(1,0,'K')
Turn(1,0,'S')
#S(KS)
Turn(2,0,'K')

Turn(1,0,'K')


Turn(1,0,'S')
Turn(2,0,'S')
Turn(1,0,'S')

Turn(2,1,'K')
Turn(2,1,'K')

feed2to1(0,1)

Turn(1,1,'put')

Turn(2,1,'attack')
Turn(2,1,'zero')

feed2to1(0,1)
Turn(1,1,'put')
Turn(2,1,'zero')
Turn(1,1,'succ')
Turn(1,1,'dbl')
feed2to1(0,1)

Turn(2,0,'zero')
Turn(1,1,'put')