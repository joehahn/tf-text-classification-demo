#helper_fns.py
#
#by Joe Hahn
#jmh.datasciences@gmail.com
#23 January 2019
#
#helper functions used by x.py and various notebooks

#imports used below
import pandas as pd

#read NYSE data into pandas dataframe
def read_nyse_data(data_path, start_date=None, end_date=None, drop_holidays=None):
    import glob
    files = glob.glob(data_path + '/*.txt')
    dataframes = []
    for file in files:
        df = pd.read_csv(file, parse_dates=['<date>'])
        dataframes.append(df)
    df = pd.concat(dataframes, ignore_index=True)
    df.columns = [col.replace('<', '').replace('>', '') for col in df.columns]
    df = df.sort_values(['date', 'ticker'])
    debug = False
    if (debug):
        print df.dtypes
        print 'number of records (M) = ', len(df)/1.0e6
        df.head()
    if (start_date):
        idx = (df['date'] >= start_date)
        df = df[idx]
    if (end_date):
        idx = (df['date'] <= end_date)
        df = df[idx]
    if (drop_holidays):
        daily_volume = df.groupby('date')['vol'].sum()
        idx = (daily_volume > 0)
        dates = daily_volume[idx].index
        idx = df['date'].isin(dates)
        df = df[idx]
    return df


