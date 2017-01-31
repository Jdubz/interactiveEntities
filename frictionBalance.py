frictionThresh = 1.2
frictionCorrection = .00001
frictionDelay = .9995

def balance(sysEnergy, sysSize, friction, frictionActive, frictionRecover):
	sysCap = frictionThresh * sysSize

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
	return {'friction': friction, 'active': frictionActive, 'recover': frictionRecover}
