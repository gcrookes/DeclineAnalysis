from InputWindow.Fluid import Fluid

class FluidList:

	def __init__(self):

		# Converts everything into m3/day
		liquid_conversions = {'m3/day': 1, 'E3m3/day': 1000, 'bbl/day': 0.158987, 'Mbbl/day': 158.987}
		gas_conversions = {'E3m3/day': 1, 'm3/day': 1/1000, 'Mscf/day': 35.3147, 'MMscf/day': 35314.7}  # Converts everything into 1000m3/day

		self.fluids = [
			Fluid('oil', 'Cal. Oil Rate', liquid_conversions),
			Fluid('water', 'Cal. Condensate Rate', liquid_conversions),
			Fluid('cond', 'Cal. Water Rate', liquid_conversions),
			Fluid('daily', 'Cal. Daily Fluid', liquid_conversions),
			Fluid('gas', 'Cal. Gas Rate', gas_conversions)]

	def label_list(self):
		return [fluid.fluid_title() for fluid in self.fluids]

	def type_of(self, fluid_title):
		for fluid in self.fluids:
			if fluid.fluid_title() == fluid_title:
				return fluid.fluid()

	def units_of(self, fluid_title):
		for fluid in self.fluids:
			if fluid.fluid_title() == fluid_title:
				return fluid.unit_list()

	def conversion(self, fluid_title, unit):
		for fluid in self.fluids:
			if fluid.fluid_title() == fluid_title:
				return fluid.conversion(unit)