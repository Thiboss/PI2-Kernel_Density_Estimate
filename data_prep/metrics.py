from imports import *

def calculate_returns(df):

    df_returns = df.pct_change(fill_method=None)
    df_returns = df_returns.drop(df_returns.index[0])

    return df_returns

def calculate_metrics(df, df_returns, start_date):

    start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
    df_metrics = pd.DataFrame(columns=['Stock', "Return", 'Volatility', 'Shape ratio', 'Sortino ratio'])
    
    cac40 = yf.download('^FCHI', start=start_date, progress=False)
    perf_cac40 = (cac40['Close'].iloc[-1] - cac40['Close'].iloc[0]) / cac40['Close'].iloc[0]

    for col in df_returns.columns:

        first_notnull_price = df[col].loc[df[col].first_valid_index()]
        last_notnull_price = df[col].loc[df[col].last_valid_index()]

        returns = (last_notnull_price - first_notnull_price) / first_notnull_price
        mean_return = df_returns[col].mean() * 252
        volatility = df_returns[col].std() * np.sqrt(252)
        lower_vol = df_returns[col][df_returns[col] < 0].std() * np.sqrt(252)

        sortino_ratio = (returns - perf_cac40) / lower_vol
        sharpe_ratio = (returns - perf_cac40) / volatility
        df_metrics = df_metrics._append({"Stock":col, "Return":returns, "Volatility":volatility, 'Shape ratio':sharpe_ratio, 'Sortino ratio':sortino_ratio}, ignore_index=True)

        df_metrics.to_csv(r"C:\Users\thibc\OneDrive - De Vinci\Dossiers\Développement\PI2\data\univers_metrics.csv", index=False)
     
    return df_metrics