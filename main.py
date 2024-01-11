from imports import *
from data_prep.yf import get_yf
from data_prep.metrics import calculate_metrics, calculate_returns
from data_prep.clear import clear_df
from data_prep.print_df import print_df

start_date = '01/01/2015'
df = get_yf(start_date)
print_df(df)

df_returns = calculate_returns(df)
print_df(df_returns)

df_metrics = calculate_metrics(df, df_returns, start_date)
print_df(df_metrics)

df_clean = clear_df(df_returns)

returns = df_clean['LVMH'].iloc[:, 1].tolist()
print("hello")
print( returns)

