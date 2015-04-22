#!/usr/bin/env python
import time as time

def showcount(count,delay):
    print(count)
    time.sleep(delay)

print("Count to 10")
# Python stops the loop when loop = 11
for loop in range(1 ,11):
    showcount(loop,1)
if True:
    print("Finished")
else:
    print("Not Finished")

