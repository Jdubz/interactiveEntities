
import math

class entity:
	def __init__(self, xPos, yPos, xVel, yVel, eID):
		self.id = str(eID)
		self.xPos = xPos
		self.yPos = yPos
		self.xVel = xVel
		self.yVel = yVel
		self.size = 1
		self.color = {'r': 1, 'g': 1, 'b': 1}

	def updatePos(self, terminalVel, friction):
		Vel = math.sqrt(math.pow(self.xVel, 2) + math.pow(self.yVel, 2))
		if Vel > terminalVel:
			self.xVel = self.xVel * (terminalVel/Vel)
			self.yVel = self.yVel * (terminalVel/Vel)

		self.xPos = self.xPos + self.xVel
		self.yPos = self.yPos + self.yVel

		self.xVel = self.xVel * friction
		self.yVel = self.yVel * friction
		return Vel

	def updateVel(self, dx, dy):
		self.xVel = self.xVel + dx
		self.yVel = self.yVel + dy

	def testBounds(self, xBoundMin, xBoundMax, yBoundMin, yBoundMax):
		if self.xPos > (xBoundMax - self.size/2) and self.xVel > 0:
			self.xVel = -self.xVel
		elif self.xPos < (xBoundMin + self.size/2) and self.xVel < 0:
			self.xVel = -self.xVel

		if self.yPos > (yBoundMax - self.size/2) and self.yVel > 0:
			self.yVel = -self.yVel
		elif self.yPos < (yBoundMin + self.size/2) and self.yVel < 0:
			self.yVel = -self.yVel

	def package(self):
		pkg = {'id': self.id}
		pkg['x'] = self.xPos
		pkg['y'] = self.yPos
		pkg['size'] = self.size
		pkg['color'] = self.color
		return pkg
