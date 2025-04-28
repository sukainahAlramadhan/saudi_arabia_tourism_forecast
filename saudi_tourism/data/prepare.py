# data/prepare.py ➤ Handles data cleaning: convert dates, drop NaNs, rename columns.
# data/prepare.py ➤ Handles data cleaning: convert dates, drop NaNs, rename columns.
# data/prepare.py ➤ Handles data cleaning: convert dates, drop NaNs, rename columns.
import pandas as pd

#from google.cloud import bigquery

from pathlib import Path


def prepare_data_demostic():
    """
    Clean raw data by
    - assigning correct dtypes to each column
    - removing buggy or irrelevant transactions
    """
    ## read data file
    df_d = pd.read_excel('raw_data/D_data.xlsx')

    ## crete date column and set it as index then drop the (yeaer month) columns
    df_d['Date'] = pd.to_datetime(df_d['Year'].astype(str) + ' ' + df_d['Month'])
    df_d.set_index('Date', inplace=True)
    df_d.drop(columns=['Year', 'Month'], inplace=True)
    df_d = df_d.dropna()

    ## rename the column
    df_d.rename(columns={'Tourists Number Overnight Visitors': 'number of visitor'}, inplace=True)
    print("✅ data prepared")

    return df_d
def prepare_data_inbound():
    # inbound data
    ## read data file
    df_i = pd.read_excel('raw_data/I_data.xlsx')

    ## crete date column and set it as index then drop the (yeaer month) columns
    df_i['Date'] = pd.to_datetime(df_i['Year'].astype(str) + ' ' + df_i['Month'])

    df_i.set_index('Date', inplace=True)
    df_i.drop(columns=['Year', 'Month'], inplace=True)
    df_i = df_i.dropna()

    ## rename the column
    df_i.rename(columns={'Tourists Number Overnight Visitors': 'number of visitor'}, inplace=True)
    # df_i.head()
    print("✅ data prepared")

    return df_i
