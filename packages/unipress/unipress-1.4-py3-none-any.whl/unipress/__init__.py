#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################### 
#   Copyright 2024 Konrad Sakowski
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
####################################################################################
#
"""
	This is a python library developed by Institute of High Pressure Physics of Polish Academy of Sciences.
"""

import numpy
import pint
import scipy
import scipy.constants

un = pint.UnitRegistry(system='mks');
un.define('fraction = [] = frac')
un.define('percent = 0.01 frac = pct')

class Physics(object):
	"""
		Class for general physical formulas and quantities.

		Parameters::

		* *un* --- units, an instance of :class:`pint.UnitRegistry`

	"""
	def __init__(self, un = un):
		self.un = un;

		self.q = self.scipy_physconst("elementary charge");
		self.c = self.scipy_physconst("speed of light in vacuum");
		self.hbar = self.scipy_physconst("Planck constant over 2 pi");

	def E2lambda(self, E):
		"""
			It converts energy to corresponding wavelength (in nm).
		"""
		return (2*numpy.pi*self.hbar*self.c / E).to(self.un.nm);
	
	def lambda2E(self, lambdaa):
		"""
			It converts wavelength to corresponding energy (in eV).
		"""
		return (2*numpy.pi*self.hbar*self.c / lambdaa).to(self.un.eV);
	
	def scipy_physconst(self, name):
		"""
			Function for loading of physical constants from *scipy* library with units of *pint* library.
		"""
		value, unit, uncertainty = scipy.constants.physical_constants[name];
		return self.un.Quantity(value, unit);

