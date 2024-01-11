from imports import *


def get_yf(start_date):

    csv_path = r"C:\Users\thibc\OneDrive - De Vinci\Dossiers\Développement\PI2\data\univers_actions.xlsx"
    df = pd.read_excel(csv_path)

    df_yf = pd.DataFrame()
    start_date = datetime.strptime(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')

    for index, row in df.iterrows():
        ticker = row['Stock Ticker'] 
        stock_name = row['Stock Name']  
        
        data = yf.download(ticker, start=start_date, progress=False)
        df_yf[stock_name] = data['Close']

    df_yf.to_csv(r"C:\Users\thibc\OneDrive - De Vinci\Dossiers\Développement\PI2\data\univers_yf.csv", index=False)

    return df_yf