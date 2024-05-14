"""
    Copyright (C) 2024  chocolate-icecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pandas as pd
import numpy as np


def tanuki_pandas_encoder_v1(item):
    if type(item) is not pd.DataFrame:
        return
    return item.to_dict()

def tanuki_pandas_decoder_v1(item):
    return pd.DataFrame.from_dict(item)


def tanuki_numpy_int64_encoder_v1(item):
    if type(item) is not np.int64:
        return
    return int(item)

def tanuki_numpy_int64_decoder_v1(item):
    return item



encoders = {"pandas.v1": tanuki_pandas_encoder_v1,
            "numpy.int64.v1": tanuki_numpy_int64_encoder_v1}
decoders = {"pandas.v1": tanuki_pandas_decoder_v1,
            "numpy.int64..v1": tanuki_numpy_int64_decoder_v1}