"""
vector class for representing 2d arrays
"""
import math

class V():
	"""
	either pass a 2D array or x,y
	"""
	def __init__(self, *args):
		self.x = 0
		self.y = 0

		if len(args) == 1:
			self.x = args[0][0]
			self.y = args[0][1]

		if len(args) == 2:
			self.x = args[0]
			self.y = args[1]

	# to string method
	def __repr__(self):
		return "[\t" + str(self.x) + ",\t" + str(self.y) + "\t]"

	"""
	this returns what this vector plus another vector (does not modify self's vector)
	"""
	def __add__(self, other):
		return V(self.x+other.x, self.y+other.y)

	"""
	this returns what this vector minus another vector (does not modify self's vector)
	"""
	def __sub__(self, other):
		return V(self.x-other.x, self.y-other.y)

	"""
	returns the result of scalar multiplication with this vector
	"""
	def __mul__(self, scalar):
		return V(self.x*scalar, self.y*scalar)

	""" 
	size of this vector
	"""
	def mag(self):
		return math.sqrt(self.x**2 + self.y**2)

	"""
	gets a perpendicular to the segment
	"""
	def getPerp(self):
		vv =  V(-self.y, self.x)
		vv.toUnit()
		return vv

	"""
	scales by 1/magnitude(self)
	no return value
	"""
	def toUnit(self):
		m = self.mag()
		self.x=self.x/m
		self.y=self.y/m
