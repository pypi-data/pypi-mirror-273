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

class ToleranceSettings:
    atol = np.finfo(float).eps  # Machine epsilon for float64
    rtol = 1e-14  # Default relative tolerance

    @staticmethod
    def set_tolerances(new_atol=None, new_rtol=None):
        if new_atol is not None:
            ToleranceSettings.atol = new_atol
        if new_rtol is not None:
            ToleranceSettings.rtol = new_rtol

class XMLConversionSettings:
    dccRestServer: str = "https://s18361.bs.ptb.de/dcc_rest_server/",
    proxies: dict = {"http": "", "https": "", "ftp": ""},

    @staticmethod
    def set_dccRestServer(newdccRestServer):
        XMLConversionSettings.dccRestServer = newdccRestServer

    @staticmethod
    def set_hhtpProxy(httpProxy):
        XMLConversionSettings.proxies["http"] = httpProxy

    @staticmethod
    def set_hhtpsProxy(httpsProxy):
        XMLConversionSettings.proxies["https"] = httpsProxy

    @staticmethod
    def set_ftpProxy(ftpProxy):
        XMLConversionSettings.proxies["ftp"] = ftpProxy
