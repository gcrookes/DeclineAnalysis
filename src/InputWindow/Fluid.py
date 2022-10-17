class Fluid:

	def __init__(self, fluid_type, title, conversions):
		self.title = title
		self.fluid_type = fluid_type
		self.unit_conversions = conversions

	def fluid(self):
		return self.fluid_type

	def fluid_title(self):
		return self.title

	def conversion(self, unit):
		try:
			return self.unit_conversions[unit]
		except:
			raise ValueError("That is not a valid unit for this fluid")

	def unit_list(self):
		return self.unit_conversions.keys()
