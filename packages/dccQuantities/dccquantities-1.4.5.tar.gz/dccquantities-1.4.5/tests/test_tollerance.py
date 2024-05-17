# This file is part of dccQuantities (https://gitlab1.ptb.de/digitaldynamicmeasurement/dccQuantities)
# Copyright 2024 [Benedikt Seeger(PTB), Vanessa Stehr(PTB), Thomas Bruns(PTB)]
# (PTB) Physikalisch Technsiche Bundesanstalt, Bundesallee 100, 38116 Braunschweig, Germany
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import numpy as np
from dccQuantitiesConfiguration import ToleranceSettings
from dccQuantities import dccQuantity
def test_default_tolerances():
    assert ToleranceSettings.atol == np.finfo(float).eps
    assert ToleranceSettings.rtol == 1e-14

def test_dsiVector_equality():
    v1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    v2 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    assert v1 == v2

def test_dsiVector_inequality():
    v1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    v2 = dccQuantity((np.arange(20) + 1) * 5.0005, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    assert v1 != v2

def test_dsiVector_equality_with_tolerance():
    v1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    v2 = dccQuantity(((np.arange(20) + 1) * 5) + 10e-8, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    assert v1 != v2

def test_dsiVector_equality_with_changedTolerance():
    ToleranceSettings.set_tolerances(new_atol=1e-10)
    v1 = dccQuantity((np.arange(20) + 1) * 5, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    v2 = dccQuantity(((np.arange(20) + 1) * 5) + 10e-11, np.ones(20) * 0.1, 'Magnitude', r'\volt', uncerType="relPercent")
    assert v1 == v2