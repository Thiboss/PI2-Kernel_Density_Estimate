from imports import *

def clear_df(df_returns):

    na_counts = df_returns.isna().sum()
    print("\nProportion de valeurs manquantes dans chaque colonne (en %) :\n")
    print(na_counts*100/len(df_returns))

    df_clean = pd.DataFrame()

    for col in df_returns:

        col_mean = df_returns[col][df_returns[col].isna() == False].mean()
        df_clean[col] = df_returns[col].fillna(col_mean)
 
    print('\nDataset nettoyé !\n')

    return df_clean