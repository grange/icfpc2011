#!/usr/bin/env python

def buildcommands(n,i):
    if n==1:
        return [(2,i,'zero'),(1,'succ',i)]
    elif n%2==0:
        return buildcommands(n/2,i)+[(1,'dbl',i)]
    else:
        return buildcommands(n-1,i)+[(1,'succ',i)]
        
