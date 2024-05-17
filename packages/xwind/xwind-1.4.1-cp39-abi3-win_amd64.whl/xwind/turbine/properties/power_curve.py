# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:39:40 2019

@author: hu578
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class PowerCtCurve(object):
    real_diameter: float
    air_density: float
    wind_speed_flag: List[float] = field(default_factory=list)
    power_values: List[float] = field(default_factory=list)
    cp_values: List[float] = field(default_factory=list)
    ct_values: List[float] = field(default_factory=list)
    _power_curve = None

    @property
    def power_curve(self):
        return self._power_curve

    @power_curve.setter
    def power_curve(self, value):
        if len(value) == len(self.wind_speed_flag):
            self._power_curve = value
        else:
            raise ()
