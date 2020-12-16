import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

##style.use('ggplot')

start_date = dt.datetime(2019,1,1)
end_date = dt.datetime(2020,1,1)

df = web.DataReader('TSLA', 'yahoo', start_date, end_date)
print(df.tail(6))
