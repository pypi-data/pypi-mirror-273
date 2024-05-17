from scipy.stats import linregress
import numpy as np
from numpy.typing import ArrayLike
import pandas as pd


def least_square_interp(x: ArrayLike, y: ArrayLike, fill_x: ArrayLike):
    r = linregress(x, y)
    return r.slope * fill_x + r.intercept


# get slope intercept and r-value of linear regression
def linregress_slope_intercept_r(x: ArrayLike, y: ArrayLike):
    r = linregress(x, y)
    return r.slope, r.intercept, r.rvalue


# winddata groupby sector
def get_sector_slope_intercept_r(winddata: pd.DataFrame, sector: str):
    x = winddata.loc[winddata["Sector"] == sector, "Windspeed"].values
    y = winddata.loc[winddata["Sector"] == sector, "Windspeed_pred"].values
    return linregress_slope_intercept_r(x, y)
