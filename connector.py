
import math

class connector:
	def __init__(self, a, b, cID):
		self.id = str(cID)
		self.a = a
		self.b = b

	def calcLength(self, lineThresh, entityPull):
		x = self.a.xPos - self.b.xPos
		y = self.a.yPos - self.b.yPos
		x2 = math.pow(x, 2)
		y2 = math.pow(y, 2)
		self.length = math.sqrt(x2 + y2)
		if self.length < lineThresh:
			pull = (lineThresh - self.length)/lineThresh

			# TODO - abstract to interaction middleware
			self.a.updateVel(-x * entityPull * pull, -y * entityPull * pull)
			self.b.updateVel(x * entityPull * pull, y * entityPull * pull)
