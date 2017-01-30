
import random
import math
import time

import entity
import connector

lineThresh = 25
terminalVel = 4
entityPull = .005
frictionThresh = 1.2
frictionCorrection = .00001
frictionDelay = .9995

entities = [0,1,2,3,4,5,6,7]

xBoundMin = -35
xBoundMax = 35
yBoundMin = -20
yBoundMax = 20
frameRate = 30.

friction = 1
frictionActive = False
frictionRecover = False

livingEnts = []
connectors = []
lastFrame = time.clock()

# To be list of middleware functions
interactions = []

def frictionBalance(sysEnergy):
	global friction
	global frictionActive
	global frictionRecover
	sysCap = frictionThresh * len(livingEnts)

	if not frictionActive and sysEnergy > sysCap:
		frictionActive = True
	elif frictionActive and friction > frictionDelay:
		friction = friction - frictionCorrection
	elif frictionActive and friction < frictionDelay:
		frictionRecover = True
		frictionActive = False
	elif frictionRecover and friction < 1.:
		friction = friction + frictionCorrection
	elif frictionRecover:
		frictionRecover = False
		friction = 1

def initialize():
	global livingEnts
	global connectors
	livingEnts = []
	for i in entities:
		xPos = (random.random()-.5)*xBoundMax
		yPos = (random.random()-.5)*yBoundMax
		xVel = (random.random()-.5)
		yVel = (random.random()-.5)
		livingEnts.append(entity.entity(xPos, yPos, xVel, yVel, i))
	connectors = []
	for i in entities:
		index = i + 1
		while index < len(entities):
			connectors.append(connector.connector(livingEnts[i], livingEnts[index], str(i)+str(index)))
			index += 1

def update():
	sysEnergyNow = 0
	for i in livingEnts:
		sysEnergyNow = sysEnergyNow + i.updatePos(terminalVel, friction)
		i.testBounds(xBoundMin, xBoundMax, yBoundMin, yBoundMax)
	for n in connectors:
		n.calcLength(lineThresh, entityPull)
	frictionBalance(sysEnergyNow)

def nextFrame():
	global lastFrame
	now = time.clock()
	downTime = 1./frameRate - (now - lastFrame)
	time.sleep(downTime)
	lastFrame = time.clock()
	print(lastFrame)

initialize()

while True:
	update()
	nextFrame()
