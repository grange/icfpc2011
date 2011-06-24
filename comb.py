#!/usr/bin/env python
import sys
from eval import I, is_int
from game import GameState

#DEBUG = sys.argv[1] == '0'
DEBUG = False

g= GameState(sys.argv[1],debug=DEBUG,eval_=True)
g.start()

Turn=g.turn



def buildno(n,m=0):
	if n==m:
		if m==0:
			return ['zero']
		else:
			return []
	elif (n%2==0) and ((m==0) or (n/m>=2)):
		return ['dbl']+buildno(n/2,m)
	else:
		return ['succ']+buildno(n-1,m)

def log(msg, s='x'):
	if DEBUG: print >>sys.stderr, s*70, 'OP', msg

class comb(int):
	def __init__(self,i,clear=False):
		self=i
		if clear:
			Left(self,put)
	def left(self,card):
		log('left '+card, s='-')
		Turn(1,self,card)
	def right(self,card):
		log('right '+card, s='-')
		Turn(2,self,card)
	def sk(self):
		log('SK')
		self.left('K')
		self.left('S')
	def skx(self,card):
		log('SKX')
		self.sk()
		self.right(card)
	def consume(self,slotno):
		log('consume')
		arr=['get']+buildno(slotno)
		for mem in arr[:-1]:
			self.skx(mem)
		self.right(arr[-1])
	def reset(self):
		log('reset')
		self.left('put')
	def loop(self):
		log('loop')
		self.right('S')
		self.right('get')
		self.right('I')
	def rep(self):
		log('rep')
		self.right('S')
		self.right('put')
		self.right('get')
	def k(self):
		log('K')
		self.left('K')
	def _num(self,n):
		log('num s%d %d' % (self, n))
		if g.eval:
			if g.b.prop[self].value==I(g.b):
				arr=buildno(n)
				self.right(arr[-1])
				for mem in arr[:-1][::-1]:
					self.left(mem)
			elif is_int(g.b.prop[self].value):
				reflen=len(buildno(n))+1
				if (n==0) and (g.b.prop[self].value==0):
					return
				elif n<g.b.prop[self].value:
					self.left('put')
					arr=buildno(n)
					self.right(arr[-1])
					for mem in arr[:-1][::-1]:
						self.left(mem)
				elif g.b.prop[self].value==n:
					return
				else:
					reflen=len(buildno(n))+1
					newarr=buildno(n,g.b.prop[self].value)
					if g.b.prop[self].value==0:
						newarr=newarr[:-1]
					if len(newarr)>reflen:
						self.left('put')
						arr=buildno(n)
						self.right(arr[-1])
						for mem in arr[:-1][::-1]:
							self.left(mem)
					else:
						for mem in newarr[::-1]:
							self.left(mem)
			else:
				self.left('put')
				arr=buildno(n)
				self.right(arr[-1])
				for mem in arr[:-1][::-1]:
					self.left(mem)
		else:
			arr=buildno(n)
			self.right(arr[-1])
			for mem in arr[:-1][::-1]:
				self.left(mem)
 
	def num(self, n):
		self._num(n)
		log('num-end s%d %d' % (self, n))

	def zero(self):
		log('zero %d' % self)
		self.right('zero')
