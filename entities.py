
import random
import math
import time
import threading
import logging
import json
import socket

logging.basicConfig(level=logging.DEBUG)

import entity
import connector
import frictionBalance

lineThresh = 25
terminalVel = 4
entityPull = .005

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

UDP_IP = '127.0.0.1'
UDP_PORT = 18000

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
  logging.debug('system initialized')

def update(ws):
  global friction
  global frictionActive
  global frictionRecover
  sysEnergyNow = 0
  system = {'entities': {}, 'connectors': {}}

  for i in livingEnts:
    sysEnergyNow = sysEnergyNow + i.updatePos(terminalVel, friction)
    i.testBounds(xBoundMin, xBoundMax, yBoundMin, yBoundMax)
    entNow = i.package()
    system['entities'][entNow['id']] = entNow

  for n in connectors:
    n.calcLength(lineThresh, entityPull)
    conNow = n.package()
    system['connectors'][conNow['id']] = conNow

  newFriction = frictionBalance.balance(sysEnergyNow, len(livingEnts), friction, frictionActive, frictionRecover)
  friction = newFriction['friction']
  frictionActive = newFriction['active']
  frictionRecover = newFriction['recover']
  ws.sendto(json.dumps(system).encode(), (UDP_IP, UDP_PORT))

def nextFrame():
  global lastFrame
  now = time.clock()
  downTime = 1./frameRate - (now - lastFrame)
  time.sleep(downTime)
  lastFrame = time.clock()

def runSystem():
  ws = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    update(ws)
    nextFrame()

initialize()

sys = threading.Thread(target=runSystem)
sys.setDaemon(True)
sys.start()

while True:
  time.sleep(3)
  logging.debug('running')
