#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import datetime as datetime
import getpass
import copy
import sys
import os
import pyodbc
from vnstock import *
from scipy.stats import gmean, linregress
from collections import defaultdict

#%%
# Constant parameter:
fee_buy = 0.15/100
fee_sell = -0.25/100

#%%
# 0) base

def gmean_ignore_nan(values):
    return gmean(values.dropna())

# 1) load data

def load_base_data(database_version, param_valm):
    user = getpass.getuser()
    if database_version == 25:
        df = pd.read_hdf(f'C:\\Users\\{user}\\OneDrive\\Amethyst Invest\\Database\\DATABASEv25\\I-PCA_FULL\\PCA.h5')

    else:
        df = load_pca(database_version=database_version)

    indicator_list = [f'VALM-MA_{param_valm}D-B_1D-RH', 'PCA-GR_1D', 'PCA-GR_1D-A_1D',
                        'PPAT-A1', 'DIV.CFO-SUM_4Q.PAT-SUM_4Q', 'DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q']
    df = load_indicator_list(df, database_version, indicator_list)
    date_count_ref = load_date_count_ref(database_version)
    date_count_ref = date_count_ref.reset_index()
    date_count_ref.rename(columns= {'index':'date_trading_count'}, inplace= True)
    df = pd.merge(df, date_count_ref, on= 'DATE_TRADING', how= 'left')
    df['PCA-RV_120D'] = np.where(df['TICKER'] == df['TICKER'].shift(120),df['PCA'].rolling(window = 120).rank(method= 'max', pct= True, ascending= True), np.nan)
    df['PCA-RV_XDP_120D'] = np.where(df['TICKER'] == df['TICKER'].shift(120),df['PCA'].rolling(window = 120).rank(method= 'max', pct= True, ascending= False), np.nan)
    # df['PCA-GR_1D'] = np.where(df['TICKER'] == df['TICKER'].shift(1), df['PCA'] /df['PCA'].shift(1), np.nan)
    # df['PCA-GR_1D-A_1D'] = np.where(df['TICKER'] == df['TICKER'].shift(-1), df['PCA-GR_1D'].shift(-1), np.nan)

    # fill_fa_indicator(df, 'PPAT-A1')
    # fill_fa_indicator(df, 'DIV.CFO-SUM_4Q.PAT-SUM_4Q')
    # fill_fa_indicator(df, 'DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q')

    return df

def load_data_pca_update_daily(window):

    # Create a connection string to the SQL database
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=amethyst-dw.datapot.edu.vn;'
        'DATABASE=fiin_db;'
        'UID=amethyst_reader;'
        'PWD=1231!#ASDF!AMTHYST;'
    )

    # Connect to the SQL database
    conn = pyodbc.connect(conn_str)

    # load data giá từ sql về
    query_ohlc = f'''
    SELECT *
    FROM (
        SELECT TICKER, DATE_TRADING, PRICE_CLOSE_ADJUSTED,
        ROW_NUMBER() OVER (PARTITION BY TICKER ORDER BY DATE_TRADING DESC) AS ROW_NUM
        FROM OP.OHLC_ADJUSTED
    ) subq
    WHERE ROW_NUM <= {window}
    order by TICKER asc, DATE_TRADING asc
    '''

    df_ohlc = pd.read_sql(query_ohlc, conn)
    df_ohlc['DATE_TRADING'] = df_ohlc['DATE_TRADING'].astype('datetime64[ns]')
    max_data_ohlc = max(df_ohlc['DATE_TRADING'])
    print(f'Bảng OP.OHLC_ADJUSTED đã cập nhật đến ngày {max_data_ohlc}')

    # load data volm từ sql về
    query_volm = '''
    SELECT *
    FROM [OP].[VOLUME_MATCHED_SUM_70D_RAX0]
    ORDER BY TICKER, DATE_TRADING
    '''

    df_volm = pd.read_sql(query_volm, conn)
    df_volm['DATE_TRADING'] = df_volm['DATE_TRADING'].astype('datetime64[ns]')
    max_data_volm = max(df_volm['DATE_TRADING'])
    print(f'Bảng OP.VOLUME_MATCHED_SUM_70D_RAX0 đã cập nhật đến ngày {max_data_volm}')

    # merge data giá và data volm
    df = pd.merge(df_ohlc, df_volm, how= 'left', on= ['TICKER','DATE_TRADING'])
    df['VALM-MA_70D-RH-B_1D'] = np.where(df['TICKER'] == df['TICKER'].shift(1), df['VOLUME_MATCHED_SUM_70D_RAX0'].shift(1), np.nan)

    return df

def get_pca_from_api(time_interval, source_history = 'DNSE', source_intraday = 'TCBS', history_have_today = False, valm_ma = 10, window_priority = 20, window_rv = 240, window_bb = 20):

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    start_date = today - timedelta(days = time_interval)
    start_date = start_date.strftime("%Y-%m-%d")

    df_stock_list = listing_companies(live=True)
    df_stock_list = df_stock_list[df_stock_list['comGroupCode'] == 'HOSE']
    stock_list = df_stock_list.ticker.values

    df_database = pd.DataFrame()
    for i in stock_list:
        df_historical_price = stock_historical_data(symbol= i, 
                                start_date= start_date, 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_history)
        df_database = pd.concat([df_database,df_historical_price], ignore_index= True)

        if history_have_today == False:
            df_last_price = stock_historical_data(symbol= i, 
                                start_date= (today - timedelta(days = 1)).strftime("%Y-%m-%d"), 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_intraday)
            df_database = pd.concat([df_database,df_last_price], ignore_index= True)
        print(f'{i}')

    df_database.rename(columns= {'ticker':'TICKER','time':'DATE_TRADING'}, inplace= True)
    df_database['DATE_TRADING'] = pd.to_datetime(df_database['DATE_TRADING'])
    df_database['valm'] = df_database['close'] * (df_database['volume'] / 10**9)
    ts_rank_create(df_database, indicator = 'close', window = window_rv)
    ts_mean_create(df_database, indicator = 'valm', window = valm_ma)
    ts_mean_create(df_database, indicator = 'close', window = window_priority)

    df_database[f'valm-ma_{valm_ma}-rh'] = df_database.groupby('DATE_TRADING')[f'ts_mean(valm,{valm_ma})'].rank(method= 'max', ascending= True, pct= True)
    df_database[f'valm-ma_{valm_ma}-b_1d-rh'] = df_database[f'valm-ma_{valm_ma}-rh'].shift(1)
    df_database[f'div.pca.ts_mean(close,{window_priority})'] = df_database['close'] / df_database[f'ts_mean(close,{window_priority})']
    df_database[f'pca_gr_1d'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(1), df_database['close'] / df_database['close'].shift(1), np.nan )
    df_database[f'std'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).std(), np.nan )
    df_database[f'mean'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).mean(), np.nan )
    df_database[f'upper_bollinger'] = df_database[f'mean'] + df_database[f'std'] * 2
    df_database[f'lower_bollinger'] = df_database[f'mean'] - df_database[f'std'] * 2
    df_database[f'div.pca.upper_bollinger'] = df_database[f'close'] / df_database[f'upper_bollinger']
    df_database[f'div.pca.lower_bollinger'] = df_database[f'close'] / df_database[f'lower_bollinger']

    return df_database

def get_pca_from_api_batch_1(time_interval, source_history = 'DNSE', source_intraday = 'TCBS', history_have_today = False, valm_ma = 10, window_priority = 20, window_rv = 240, window_bb = 20):

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    start_date = today - timedelta(days = time_interval)
    start_date = start_date.strftime("%Y-%m-%d")

    df_stock_list = listing_companies(live=True)
    df_stock_list = df_stock_list[df_stock_list['comGroupCode'] == 'HOSE'].reset_index()
    df_stock_list = df_stock_list[df_stock_list.index < 200]
    stock_list = df_stock_list.ticker.values

    df_database = pd.DataFrame()
    for i in stock_list:
        df_historical_price = stock_historical_data(symbol= i, 
                                start_date= start_date, 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_history)
        df_database = pd.concat([df_database,df_historical_price], ignore_index= True)

        if history_have_today == False:
            df_last_price = stock_historical_data(symbol= i, 
                                start_date= (today - timedelta(days = 1)).strftime("%Y-%m-%d"), 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_intraday)
            df_database = pd.concat([df_database,df_last_price], ignore_index= True)
        print(f'{i}')

    df_database.rename(columns= {'ticker':'TICKER','time':'DATE_TRADING'}, inplace= True)
    df_database['DATE_TRADING'] = pd.to_datetime(df_database['DATE_TRADING'])
    df_database['valm'] = df_database['close'] * (df_database['volume'] / 10**9)
    ts_rank_create(df_database, indicator = 'close', window = window_rv)
    ts_mean_create(df_database, indicator = 'valm', window = valm_ma)
    ts_mean_create(df_database, indicator = 'close', window = window_priority)

    df_database[f'valm-ma_{valm_ma}-rh'] = df_database.groupby('DATE_TRADING')[f'ts_mean(valm,{valm_ma})'].rank(method= 'max', ascending= True, pct= True)
    df_database[f'valm-ma_{valm_ma}-b_1d-rh'] = df_database[f'valm-ma_{valm_ma}-rh'].shift(1)
    df_database[f'div.pca.ts_mean(close,{window_priority})'] = df_database['close'] / df_database[f'ts_mean(close,{window_priority})']
    df_database[f'pca_gr_1d'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(1), df_database['close'] / df_database['close'].shift(1), np.nan )
    df_database[f'std'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).std(), np.nan )
    df_database[f'mean'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).mean(), np.nan )
    df_database[f'upper_bollinger'] = df_database[f'mean'] + df_database[f'std'] * 2
    df_database[f'lower_bollinger'] = df_database[f'mean'] - df_database[f'std'] * 2
    df_database[f'div.pca.upper_bollinger'] = df_database[f'close'] / df_database[f'upper_bollinger']
    df_database[f'div.pca.lower_bollinger'] = df_database[f'close'] / df_database[f'lower_bollinger']

    return df_database

def get_pca_from_api_batch_2(time_interval, source_history = 'DNSE', source_intraday = 'TCBS', history_have_today = False, valm_ma = 10, window_priority = 20, window_rv = 240, window_bb = 20):

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    start_date = today - timedelta(days = time_interval)
    start_date = start_date.strftime("%Y-%m-%d")

    df_stock_list = listing_companies(live=True)
    df_stock_list = df_stock_list[df_stock_list['comGroupCode'] == 'HOSE'].reset_index()
    df_stock_list = df_stock_list[df_stock_list.index >= 200]
    stock_list = df_stock_list.ticker.values

    df_database = pd.DataFrame()
    for i in stock_list:
        df_historical_price = stock_historical_data(symbol= i, 
                                start_date= start_date, 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_history)
        df_database = pd.concat([df_database,df_historical_price], ignore_index= True)

        if history_have_today == False:
            df_last_price = stock_historical_data(symbol= i, 
                                start_date= (today - timedelta(days = 1)).strftime("%Y-%m-%d"), 
                                end_date = today_str, 
                                resolution='1D', 
                                type='stock', 
                                beautify=True, 
                                decor=False, 
                                source= source_intraday)
            df_database = pd.concat([df_database,df_last_price], ignore_index= True)
        print(f'{i}')

    df_database.rename(columns= {'ticker':'TICKER','time':'DATE_TRADING'}, inplace= True)
    df_database['DATE_TRADING'] = pd.to_datetime(df_database['DATE_TRADING'])
    df_database['valm'] = df_database['close'] * (df_database['volume'] / 10**9)
    ts_rank_create(df_database, indicator = 'close', window = window_rv)
    ts_mean_create(df_database, indicator = 'valm', window = valm_ma)
    ts_mean_create(df_database, indicator = 'close', window = window_priority)

    df_database[f'valm-ma_{valm_ma}-rh'] = df_database.groupby('DATE_TRADING')[f'ts_mean(valm,{valm_ma})'].rank(method= 'max', ascending= True, pct= True)
    df_database[f'valm-ma_{valm_ma}-b_1d-rh'] = df_database[f'valm-ma_{valm_ma}-rh'].shift(1)
    df_database[f'div.pca.ts_mean(close,{window_priority})'] = df_database['close'] / df_database[f'ts_mean(close,{window_priority})']
    df_database[f'pca_gr_1d'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(1), df_database['close'] / df_database['close'].shift(1), np.nan )
    df_database[f'std'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).std(), np.nan )
    df_database[f'mean'] = np.where(df_database['TICKER'] == df_database['TICKER'].shift(window_bb), df_database['close'].rolling(window= window_bb).mean(), np.nan )
    df_database[f'upper_bollinger'] = df_database[f'mean'] + df_database[f'std'] * 2
    df_database[f'lower_bollinger'] = df_database[f'mean'] - df_database[f'std'] * 2
    df_database[f'div.pca.upper_bollinger'] = df_database[f'close'] / df_database[f'upper_bollinger']
    df_database[f'div.pca.lower_bollinger'] = df_database[f'close'] / df_database[f'lower_bollinger']

    return df_database

def get_local_dtb_dir(database_version):
    """Lấy direction """

    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
    return local_dtb_dir

def get_factor_for_indicator(indicator, database_version):
    try:
        local_dtb_dir = get_local_dtb_dir(database_version)
        save_file_name = "ILUT.xlsx"
        ilut_df = pd.read_excel(os.path.join(local_dtb_dir, save_file_name))
        output = ilut_df[ilut_df["INDICATOR"] == indicator]["FACTOR"].values[0]
        return output
    except IndexError:
        print(f"I am having a problem with indicator: {indicator}")
        return np.nan

def load_volm(database_version):
    """Khởi tạo 1 dataframe bắt đầu với indicator Volume

    Args:
        df: Tên dataframe được lắp indicator vào
        database_version: là 15, 17, 19, hay 21 hay bất kỳ version nào mới hơn
        indicator (string): chính là tên indicator VALM
    """
    indicator = 'VALM-MA_70D-B_1D-RH'
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
    factor = get_factor_for_indicator(indicator, database_version)
    df = pd.read_hdf(os.path.join(local_dtb_dir,f"I-{factor}",f'{indicator}.h5'))   
    df = df.drop_duplicates(subset= ['TICKER','DATE_TRADING']).reset_index(drop = True)   

    return df

def load_pca(database_version):
    """Khởi tạo 1 dataframe bắt đầu với indicator Volume

    Args:
        df: Tên dataframe được lắp indicator vào
        database_version: là 15, 17, 19, hay 21 hay bất kỳ version nào mới hơn
        indicator (string): chính là tên indicator VALM
    """
    indicator = 'PCA'
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
    factor = get_factor_for_indicator(indicator, database_version)
    df = pd.read_hdf(os.path.join(local_dtb_dir,f"I-{factor}",f'{indicator}.h5'))
    df = df.drop_duplicates(subset= ['TICKER','DATE_TRADING']).reset_index(drop = True)   
    return df

def load_indicator(df, database_version, indicator):
    """lấy indicator từ kho onedrive

    Args:
        df: Tên dataframe được lắp indicator vào
        database_version: là 15, 17, 19, hay 21 hay bất kỳ version nào mới hơn
        indicator (string): tên indicator sử dụng
    """
    if indicator not in df.columns:
        onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
        local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
        factor = get_factor_for_indicator(indicator, database_version)
        df_tem = pd.read_hdf(os.path.join(local_dtb_dir,f"I-{factor}",f'{indicator}.h5'))
        df = pd.merge(df, df_tem, how= 'left', on=['TICKER', 'DATE_TRADING'])   
        df = df.drop_duplicates(subset= ['TICKER','DATE_TRADING']).reset_index(drop= True)
        # df = df.sort_values(by=['TICKER', 'DATE_TRADING'])
    
    return df
 
def load_indicator_list(df, database_version, indicator_list):
    """Lấy list indicator lắp vào với nhau
       
    Args:
        df: Tên dataframe được lắp indicator vào
        database_version: là 15, 17, 19, hay 21 hay bất kỳ version nào mới hơn
        indicator (string): tên indicator sử dụng"""

    for indicator in indicator_list:
        df = load_indicator(df, database_version, indicator)
    return df

def load_date_count_ref(database_version = 29):
    """load file date_count_ref để lấy các thông tin ngày tháng
       
    Args:
        df: Tên dataframe được lắp indicator vào
        database_version: mặc định là 29 là 15, 17, 19, hay 21 hay bất kỳ version nào mới hơn"""
    # user = getpass.getuser()
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
    file_name = f"DATE_COUNT_REF.xlsx"
    file_save_dir = local_dtb_dir
    date_count_ref_df = pd.DataFrame(pd.read_excel(os.path.join(file_save_dir, file_name)))
    # date_count_ref_df = pd.DataFrame(pd.read_excel(f'C:\\Users\\{user}\\OneDrive\\Amethyst Invest\\Database\\DATABASEv{database_version}\\{file_name}'))
    return date_count_ref_df

def fill_fa_indicator(df, indicator):
    """fill data fa từ quý thành ngày"""
    grouped = df.groupby(['TICKER','AM_QUARTER_STR'])
    df[indicator] = grouped[indicator].ffill()

def save_cong_indicator(df, indicator_text, database_version):
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\\Database\\DATABASEv{database_version}\\tem\\cong")
    df.to_hdf(os.path.join(local_dtb_dir,f'{indicator_text}.h5'), key = 'values', mode = 'w')

# 2) create indicator, signal, position

def position_create(df, t3 = 'true', cefl = 'false'):
    """Tạo Position khi đã có signal_in và signal_out"""

    df_tem = df.copy().reset_index(drop = True)

    matching_columns_in = [col for col in df_tem.columns if "signal_in_" in col]
    matching_columns_out = [col for col in df_tem.columns if "signal_out_" in col]

    df_tem['signal_in'] = df_tem[matching_columns_in].prod(axis=1)
    df_tem['signal_out'] = df_tem[matching_columns_out].sum(axis=1)
    df_tem['signal_out'] = np.where(df_tem['signal_out'] > 0, 1, 0)
    df_tem['position'] = df_tem['signal_in'] + df_tem['signal_out']
    
    ticker_arr = df_tem['TICKER']
    min_index = df_tem.index.min()
    index_arr = df_tem.index.values
    signal_in_arr = df_tem['signal_in'].values
    signal_out_arr = df_tem['signal_out'].values
    position_arr = df_tem['position'].values

    for index in index_arr:
        if (signal_out_arr[index] == 1):
            position_arr[index] = 0
        elif signal_in_arr[index] == 1:
            position_arr[index] = 1
        elif index == min_index:
            position_arr[index] = 0
        elif ticker_arr[index] != ticker_arr[index -1]:
            position_arr[index] = 0
        else:
            position_arr[index] = position_arr[index - 1]
    df_tem['position'] = position_arr

    if cefl == 'true':
        signal_create(df_tem, indicator = 'PCA-GR_1D', signal_kind = 'signal_out', method = 'greater_or_equal', threshold = 1.065)
        signal_create(df_tem, indicator = 'PCA-GR_1D', signal_kind = 'signal_in', method = 'smaller_or_equal', threshold = 0.935)
        signal_out_arr = df_tem['signal_out_PCA-GR_1D']

        position_cefl = position_arr.copy()
        for i in index_arr:
            if (i == 0) and (position_arr[i] == 1) and (signal_out_arr[i] == 1):
                position_cefl[i] = 0
            elif (i != 0) and (position_cefl[i-1] == 0) and (position_arr[i] == 1) and (signal_out_arr[i] == 1):
                position_cefl[i] = 0
            elif (i != 0) and(position_cefl[i-1] == 1) and (position_arr[i] == 0) and (signal_out_arr[i] == 1):
                position_cefl[i] = 1
        position_arr = position_cefl
        df_tem['position'] = position_arr

    if t3 == 'true':
        position_arr_t3 = position_arr.copy()
        for index in index_arr:
            try:
                if index == min_index and position_arr[index] == 1 and ticker_arr[index] == ticker_arr[index + 2]:
                    position_arr_t3[index + 1] = 1
                    position_arr_t3[index + 2] = 1
                elif index != min_index and position_arr[index] == 1 and position_arr_t3[index - 1] == 0 and ticker_arr[index] == ticker_arr[index + 2]:
                    position_arr_t3[index + 1] = 1
                    position_arr_t3[index + 2] = 1
            except IndexError:
                continue
        df_tem['position'] = position_arr_t3

    return df_tem

def signal_create(df, signal_kind, indicator, method, threshold):
    """
    dataframe: tên của dataframe chứa indicator
    signal_kind: chọn giữa 2 loại signal_in, signal_out 
    indicator: tên của indicator
    method: chọn giữa equal, greater, smaller, greater_or_equal, smaller_or_equal
    threshold: ngưỡng threshold
    """
    if signal_kind == 'signal_in':
        if method == "equal": 
            df[f'signal_in_{indicator}'] = np.where( df[indicator] == threshold, 1, 0 )
        elif method == "greater":
            df[f'signal_in_{indicator}'] = np.where( df[indicator] > threshold, 1, 0 )
        elif method == "greater_or_equal":
            df[f'signal_in_{indicator}'] = np.where( df[indicator] >= threshold, 1, 0 )
        elif method == "smaller":
            df[f'signal_in_{indicator}'] = np.where( df[indicator] < threshold, 1, 0 )
        elif method == "smaller_or_equal":
            df[f'signal_in_{indicator}'] = np.where( df[indicator] <= threshold, 1, 0 )
        elif method == "cross_over":
            df[f'signal_in_{indicator}'] = np.where( (df['TICKER'] == df['TICKER'].shift(1)) & (df[indicator] >= threshold) & (df[indicator].shift(1) < threshold), 1, 0)
        elif method == "cross_under":
            df[f'signal_in_{indicator}'] = np.where( (df['TICKER'] == df['TICKER'].shift(1)) & (df[indicator] < threshold) & (df[indicator].shift(1) >= threshold), 1, 0)
        elif method == "unequal":
            df[f'signal_in_{indicator}'] = np.where( df[indicator] != threshold, 1, 0 )
    elif signal_kind == 'signal_out':
        if method == "equal": 
            df[f'signal_out_{indicator}'] = np.where( df[indicator] == threshold, 1, 0 )
        elif method == "greater":
            df[f'signal_out_{indicator}'] = np.where( df[indicator] > threshold, 1, 0 )
        elif method == "greater_or_equal":
            df[f'signal_out_{indicator}'] = np.where( df[indicator] >= threshold, 1, 0 )
        elif method == "smaller":
            df[f'signal_out_{indicator}'] = np.where( df[indicator] < threshold, 1, 0 )
        elif method == "smaller_or_equal":
            df[f'signal_out_{indicator}'] = np.where( df[indicator] <= threshold, 1, 0 )
        elif method == "cross_over":
            df[f'signal_out_{indicator}'] = np.where( (df['TICKER'] == df['TICKER'].shift(1)) & (df[indicator] >= threshold) & (df[indicator].shift(1) < threshold), 1, 0)
        elif method == "cross_under":
            df[f'signal_out_{indicator}'] = np.where( (df['TICKER'] == df['TICKER'].shift(1)) & (df[indicator] < threshold) & (df[indicator].shift(1) >= threshold), 1, 0)  
        elif method == "unequal":
            df[f'signal_out_{indicator}'] = np.where( df[indicator] != threshold, 1, 0 )
    else:
        print('chắc là sai method')

def signal_bound_create(df, signal_kind, indicator, lower_bound, upper_bound):
    """
    dataframe: tên của dataframe chứa indicator
    signal_kind: chọn giữa 2 loại signal_in, signal_out 
    indicator: tên của indicator
    method: chọn giữa equal, greater, smaller, greater_or_equal, smaller_or_equal
    threshold: ngưỡng threshold
    """
    if signal_kind == 'signal_in':
        df[f'signal_in_{indicator}'] = np.where((df[indicator] >= lower_bound) & (df[indicator] <= upper_bound), 1, 0 )

    elif signal_kind == 'signal_out':
        df[f'signal_out_{indicator}'] = np.where((df[indicator] < lower_bound) | (df[indicator] > upper_bound), 1, 0 )

def position_trailing_stop_create(df, threshold, database_version = 29):

    indicator_list = ['PHA','PLA']
    df = load_indicator_list(df, database_version = database_version, indicator_list = indicator_list)
    df = df.reset_index(drop=True)

    matching_columns_in = [col for col in df.columns if "signal_in_" in col]
    df['signal_in'] = df[matching_columns_in].prod(axis=1)

    signal_create(df, indicator='signal_in', signal_kind='signal_in', method='cross_over', threshold=1)
    index = df.index.values
    df['position_tem'] = 0
    position_arr = df['position_tem'].values
    signal_in_signal_in_arr = df['signal_in_signal_in'].values
    pla_arr = df['PLA'].values
    pha_arr = df['PHA'].values

    highest_pca_arr = []
    drawdown_arr = []

    for i in index:
        if i == 0 or (i != 0 and position_arr[i-1] == 1):
            if signal_in_signal_in_arr[i] == 1:
                # highest_pca = pha_arr[i]
                highest_pca = df.loc[i,'PCA']
                drawdown = pla_arr[i] / highest_pca
                position_arr[i] = 0
            else:
                highest_pca = np.nan
                drawdown = pla_arr[i] / highest_pca
                position_arr[i] = 1

        elif i != 0 and position_arr[i-1] == 0:
            if pha_arr[i] > highest_pca:
                highest_pca = pha_arr[i]
            drawdown = pla_arr[i] / highest_pca

            position_arr[i] = 1 if drawdown < threshold else 0

        highest_pca_arr.append(highest_pca)
        drawdown_arr.append(drawdown)

    df['signal_out_trailing_stop'] = position_arr
    # df['trailing_drawdown'] = drawdown_arr
    # df['highest_trailing_pca'] = highest_pca_arr
    return df['signal_out_trailing_stop']

def position_trailing_stop_create_and_reenter(df, threshold_cut_loss, threshold_reenter, database_version = 29):
    
    df = position_create(df)

    indicator_list = ['PHA','PLA']
    df = load_indicator_list(df, database_version = database_version, indicator_list = indicator_list)
    df = df.reset_index(drop=True)

    index = df.index.values
    position_arr = df['position'].values
    position_actual_arr = position_arr.copy()
    ticker_arr = df['TICKER'].values
    pla_arr = df['PLA'].values
    pha_arr = df['PHA'].values

    lowest_pca_arr = []
    highest_pca_arr = []
    rebound_arr = []
    drawdown_arr = []

    for i in index:
        if (i == 0) or (ticker_arr[i] != ticker_arr[i-1]):
            if position_arr[i] == 1:
                highest = df.loc[i,'PCA']
                lowest = df.loc[i,'PCA']
                drawdown = 1
                rebound = np.nan
            else:
                highest = np.nan
                lowest = np.nan
                drawdown = np.nan
                rebound = np.nan

        elif (position_arr[i] == 1) and (ticker_arr[i] == ticker_arr[i-1]):
            if (position_arr[i-1] == 0):
                highest = df.loc[i,'PCA']
                lowest = pla_arr[i]
                drawdown = 1
                rebound = np.nan
            elif (position_arr[i-1] == 1):
                if(position_actual_arr[i-1] == 1):
                    if pha_arr[i] > highest:
                        highest = pha_arr[i]
                    lowest = pla_arr[i]
                    drawdown = pla_arr[i]/highest
                    rebound = np.nan
                    if drawdown < threshold_cut_loss:
                        position_actual_arr[i] = 0
                        lowest = df.loc[i,'PCA']
                        highest = df.loc[i,'PCA']

                elif (position_actual_arr[i-1] == 0):
                    if pla_arr[i] < lowest:
                        lowest = pla_arr[i]
                    highest = pha_arr[i]
                    drawdown = np.nan
                    rebound = pha_arr[i]/lowest
                    
                    if rebound > threshold_reenter:                    
                        position_actual_arr[i] = 1
                        lowest = df.loc[i,'PCA']
                        highest = df.loc[i,'PCA']
                    else:
                        position_actual_arr[i] = 0
        elif (position_arr[i] == 0):
            lowest = np.nan
            highest = np.nan
            drawdown = np.nan
            rebound = np.nan

        lowest_pca_arr.append(lowest)
        highest_pca_arr.append(highest)
        drawdown_arr.append(drawdown)
        rebound_arr.append(rebound)

    df['assign_trailing_cut_loss_and_reenter'] = position_actual_arr
    df['lowest_trailing'] = lowest_pca_arr
    df['highest_trailing'] = highest_pca_arr
    df['trailing_drawdown'] = drawdown_arr
    df['trailing_rebound'] = rebound_arr

    return df

def group_create(df, indicator_1, signal_kind_1, method_1, threshold_1, indicator_2, signal_kind_2, method_2, threshold_2 ):
    signal_create(df, indicator = indicator_1, signal_kind= signal_kind_1, method= method_1, threshold= threshold_1)
    signal_create(df, indicator = indicator_2, signal_kind= signal_kind_2, method= method_2, threshold= threshold_2)
    df['group'] = np.where((df[indicator_1].isna()) | (df[indicator_2].isna()), np.nan, np.where(
                        (df[f'signal_in_{indicator_1}'] == 1) & (df[f'signal_in_{indicator_2}'] == 1), 'a & b', np.where(
                       (df[f'signal_in_{indicator_1}'] == 1) & (df[f'signal_in_{indicator_2}'] == 0), 'a, not b',np.where(
                       (df[f'signal_in_{indicator_1}'] == 0) & (df[f'signal_in_{indicator_2}'] == 1), 'not a, b', 'not a, not b'))))

def percentage_positive_negative_return_create(df, gr, ma, rank, valm):
    df[f'PCA-GR_{gr}D'] = np.where(df.TICKER == df.TICKER.shift(gr), df.PCA / df.PCA.shift(gr), np.nan)
    df_gr = df[['TICKER','DATE_TRADING','PCA','VALM-MA_70D-B_1D-RH',f'PCA-GR_{gr}D']].copy()
    df_gr[f'PCA-GR_{gr}'] = np.where(df_gr.TICKER == df_gr.TICKER.shift(gr), df_gr.PCA / df_gr.PCA.shift(gr), np.nan)
    df_positive_return = pd.DataFrame(df_gr[(df_gr['VALM-MA_70D-B_1D-RH'] > valm) & (df_gr[f'PCA-GR_{gr}'] > 1)].groupby('DATE_TRADING')[f'PCA-GR_{gr}'].count()).reset_index()
    df_negative_return = pd.DataFrame(df_gr[(df_gr['VALM-MA_70D-B_1D-RH'] > valm) & (df_gr[f'PCA-GR_{gr}'] < 1)].groupby('DATE_TRADING')[f'PCA-GR_{gr}'].count()).reset_index()
    df_valm = pd.DataFrame(df_gr[(df_gr['VALM-MA_70D-B_1D-RH'] > valm)].groupby('DATE_TRADING')[f'PCA-GR_{gr}'].count()).reset_index()

    df_positive_return.rename(columns= {f'PCA-GR_{gr}':f'count(pca_gr{gr}>1)'}, inplace= True)
    df_negative_return.rename(columns= {f'PCA-GR_{gr}':f'count(pca_gr{gr}<1)'}, inplace= True)
    df_valm.rename(columns= {f'PCA-GR_{gr}':f'count(valm>0.6)'}, inplace= True)

    df_valm = pd.merge(df_valm, df_positive_return, how= 'left', on= 'DATE_TRADING')
    df_valm = pd.merge(df_valm, df_negative_return, how= 'left', on= 'DATE_TRADING')

    df_valm[f'count(valm>0.6)'].fillna(value=0, inplace= True)
    df_valm[f'count(pca_gr{gr}>1)'].fillna(value=0, inplace= True)
    df_valm[f'count(pca_gr{gr}<1)'].fillna(value=0, inplace= True)

    df_valm[f'percentage_positive_return_{gr}d'] = df_valm[f'count(pca_gr{gr}>1)'] / df_valm[f'count(valm>0.6)']
    df_valm[f'percentage_negative_return_{gr}d'] = df_valm[f'count(pca_gr{gr}<1)'] / df_valm[f'count(valm>0.6)']

    df_valm[f'ts_mean(percentage_positive_return_{gr}d,{ma})'] = df_valm[f'percentage_positive_return_{gr}d'].rolling(window = ma).mean()
    df_valm[f'ts_mean(percentage_negative_return_{gr}d,{ma})'] = df_valm[f'percentage_negative_return_{gr}d'].rolling(window = ma).mean()

    df_valm[f'ts_rank(ts_mean(percentage_positive_return_{gr}d,{ma}),{rank}'] = df_valm[f'ts_mean(percentage_positive_return_{gr}d,{ma})'].rolling(window= rank).rank(method= 'max', pct= True, ascending= True)
    df_valm[f'ts_rank(ts_mean(percentage_negative_return_{gr}d,{ma}),{rank}'] = df_valm[f'ts_mean(percentage_negative_return_{gr}d,{ma})'].rolling(window= rank).rank(method= 'max', pct= True, ascending= True)
    df = pd.merge(df, df_valm, how= 'left', on= 'DATE_TRADING')
    return df

def volatility_create(df, window, method):
    if method == 'pca':
        df[f'ts_std(pca,{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df['PCA'].rolling(window = window).std(), np.nan)
        df[f'mean(pca,{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df['PCA'].rolling(window = window).mean(), np.nan)
        df[f'ts_std(pca,{window})'] = df[f'ts_std(pca,{window})'] / df[f'mean(pca,{window})']
        
    elif method == 'r1d':
        df[f'ts_std(r1d,{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df['PCA-GR_1D'].rolling(window = window).std(), np.nan)
        
def rv_volatility_create(df, window, window_rank, method):    
    df[f'ts_rank(ts_std({method},{window}),{window_rank},xap)'] = df[f'ts_std({method},{window})'].rolling(window = window_rank).rank(method= 'max', ascending= True, pct= True)
    return df

def rh_volatility_create(df, window, method, universe, date_start, date_end, valm):
    if universe == 'hose':
        df_tem = df
    else:
        df_tem = eval(f'{universe}_universe')(df,date_start,date_end,valm)

    df_rank = pd.DataFrame(df_tem.groupby('DATE_TRADING')[f'ts_std({method},{window})'].rank(method = 'max', ascending = True, pct = True)).reset_index(drop= True)
    df_rank.rename(columns= {f'ts_std({method},{window})':f'rank(ts_std({method},{window}),{universe},xap)'}, inplace= True)
    df_tem = pd.merge(df_tem, df_rank, left_index= True, right_index= True)
    df = pd.merge(df, df_tem[['DATE_TRADING', 'TICKER', f'rank(ts_std({method},{window}),{universe},xap)']], how= 'left', on= ['TICKER','DATE_TRADING'])    
    return df

def rank_create(df, indicator, window, valm=0.6):
    date_start = df['DATE_TRADING'].min()
    date_end = df['DATE_TRADING'].max()
    if window == 'hose':
        df_tem = df.copy()
        df_tem['position'] = 1
    else:
        df_tem = eval(f'{window}_universe')(df,date_start,date_end,valm)
        position_create(df_tem, t3= 'False')

    df_rank = pd.DataFrame(df_tem[df_tem['position'] == 1].groupby('DATE_TRADING')[indicator].rank(method = 'max', ascending = True, pct = True)).reset_index(drop= True)
    df_rank.rename(columns= {indicator:f'rank({indicator},{window},xap)'}, inplace= True)
    df_tem = pd.merge(df_tem, df_rank,  left_index= True, right_index= True)
    df[f'rank({indicator},{window},xap)'] = df_tem[f'rank({indicator},{window},xap)'].copy()

    return df[f'rank({indicator},{window},xap)']

def ts_rank_create(df, indicator, window):
    df[f'ts_rank({indicator},{window},xap)'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df[indicator].rolling(window = window).rank(method= 'max', ascending= True, pct= True), np.nan)
    return df[f'ts_rank({indicator},{window},xap)']

def ts_mean_create(df, indicator, window):
    df[f'ts_mean({indicator},{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df[indicator].rolling(window = window).mean(), np.nan)
    return df[f'ts_mean({indicator},{window})']

def ts_growth_create(df, indicator, window):
    df[f'ts_growth({indicator},{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df[indicator] / df[indicator].shift(window), np.nan)
    return df[f'ts_growth({indicator},{window})']

def rsi_create(df, indicator, window):
    delta = df.groupby('TICKER')[indicator].diff() / df[indicator].shift(1)
    df["GAIN"] = delta.clip(lower=0)
    df["LOSS"] = -1 * delta.clip(upper=0)
    df["EMA_GAIN" + str(window)] = df.groupby('TICKER')['GAIN'].transform(lambda x: x.ewm(com=window - 1, adjust=False).mean())
    df["EMA_LOSS" + str(window)] = df.groupby('TICKER')['LOSS'].transform(lambda x: x.ewm(com=window - 1, adjust=False).mean())
    df["RS" + str(window)] = df["EMA_GAIN" + str(window)] / df["EMA_LOSS" + str(window)]
    df[f'rsi({indicator},{window})'] = 100 - (100 / (1 + df["RS" + str(window)]))
    return df[f'rsi({indicator},{window})']

def ts_zscore_create(df, indicator, window):
    df[f'ts_mean({indicator},{window})'] = ts_mean_create(df, indicator, window)
    df[f'ts_std({indicator},{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), df[indicator].rolling(window = window).std(), np.nan)
    df[f'ts_zscore({indicator},{window})'] = np.where(df['TICKER'] == df['TICKER'].shift(window), (df[indicator] - df[f'ts_mean({indicator},{window})']) / df[f'ts_std({indicator},{window})'], np.nan)
    return df[f'ts_zscore({indicator},{window})']

def percentage_in_high_volatility_create(df, volatility_indicator, threshold, ma, rank, valm):
    df_volm = pd.DataFrame(df.groupby('DATE_TRADING')['PCA-GR_1D-A_1D'].count()).reset_index()
    df_high_volatility = pd.DataFrame(df[(df[volatility_indicator] > threshold) & (df['VALM-MA_70D-B_1D-RH'] > valm)].groupby('DATE_TRADING')['PCA-GR_1D-A_1D'].count()).reset_index()
    
    df_volm.rename(columns= {'PCA-GR_1D-A_1D':'count_volm'}, inplace= True)
    df_high_volatility.rename(columns= {'PCA-GR_1D-A_1D':'count_high_volatility'}, inplace= True)
    
    df_volm = pd.merge(df_volm, df_high_volatility, how= 'left', on= 'DATE_TRADING')
    df_volm['percentage_in_high_volatility'] = df_volm['count_high_volatility'] / df_volm['count_volm']
    df_volm.fillna(value= 0, inplace= True)

    df_volm[f'ts_mean(percentage_in_high_volatility,{ma})'] = df_volm['percentage_in_high_volatility'].rolling(window= ma).mean()
    df_volm[f'ts_rank(ts_mean(percentage_in_high_volatility,{ma}),{rank},xap)'] = df_volm[f'ts_mean(percentage_in_high_volatility,{ma})'].rolling(window= rank).rank(method= 'max', ascending= True, pct= True)
    df = pd.merge(df, df_volm[['DATE_TRADING','percentage_in_high_volatility',f'ts_rank(ts_mean(percentage_in_high_volatility,{ma}),{rank},xap)']], how= 'left', on= 'DATE_TRADING')
    return df

def percentage_in_low_volatility_create(df, volatility_indicator, threshold, ma, rank, valm):
    df_volm = pd.DataFrame(df.groupby('DATE_TRADING')['PCA-GR_1D-A_1D'].count()).reset_index()
    df_low_volatility = pd.DataFrame(df[(df[volatility_indicator] < threshold) & (df['VALM-MA_70D-B_1D-RH'] > valm)].groupby('DATE_TRADING')['PCA-GR_1D-A_1D'].count()).reset_index()
    
    df_volm.rename(columns= {'PCA-GR_1D-A_1D':'count_volm'}, inplace= True)
    df_low_volatility.rename(columns= {'PCA-GR_1D-A_1D':'count_low_volatility'}, inplace= True)
    
    df_volm = pd.merge(df_volm, df_low_volatility, how= 'left', on= 'DATE_TRADING')
    df_volm['percentage_in_low_volatility'] = df_volm['count_low_volatility'] / df_volm['count_volm']
    df_volm.fillna(value= 0, inplace= True)

    df_volm[f'ts_mean(percentage_in_low_volatility,{ma})'] = df_volm['percentage_in_low_volatility'].rolling(window= ma).mean()
    df_volm[f'ts_rank(ts_mean(percentage_in_low_volatility,{ma}),{rank}),xap'] = df_volm[f'ts_mean(percentage_in_low_volatility,{ma})'].rolling(window= rank).rank(method= 'max', ascending= True, pct= True)
    df = pd.merge(df, df_volm[['DATE_TRADING','percentage_in_low_volatility', f'ts_rank(ts_mean(percentage_in_low_volatility,{ma}),{rank}),xap']], how= 'left', on= 'DATE_TRADING')
    
    return df

def percentage_count_create_v1(df, indicator_1, method_1, threshold_1, indicator_2, method_2, threshold_2):
   
    signal_create(df, signal_kind = 'signal_in', indicator= 'VALM-MA_70D-B_1D-RH', method= 'greater_or_equal', threshold= 0.6)
    df_count_volm = pd.DataFrame(df[(df[f'signal_in_VALM-MA_70D-B_1D-RH'] == 1)].groupby('DATE_TRADING')['TICKER'].count()).reset_index()
    df_count_volm.rename(columns= {'TICKER':f'count_volm'}, inplace = True)
    df_count_volm['count_volm'].fillna(value = 0, inplace = True)

    signal_create(df, signal_kind = 'signal_in', method = method_1, indicator= indicator_1, threshold = threshold_1)
    df_count_1 = pd.DataFrame(df[(df[f'signal_in_{indicator_1}'] == 1) & (df[f'signal_in_VALM-MA_70D-B_1D-RH'] == 1)].groupby('DATE_TRADING')['TICKER'].count()).reset_index()
    df_count_1.rename(columns= {'TICKER':f'count_{indicator_1}_{method_1}_{threshold_1}'}, inplace = True)
    df_count_1[f'count_{indicator_1}_{method_1}_{threshold_1}'].fillna(value = 0, inplace = True)

    signal_create(df, signal_kind = 'signal_in', method = method_2, indicator= indicator_2, threshold = threshold_2)
    df_count_2 = pd.DataFrame(df[(df[f'signal_in_{indicator_2}'] == 1) & (df[f'signal_in_VALM-MA_70D-B_1D-RH'] == 1)].groupby('DATE_TRADING')['TICKER'].count()).reset_index()  
    df_count_2.rename(columns= {'TICKER':f'count_{indicator_2}_{method_2}_{threshold_2}'}, inplace = True)
    df_count_2[f'count_{indicator_2}_{method_2}_{threshold_2}'].fillna(value = 0, inplace = True)

    df_count = pd.merge(df_count_volm, df_count_1, how= 'left', on= 'DATE_TRADING')
    df_count = pd.merge(df_count, df_count_2, how= 'left', on= 'DATE_TRADING')

    df_count['count_volm'].fillna(value = 0, inplace = True)
    df_count[f'count_{indicator_1}_{method_1}_{threshold_1}'].fillna(value = 0, inplace = True)
    df_count[f'count_{indicator_2}_{method_2}_{threshold_2}'].fillna(value = 0, inplace = True)

    df_count[f'percentage_count_{indicator_1}_{method_1}_{threshold_1}'] = df_count[f'count_{indicator_1}_{method_1}_{threshold_1}'] / df_count[f'count_volm']
    df_count[f'percentage_count_{indicator_2}_{method_2}_{threshold_2}'] = df_count[f'count_{indicator_2}_{method_2}_{threshold_2}'] / df_count[f'count_volm']
    df_count[f'count_{indicator_1}_{method_1}_{threshold_1}/count_{indicator_2}_{method_2}_{threshold_2}'] = df_count[f'count_{indicator_1}_{method_1}_{threshold_1}'] / df_count[f'count_{indicator_2}_{method_2}_{threshold_2}']    
    df = pd.merge(df, df_count[['DATE_TRADING','count_volm', f'percentage_count_{indicator_1}_{method_1}_{threshold_1}',
                                    f'percentage_count_{indicator_2}_{method_2}_{threshold_2}',
                                    f'count_{indicator_1}_{method_1}_{threshold_1}/count_{indicator_2}_{method_2}_{threshold_2}']], on= 'DATE_TRADING', how= 'left')
    return df_count

def percentage_count_create(df, indicator, method, threshold, param_valm, valm):
   
    signal_create(df, signal_kind='signal_in', indicator=indicator, method=method, threshold=threshold)
    positive_count = df[(df[f'signal_in_{indicator}'] == 1) & (df[f'VALM-MA_{param_valm}D-B_1D-RH'] > valm)].groupby('DATE_TRADING')[f'TICKER'].count().to_frame().reset_index()
    negative_count = df[(df[f'signal_in_{indicator}'] == 0) & (df[f'VALM-MA_{param_valm}D-B_1D-RH'] > valm)].groupby('DATE_TRADING')[f'TICKER'].count().to_frame().reset_index()
    total_count = df[df[f'VALM-MA_{param_valm}D-B_1D-RH'] > 0].groupby('DATE_TRADING')[f'TICKER'].count().to_frame().reset_index()
    df = pd.merge(df, positive_count, how= 'left', on= 'DATE_TRADING', suffixes=('','_positive_count'))
    df = pd.merge(df, negative_count, how= 'left', on= 'DATE_TRADING', suffixes=('','_negative_count'))
    df = pd.merge(df, total_count, how= 'left', on= 'DATE_TRADING', suffixes=('','_total_count'))
    df['percentage_positive'] = df[f'TICKER_positive_count'] / df[f'TICKER_total_count']
    df['percentage_negative'] = df[f'TICKER_negative_count'] / df[f'TICKER_total_count']
    
    return df['percentage_positive'],df['percentage_negative']
def regression_create(df, indicator, window, method = 'slope'):

    column_name = indicator
    rolling_slope = []
    rolling_intercept = []
    rolling_p_value = []
    rolling_r_value = []
    rolling_std_err = []


    for i in df.index.values:
        if i < window:
            slope = np.nan
            intercept = np.nan
            p_value = np.nan
            r_value = np.nan
            std_err = np.nan
            
            rolling_slope.append(slope)
            rolling_intercept.append(intercept)
            rolling_p_value.append(p_value)
            rolling_r_value.append(r_value)
            rolling_std_err.append(std_err)

        elif df['TICKER'][i] == df['TICKER'][i-window]:
            window_data = df[column_name][i-window:i]
            slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(window_data)), window_data)
            
            rolling_slope.append(slope)
            rolling_intercept.append(intercept)
            rolling_p_value.append(p_value)
            rolling_r_value.append(r_value)
            rolling_std_err.append(std_err)
        else:    
            slope = np.nan
            intercept = np.nan
            p_value = np.nan
            r_value = np.nan
            std_err = np.nan
            
            rolling_slope.append(slope)
            rolling_intercept.append(intercept)
            rolling_p_value.append(p_value)
            rolling_r_value.append(r_value)
            rolling_std_err.append(std_err)

    df[f'ts_regression({indicator},{window},{method})'] = eval(f'rolling_{method}')
    return df[f'ts_regression({indicator},{window},{method})']

def ts_slope_regression_create(df, indicator, window):
    df[f'ts_slope_regression_create({indicator},{window})'] = regression_create(df, indicator, window, method = 'slope')
    return df[f'ts_slope_regression({indicator},{window})']

def fee_create(df, fee_buy = 0.15/100, fee_sell = -0.25/100):
    date_list = sorted(df['DATE_TRADING'].unique())
    df_adj = pd.DataFrame()

    daily_return = df['daily_return'].values
    nav_buy_to_nav = df['nav_buy_to_nav'].values
    nav_sell_to_nav = df['nav_sell_to_nav'].values
    cash_to_nav_total = df['cash_to_nav_total'].values

    nav_total = 1
    cash = 1
    for i in range(len(date_list)):
        fee_relative = (nav_buy_to_nav[i] * fee_buy + nav_sell_to_nav[i] * fee_sell)
        if i == 0:
            nav_total = nav_total * (1 - fee_relative)
        else:
            nav_total = (daily_return[i] + 1) * nav_total * (1 - fee_relative)
        cash = nav_total * cash_to_nav_total[i]
        nav_stock = nav_total - cash
        turnover = (nav_buy_to_nav[i] - nav_sell_to_nav[i]) / 2

        row = pd.DataFrame({ 'acc_return': [nav_total],
                            'cash': [cash],
                            'nav_stock': [nav_stock],
                            'turnover': [turnover],
                            'fee_relative': [fee_relative], 
                            })
        df_adj = pd.concat([df_adj, row], ignore_index= True)

    df_adj['DATE_TRADING'] = df['DATE_TRADING'].values
    df_adj['stock_list'] = df['stock_list'].values
    df_adj['ticker_count'] = df['ticker_count'].values
    df_adj['max_assign'] = df['max_assign'].values
    df_adj['nav_buy_to_nav'] = df['nav_buy_to_nav'].values
    df_adj['nav_buy_to_nav_arr'] = df['nav_buy_to_nav_arr'].values
    df_adj['nav_sell_to_nav'] = df['nav_sell_to_nav'].values
    df_adj['nav_sell_to_nav_arr'] = df['nav_sell_to_nav_arr'].values
    df_adj['nav_stock_to_nav_arr'] = df['nav_stock_to_nav_arr'].values

    df_adj['daily_return'] = df_adj['acc_return'] / df_adj['acc_return'].shift(1) - 1
    df_adj['daily_return'].fillna(value= 0, inplace= True)
    df_adj['cash_to_nav_total'] = df_adj['cash'] / df_adj['acc_return']
    df_adj['nav_stock_to_nav'] = df_adj['nav_stock'] / df_adj['acc_return']

    return df_adj

def valm_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'greater', threshold= valm)
    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_out', indicator= 'VALM-MA_70D-B_1D-RH', 
                  method= 'smaller', threshold= valm)
    return df

def fa_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'greater', threshold= valm)
    signal_create(df, signal_kind= 'signal_in', indicator= 'PPAT-A1', 
                  method= 'greater_or_equal', threshold= 1)
    df['signal_in_DIV.CFO-SUM_4Q.PAT-SUM_4Q'] = np.where((df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'] > 0.3) | (df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'].isna()), 1, 0)
    df['signal_in_DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] = np.where((df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] < 0.55) | (df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'].isna()), 1, 0)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'smaller', threshold= valm)
    signal_create(df, signal_kind= 'signal_out', indicator= 'PPAT-A1', 
                  method= 'smaller', threshold= 1)
    df['signal_out_DIV.CFO-SUM_4Q.PAT-SUM_4Q'] = np.where((df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'] < 0.3), 1, 0)
    df['signal_out_DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] = np.where((df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] > 0.55), 1, 0)

    return df

def dep9_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'greater', threshold= valm)
    signal_create(df, signal_kind= 'signal_in', indicator= 'PCA-RV_120D', 
                  method= 'greater_or_equal', threshold= 0.9)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'smaller', threshold= valm)
    signal_create(df, signal_kind= 'signal_out', indicator= 'PCA-RV_120D', 
                  method= 'smaller', threshold= 0.9)
    return df

def high_valm_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.9 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.9 , upper_bound= 1)
    return df

def medium_valm_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.7 , upper_bound= 0.9)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.7 , upper_bound= 0.9)
    return df

def low_valm_universe(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.6 , upper_bound= 0.7)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= 0.6 , upper_bound= 0.7)
    return df

def high_ep_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'EP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'EP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'EP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)
    return df

def medium_ep_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'EP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'EP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'EP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)
    return df

def low_ep_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'EP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'EP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'EP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def high_bp_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'BP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'BP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'BP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)
    return df

def medium_bp_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'BP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'BP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'BP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)
    return df

def low_bp_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'BP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'BP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'BP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def high_marcap_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'MARCAP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'MARCAP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'MARCAP-RH', 
                        lower_bound= 0.67 , upper_bound= 1)
    return df

def medium_marcap_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'MARCAP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'MARCAP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'MARCAP-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)
    return df

def low_marcap_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'MARCAP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'MARCAP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'MARCAP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def low_marcap_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'MARCAP-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'MARCAP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'MARCAP-RH', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def high_gr60rh_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-GR_60D-RH', database_version = database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0.67 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0.67 , upper_bound= 1)
    return df

def medium_gr60rh_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-GR_60D-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0.33 , upper_bound= 0.67)
    return df

def low_gr60rh_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-GR_60D-RH', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-GR_60D-RH', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def high_rv120_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-RV_120D', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-RV_120D', 
                        lower_bound= 0.67 , upper_bound= 1)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-RV_120D', 
                        lower_bound= 0.67 , upper_bound= 1)
    return df

def medium_rv120_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-RV_120D', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-RV_120D', 
                        lower_bound= 0.33 , upper_bound= 0.67)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-RV_120D', 
                        lower_bound= 0.33 , upper_bound= 0.67)
    return df

def low_rv120_universe(df, date_start, date_end, valm, param_valm, database_version = 29):
    df = load_indicator(df, indicator = 'PCA-RV_120D', database_version= database_version)
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'PCA-RV_120D', 
                        lower_bound= 0 , upper_bound= 0.33)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                        lower_bound= valm , upper_bound= 1)
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'PCA-RV_120D', 
                        lower_bound= 0 , upper_bound= 0.33)
    return df

def fa_signal(df, date_start, date_end, valm, param_valm):
    #signal_in
    signal_bound_create(df, signal_kind= 'signal_in', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_in', indicator= f'VALM-MA_{param_valm}D-B_1D-RH', 
                  method= 'greater', threshold= valm)
    signal_create(df, signal_kind= 'signal_in', indicator= 'PPAT-A1', 
                  method= 'greater_or_equal', threshold= 1)
    df['signal_in_DIV.CFO-SUM_4Q.PAT-SUM_4Q'] = np.where((df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'] > 0.3) | (df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'].isna()), 1, 0)
    df['signal_in_DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] = np.where((df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] < 0.55) | (df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'].isna()), 1, 0)

    #signal_out
    signal_bound_create(df, signal_kind= 'signal_out', indicator= 'DATE_TRADING', 
                        lower_bound= date_start , upper_bound= date_end)
    signal_create(df, signal_kind= 'signal_out', indicator= 'PPAT-A1', 
                  method= 'smaller', threshold= 1)
    df['signal_out_DIV.CFO-SUM_4Q.PAT-SUM_4Q'] = np.where((df['DIV.CFO-SUM_4Q.PAT-SUM_4Q'] < 0.3), 1, 0)
    df['signal_out_DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] = np.where((df['DIV.RECEIVABLES.GROSS_REVENUE-SUM_4Q'] > 0.55), 1, 0)

# 3) assign and evaluate
def deal_length_median(df, date_start, date_end):
    
    df = df[(df['DATE_TRADING']> date_start) & (df['DATE_TRADING']< date_end)].reset_index(drop= True)
    date_list = sorted(df['DATE_TRADING'].unique())
    date_list = np.array(date_list)
    df['position_diff'] = np.where(df['TICKER'] == df['TICKER'].shift(1), df['position'] - df['position'].shift(1), np.nan)
    df = df[(df['position_diff'] != 0) | (df['position'] == 1) ].reset_index(drop= True)

    date_trading = df['DATE_TRADING'].values
    ticker = df['TICKER'].values
    position = df['position'].values
    pca_arr = df['PCA'].values

    ticker_arr = []
    date_start_arr = []
    date_end_arr = []
    pca_start_arr = []
    pca_end_arr = []

    for n in range(len(date_trading)):
        # print(n)
        if (n == 0):
            if (position[n] == 1):
                ticker_deal = ticker[n]
                date_start_deal = date_trading[n]
                pca_start_deal = pca_arr[n]
                ticker_arr.append(ticker_deal)
                date_start_arr.append(date_start_deal)
                pca_start_arr.append(pca_start_deal)
                # ticker_arr = np.array(ticker_arr, ticker_deal)
                # date_start_arr = np.array(date_start_arr, date_start_deal)
                # pca_start_arr = np.array(pca_start_arr, pca_start_deal)

        elif (n != 0):
            if (ticker[n] == ticker[n-1]):
                if (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 0) and (position[n-1] == 1):
                    date_end_deal = date_trading[n]
                    pca_end_deal = pca_arr[n]
                    date_end_arr.append(date_end_deal)  
                    pca_end_arr.append(pca_end_deal)

            elif (ticker[n] != ticker[n-1]):
                if (position[n-1] == 1) and ((position[n] == 0)):
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

                elif (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 1) and (position[n-1] == 1):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]

                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

        elif (n == (len(date_trading) - 1)) and (position[n] == 1):
            date_end_deal = date_trading[n]
            pca_end_deal = pca_arr[n]
            date_end_arr.append(date_end_deal)
            pca_end_arr.append(pca_end_deal)

    date_count = []

    for i in range(len(ticker_arr)):
        # date_count_deal = len([x for x in date_list if date_start_arr[i] < x <= date_end_arr[i]])
        # date_count_deal = date_list.index(date_end_arr[i]) - date_list.index(date_start_arr[i]) 
        date_count_deal = (np.where(date_list == date_end_arr[i])[0][0] if np.any(date_list == date_end_arr[i]) else -1) - (np.where(date_list == date_start_arr[i])[0][0] if np.any(date_list == date_start_arr[i]) else -1 )
        
        date_count.append(date_count_deal)
        deal_length_median = np.median(date_count)
        
    return deal_length_median

def position_analysis(df, date_start, date_end):
    """ deal_analysis: Kết quả sẽ là 1 bảng để nghiên cứu deal_length và 1 bảng nghiên cứu return"""
    deal_df = pd.DataFrame()
    df = df[(df['DATE_TRADING']> date_start) & (df['DATE_TRADING']< date_end)].reset_index(drop= True)
    date_list = sorted(df['DATE_TRADING'].unique())
    date_list = np.array(date_list)
    df['position_diff'] = np.where(df['TICKER'] == df['TICKER'].shift(1), df['position'] - df['position'].shift(1), np.nan)
    df = df[(df['position_diff'] != 0) | (df['position'] == 1) ].reset_index(drop= True)

    date_trading = df['DATE_TRADING'].values
    ticker = df['TICKER'].values
    position = df['position'].values
    pca_arr = df['PCA'].values

    ticker_arr = []
    date_start_arr = []
    date_end_arr = []
    pca_start_arr = []
    pca_end_arr = []

    for n in range(len(date_trading)):
        # print(n)
        if (n == 0):
            if (position[n] == 1):
                ticker_deal = ticker[n]
                date_start_deal = date_trading[n]
                pca_start_deal = pca_arr[n]
                ticker_arr.append(ticker_deal)
                date_start_arr.append(date_start_deal)
                pca_start_arr.append(pca_start_deal)
                # ticker_arr = np.array(ticker_arr, ticker_deal)
                # date_start_arr = np.array(date_start_arr, date_start_deal)
                # pca_start_arr = np.array(pca_start_arr, pca_start_deal)

        elif (n != 0):
            if (n == (len(date_trading) - 1)) and (position[n] == 1):
                date_end_deal = date_trading[n]
                pca_end_deal = pca_arr[n]
                date_end_arr.append(date_end_deal)
                pca_end_arr.append(pca_end_deal)
                
            elif (ticker[n] == ticker[n-1]):
                if (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 0) and (position[n-1] == 1):
                    date_end_deal = date_trading[n]
                    pca_end_deal = pca_arr[n]
                    date_end_arr.append(date_end_deal)  
                    pca_end_arr.append(pca_end_deal)

            elif (ticker[n] != ticker[n-1]):
                if (position[n-1] == 1) and ((position[n] == 0)):
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

                elif (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 1) and (position[n-1] == 1):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]

                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

    date_count = []

    for i in range(len(ticker_arr)):
        # date_count_deal = len([x for x in date_list if date_start_arr[i] < x <= date_end_arr[i]])
        # date_count_deal = date_list.index(date_end_arr[i]) - date_list.index(date_start_arr[i]) 
        date_count_deal = (np.where(date_list == date_end_arr[i])[0][0] if np.any(date_list == date_end_arr[i]) else -1) - (np.where(date_list == date_start_arr[i])[0][0] if np.any(date_list == date_start_arr[i]) else -1 )
        
        date_count.append(date_count_deal)

    deal_df['TICKER'] = ticker_arr
    deal_df['DATE_START'] = date_start_arr
    deal_df['DATE_END'] = date_end_arr
    deal_df['PRICE_START'] = pca_start_arr
    deal_df['PRICE_END'] = pca_end_arr
    deal_df['deal_return'] = deal_df['PRICE_END'] / deal_df['PRICE_START'] - 1
    deal_df['deal_length'] = date_count

    number_of_ticker_a_day = pd.DataFrame(df.groupby('DATE_TRADING')['position'].sum()).reset_index()
    number_of_ticker_a_day = number_of_ticker_a_day['position'].describe()
    deal_return = deal_df['deal_return'].describe()
    deal_length = deal_df['deal_length'].describe()

    pos_return_percentage = deal_df[deal_df['deal_return'] > 0]['TICKER'].count()/len(deal_df)
    pos_return_value = deal_df[deal_df['deal_return'] > 0]['deal_return'].mean()
    neg_return_value = deal_df[deal_df['deal_return'] < 0]['deal_return'].mean()
    kelly = -pos_return_percentage*pos_return_value/(neg_return_value*(1-pos_return_percentage))

    deal_df['YEAR'] = deal_df['DATE_START'].dt.year

    pos_return_by_year = deal_df[deal_df['deal_return'] > 0].groupby(['YEAR'])['deal_return'].describe().reset_index()
    pos_return_by_year.rename(columns= lambda x: x + '_pos', inplace= True)
    neg_return_by_year = deal_df[deal_df['deal_return'] < 0].groupby(['YEAR'])['deal_return'].describe().reset_index()
    neg_return_by_year.rename(columns= lambda x: x + '_neg', inplace= True)

    deal_length_pos_return_by_year = deal_df[deal_df['deal_return'] > 0].groupby(['YEAR'])['deal_length'].describe().reset_index()
    deal_length_pos_return_by_year.rename(columns= lambda x: x + '_pos', inplace= True)
    deal_length_neg_return_by_year = deal_df[deal_df['deal_return'] < 0].groupby(['YEAR'])['deal_length'].describe().reset_index()
    deal_length_neg_return_by_year.rename(columns= lambda x: x + '_neg', inplace= True)

    return_by_year = deal_df.groupby(['YEAR'])['deal_return'].describe().reset_index()
    deal_length_by_year = deal_df.groupby(['YEAR'])['deal_length'].describe().reset_index()

    return_by_year = pd.merge(return_by_year, pos_return_by_year, left_index= True, right_index= True)
    return_by_year = pd.merge(return_by_year, neg_return_by_year, left_index= True, right_index= True)
    return_by_year['pos_deal_percentage'] = return_by_year['count_pos'] / return_by_year['count']
    return_by_year[['pos_deal_percentage','mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']] = return_by_year[['pos_deal_percentage','mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']].applymap(lambda x: '{:.1%}'.format(x))

    deal_length_by_year = pd.merge(deal_length_by_year, deal_length_pos_return_by_year, left_index= True, right_index= True)
    deal_length_by_year = pd.merge(deal_length_by_year, deal_length_neg_return_by_year, left_index= True, right_index= True)
    deal_length_by_year['pos_deal_percentage'] = deal_length_by_year['count_pos'] / deal_length_by_year['count']
    deal_length_by_year[['pos_deal_percentage']] = deal_length_by_year[['pos_deal_percentage']].applymap('{:.1%}'.format)
    deal_length_by_year[['mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']] = deal_length_by_year[['mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']].applymap(lambda x: '{:.1f}'.format(x))
    
    print(f'Tỉ lệ deal thắng/thua {pos_return_percentage}/{1-pos_return_percentage}')
    print(f'Mức độ thắng của các deal thắng {pos_return_value}')
    print(f'Mức độ thua của các deal thua {neg_return_value}')
    print(f'Kelly {kelly}')

    print(f'Distribution return của tất cả các deal')
    display(deal_return)
    print(f'Distribution length của tất cả các deal')
    display(deal_length)
    print(f'Distribution số mã đạt position mỗi ngày')
    display(number_of_ticker_a_day)

    print('Đây là distribution return')
    display(return_by_year[['YEAR','count','pos_deal_percentage','mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']])

    print('Đây là distribution deal length')
    display(deal_length_by_year[['YEAR','count','pos_deal_percentage','mean','25%','50%','75%','mean_pos','25%_pos','50%_pos','75%_pos','mean_neg','25%_neg','50%_neg','75%_neg']])

    gr_df_tem = df.copy()

    quantile_df = gr_df_tem.groupby(['position'])['PCA-GR_1D-A_1D'].describe().reset_index()
    quantile_df_prod = gr_df_tem.groupby(['position'])['PCA-GR_1D-A_1D'].apply(gmean_ignore_nan).reset_index()
    quantile_df_prod[f'anlz_return'] = quantile_df_prod['PCA-GR_1D-A_1D']**250-1
    quantile_df = pd.merge(quantile_df, quantile_df_prod[['position', f'anlz_return']], how= 'left', on= 'position')
    quantile_df['mean_count_ticker'] = quantile_df['count'] / gr_df_tem['DATE_TRADING'].nunique()
    
    tem = gr_df_tem.groupby(['DATE_TRADING','position'])['PCA-GR_1D-A_1D'].mean().reset_index()
    tem_1 = tem.groupby(['position'])['PCA-GR_1D-A_1D'].prod().reset_index()
    tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
    quantile_df = pd.merge(quantile_df, tem_1[['position', 'eq1d_anlz_return']], how= 'left', on= 'position')
    
    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('position')['TICKER'].count().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('position')['TICKER'].count().reset_index()
    all = gr_df_tem.groupby('position')['TICKER'].count().reset_index()
    all['cnt_positive'] = pos['TICKER'] / all['TICKER']
    all['cnt_negative'] = neg['TICKER'] / all['TICKER']
    # quantile_df = pd.merge(quantile_df, all[['position','cnt_positive','cnt_negative']], how= 'left', on= 'position')

    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('position')['PCA-GR_1D-A_1D'].mean().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('position')['PCA-GR_1D-A_1D'].mean().reset_index()

    pos.rename(columns= {'PCA-GR_1D-A_1D': 'pos_mean_r1D'}, inplace= True)
    neg.rename(columns= {'PCA-GR_1D-A_1D': 'neg_mean_r1D'}, inplace= True)

    all = pd.merge(all[['position','cnt_positive','cnt_negative']], pos, how= 'left', on= 'position')
    all = pd.merge(all, neg, how= 'left', on= 'position')
    all['kelly'] = - all['cnt_positive'] * (1- all['pos_mean_r1D']) / (all['cnt_negative'] * (1-all['neg_mean_r1D']))

    display(quantile_df[['position','count','mean','std','anlz_return','mean_count_ticker','eq1d_anlz_return']])
    display(all)

def trading_to_nav_calculate_function(df, database_version):
    """là 1 function để phục vụ các function khác
        để tính toán nav_trading, đặc biệt trong tình huống hypothesis bị thay đổi theo hàm số"""
    index = df.index.values
    df_r1d = load_pca(database_version)
    indicator_list = ['PCA-GR_1D-A_1D']
    df_r1d = load_indicator_list(df_r1d, database_version, indicator_list)
    min_date = df['DATE_TRADING'].min()
    max_date = df['DATE_TRADING'].max()
    df_r1d = df_r1d[(df_r1d['DATE_TRADING'] >= min_date) & (df_r1d['DATE_TRADING'] <= max_date)]
    datetable = df_r1d.groupby('DATE_TRADING').agg({'TICKER': list, 'PCA-GR_1D-A_1D': list}).reset_index().reset_index()
    ticker_arr = datetable['TICKER'].values
    r1d_arr = datetable['PCA-GR_1D-A_1D'].values
    date_count = len(index)

    ticker_position_arr = df.stock_list.values
    nav_stock_to_nav_arr = df.nav_stock_to_nav_arr.values

    nav_total = [None] * date_count # nav_total, mỗi ngày 1 số
    number_of_stock = [None] * date_count # số mã trong danh mục, mỗi ngày 1 số
    # cash = [None] * date_count # cash_value, mỗi ngày 1 số
    max_assign = [None] * date_count # max_assign, mỗi ngày 1số

    in_arr = [None] * date_count # danh sách mã mới vào, array
    out_arr = [None] * date_count # danh sách mã  bị loại, array
    stay_arr = [None] * date_count # danh sách mã tiếp tục ở lại, array
    assign_arr = [None] * date_count # danh sách mã được assign, array

    assign_r1d_arr = [None] * date_count # PCA-GR_1D-A_1D của các mã được assign

    nav_stock_in_arr = [None] * date_count # nav_each_stock trong danh sách in, array
    nav_stock_out_arr = [None] * date_count # nav_each_stock trong danh sách out, array
    nav_stock_stay_diff_arr = [None] * date_count # chênh lệch giữa nav t0 của cổ phiếu và nav t-1 * pca_r1d_a1d, array
    nav_stock_assign_arr = [None] * date_count # nav_each_assign_stock , array
    nav_stock = [None] * date_count # nav_stock, number
    nav_buy_arr = [None] * date_count # nav_buy_value, number
    nav_sell_arr = [None] * date_count # nav_sell_value, number

    # nav_stock_to_nav_arr = [None] * date_count # tỉ trọng từng cổ phiếu trong danh mục, array
    nav_buy_to_nav = [None] * date_count # total_buy_to_nav, number
    nav_sell_to_nav = [None] * date_count # total_sell_to_nav, number
    # nav_buy_to_nav_arr = [None] * date_count # nav_buy_to_nav_each_stock, array
    # nav_sell_to_nav = [None] * date_count # total_sell_to_nav, number
    # nav_sell_to_nav_arr = [None] * date_count # nav_sell_to_nav_each_stock, array
    stock_buy_arr = [None] * date_count # danh sách các mã được buy, array
    stock_sell_arr = [None] * date_count # danh sách các mã được sell, array

    # ngày đầu tiên
    nav_total[0] = 1
    in_arr[0] = ticker_position_arr[0]
    out_arr[0] = []
    stay_arr[0] = []
    assign_arr[0] = in_arr[0]
    stock_buy_arr [0] = in_arr[0]
    stock_sell_arr[0] = []

    # list PCA-GR_1D-A_1D hàng ngày
    assign_r1d_arr[0] = [r1d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]

    # list các nav_stock ở các nhóm
    nav_stock_in_arr[0] = nav_stock_to_nav_arr[0]
    nav_stock_out_arr[0] = []
    nav_stock_stay_diff_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_diff_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    nav_buy_arr[0] = nav_stock_in_arr[0]
    nav_sell_arr[0] = []

    nav_buy_to_nav[0] = sum(nav_stock_in_arr[0])
    nav_sell_to_nav[0] = sum(nav_stock_out_arr[0])
    # nav_buy_to_nav_arr[0] = nav_stock_in_arr[0]
    # nav_sell_to_nav_arr[0] = []
    # nav_stock_assign_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_assign_arr[0]]

    # các chỉ tiêu quản lý cả danh mục
    # cash[0] = nav_total[0] - nav_stock[0]
    # nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]
    max_assign[0] = max([x for x in nav_stock_to_nav_arr[0]], default = 0)
    number_of_stock[0] = len(assign_arr[0])

    # Iteration through days
    i = 1
    while i < date_count:

        # các array liên quan đến danh sách cp stay - in - out
        in_arr[i] = [x for x in ticker_position_arr[i] if x not in set(assign_arr[i-1])]
        stay_arr[i] = [x for x in ticker_position_arr[i] if x in set(assign_arr[i-1])]
        out_arr[i] = [x for x in assign_arr[i-1] if x not in set(ticker_position_arr[i])]
        assign_arr[i] = ticker_position_arr[i]

        # các array liên quan đến return cp stay - in - out
        assign_r1d_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

        # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
        number_of_stock[i] = len(assign_arr[i])

        nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
        nav_gain_loss = [x * (y-1) for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
        nav_total[i] = sum(nav_gain_loss) + 1
        nav_stock_assign_to_nav_arr_last_day = [x / nav_total[i] for x in nav_stock_assign_arr_last_day]
        nav_stock_assign_arr[i] = nav_stock_to_nav_arr[i] 
        nav_stock_in_arr[i] = [nav_stock_assign_arr[i][assign_arr[i].index(j)] for j in in_arr[i]]
        nav_stock_stay_diff_arr[i] = [nav_stock_assign_arr[i][assign_arr[i].index(j)] - nav_stock_assign_to_nav_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
        
        nav_stock_out_arr[i] = [-1 * nav_stock_assign_to_nav_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]

        nav_buy_arr[i] = nav_stock_in_arr[i] + [x for x in nav_stock_stay_diff_arr[i] if x > 0]
        nav_sell_arr[i] = nav_stock_out_arr[i] + [x for x in nav_stock_stay_diff_arr[i] if x < 0]

        nav_stock[i] = sum(nav_stock_assign_arr[i])
        # cash[i] = nav_total[i] - nav_stock[i]
        # nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]
        max_assign[i] = max([x for x in nav_stock_assign_arr[i]], default = 0)
        nav_buy_to_nav[i] = sum(nav_buy_arr[i]) / nav_total[i]
        nav_sell_to_nav[i] = sum(nav_sell_arr[i]) / nav_total[i]
        # nav_buy_to_nav_arr[i] = [x/nav_total[i] for x in nav_buy_arr[i]]
        # nav_sell_to_nav_arr[i] = [x/nav_total[i] for x in nav_sell_arr[i]]
        stock_buy_arr[i] = in_arr[i] + [stay_arr[i][j] for j in range(len(nav_stock_stay_diff_arr[i])) if nav_stock_stay_diff_arr[i][j] > 0]
        stock_sell_arr[i] = out_arr[i] + [stay_arr[i][j] for j in range(len(nav_stock_stay_diff_arr[i])) if nav_stock_stay_diff_arr[i][j] < 0]
        # nav_stock_assign_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_assign_arr[i]]
        
        i = i + 1

    df['stock_buy_arr'] = stock_buy_arr
    df['nav_buy_to_nav_arr'] = nav_buy_arr
    df['nav_buy_to_nav'] = nav_buy_to_nav

    df['stock_sell_arr'] = stock_sell_arr
    df['nav_sell_to_nav_arr'] = nav_sell_arr
    df['nav_sell_to_nav'] = nav_sell_to_nav

    df['ticker_count'] = number_of_stock
    df['max_assign'] = max_assign

    return df

def assign_slot_hai_v3(df, max_slot, indicator_priority, date_start, date_end, fee = True):
    max_slot = int(max_slot)
    df1 = df[['DATE_TRADING', 'TICKER', 'position', indicator_priority, 'PCA-GR_1D', 'PCA-GR_1D-A_1D']].copy()
    df1.sort_values(by = ['DATE_TRADING',indicator_priority],ascending = [True,False], inplace=True)
    date_list = sorted(df1[(df1['DATE_TRADING'] >= date_start) & (df1['DATE_TRADING'] < date_end)]['DATE_TRADING'].unique())
    number_of_date_list = len(date_list)

    datetable_2 = df1[(df1['DATE_TRADING'] >= date_start) & (df1['DATE_TRADING'] <= date_end)].groupby('DATE_TRADING').agg({'TICKER': lambda x: x.tolist(), 'PCA-GR_1D-A_1D': lambda x: x.tolist()}).reset_index()
    datetable_2["TICKER"] = datetable_2["TICKER"].apply(lambda x: [] if x != x else x)
    datetable_2["PCA-GR_1D-A_1D"] = datetable_2["PCA-GR_1D-A_1D"].apply(lambda x: [] if x != x else x)
    ticker_list_arr = datetable_2["TICKER"].values
    r1d_arr = datetable_2["PCA-GR_1D-A_1D"].values
    datetable_2.drop('TICKER', axis = 1, inplace = True)

    datetable = df1[df1['position'] == 1].groupby('DATE_TRADING').agg({'TICKER': lambda x: x.tolist()}).reset_index()
    datetable = pd.merge(datetable_2, datetable, how = 'left', on = 'DATE_TRADING')
    datetable["TICKER"] = datetable["TICKER"].apply(lambda x: [] if x != x else x)

    eod_p_arr = datetable["TICKER"].values

    # list các danh sách mã
    in_arr = [None] * number_of_date_list # danh sách các mã mới xuất hiện trong danh sách có position
    out_arr = [None] * number_of_date_list # danh sách các mã rời khỏi danh sách có position
    stay_arr = [None] * number_of_date_list # danh sách các mã tiếp tục ở trong danh sách có position
    assign_arr = [None] * number_of_date_list # danh sách các mã được assign
    waiting_arr = [None] * number_of_date_list # danh sách các mã có position nhưng không được assign

    # list PCA-GR_1D-A_1D hàng ngày
    assign_r1d_arr = [None] * number_of_date_list # PCA-GR_1D-A_1D của các mã được assign

    # list các nav_stock ở các nhóm
    nav_stock_in_arr = [None] * number_of_date_list # nav_stock của các mã mới trong danh sách, mỗi ngày là 1 array
    nav_stock_out_arr = [None] * number_of_date_list # nav_stock của các mã out trong danh sách, mỗi ngày là 1 array
    nav_stock_stay_arr = [None] * number_of_date_list # nav_stock của các mã vẫn ở trong danh sách, mỗi ngày là 1 array
    nav_stock_assign_arr = [None] * number_of_date_list # nav_stock của các mã được assign, mỗi ngày là 1 array
    nav_stock_assign_to_nav_arr = [None] * number_of_date_list # nav_stock_each_stock/nav, mỗi ngày 1 array
    nav_stock = [None] * number_of_date_list # nav_stock tổng của các mã được assign, mỗi ngày là 1 con số

    stock_buy_arr = [None] * number_of_date_list # danh sách các mã được mua, mỗi ngày 1 array
    stock_sell_arr = [None] * number_of_date_list # danh sách các mã được bán, mỗi ngày 1 array
    nav_stock_to_nav = [None] * number_of_date_list # tỉ trọng nav_stock/nav, mỗi ngày 1 con số
    nav_buy_to_nav_arr = [None] * number_of_date_list # tỉ trọng nav_buy_each_stock/nav, mỗi ngày 1 array
    nav_buy_to_nav = [None] * number_of_date_list # giá trị mua/nav, mỗi ngày 1 con số
    nav_sell_to_nav_arr = [None] * number_of_date_list # tỉ trọng nav_sell_each_stock/nav, mỗi ngày 1 array
    nav_sell_to_nav = [None] * number_of_date_list # giá trị bán/nav, mỗi ngày 1 con số
    
    # các chỉ tiêu quản lý cả danh mục
    nav_total = [None] * number_of_date_list # giá trị nav_total, mỗi ngày 1 con số
    number_of_stock = [None] * number_of_date_list # số cổ phiếu mỗi ngày, mỗi ngày 1 con số
    cash = [None] * number_of_date_list # cash_value, mỗi ngày 1 con số
    max_assign = [None] * number_of_date_list # max_assign của 1 cổ phiếu, mỗi ngày 1 con số

    # ngày đầu
    out_arr[0] = []
    stay_arr[0] = []
    waiting_arr[0] = [x for x in eod_p_arr[0] if x not in set(stay_arr[0])]
    in_arr[0] = eod_p_arr[0] if len(eod_p_arr[0]) < max_slot else eod_p_arr[0][:max_slot]
    assign_arr[0] = in_arr[0] + stay_arr[0]

    assign_r1d_arr[0] = [r1d_arr[0][ticker_list_arr[0].index(j)] for j in assign_arr[0]]

    nav_total[0] = 1
    number_of_stock[0] = len(in_arr[0])

    nav_stock_in_arr[0] = [nav_total[0]/max_slot for _ in range(len(in_arr[0]))]
    nav_stock_out_arr[0] = []
    nav_stock_stay_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    nav_buy_to_nav[0] = sum(nav_stock_in_arr[0])
    nav_buy_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_in_arr[0]]
    nav_sell_to_nav[0] = sum(nav_stock_out_arr[0])
    nav_sell_to_nav_arr[0] = []
    nav_stock_assign_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_assign_arr[0]]
    stock_buy_arr[0] = in_arr[0]
    stock_sell_arr[0] = out_arr[0]

    cash[0] = nav_total[0] - nav_stock[0]
    nav_stock_to_nav[0] = sum(nav_stock_assign_to_nav_arr[0]) / nav_total[0]
    max_assign[0] = max([x for x in nav_stock_assign_to_nav_arr[0]], default = 0)

    i = 1
    while i < len(date_list):
        # các array liên quan đến danh sách cp stay - in - out
        stay_arr[i] = [x for x in eod_p_arr[i] if x in set(assign_arr[i-1])]
        out_arr[i] = [x for x in assign_arr[i-1] if x not in set(eod_p_arr[i])]
        waiting_arr[i] = [x for x in eod_p_arr[i] if x not in set(assign_arr[i-1])]
        
        if len(stay_arr[i]) < max_slot:
            in_arr[i] = waiting_arr[i][:max_slot - len(stay_arr[i])]
        else:
            in_arr[i] = []
        
        assign_arr[i] = in_arr[i] + stay_arr[i]

        # các array liên quan đến return cp stay - in - out
        assign_r1d_arr[i] = [r1d_arr[i][ticker_list_arr[i].index(j)] for j in assign_arr[i]]

        # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
        number_of_stock[i] = len(assign_arr[i])

        nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
        nav_stock_stay_arr[i] = [nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
        nav_stock_out_arr[i] = [-1 * nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]
        nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
        nav_stock_in_arr[i] = [nav_total[i]/max_slot for _ in range(len(in_arr[i]))]

        nav_stock_assign_arr[i] = nav_stock_in_arr[i] + nav_stock_stay_arr[i]
        nav_stock[i] = sum(nav_stock_assign_arr[i])
        cash[i] = nav_total[i] - nav_stock[i]
        nav_stock_to_nav[i] = sum(nav_stock_assign_arr[i]) / nav_total[i]
        nav_stock_assign_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_assign_arr[i]]
        max_assign[i] = max([x for x in nav_stock_assign_to_nav_arr[i]], default = 0)
        nav_buy_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_in_arr[i]]
        nav_buy_to_nav[i] = sum(nav_stock_in_arr[i])/ nav_total[i]
        nav_sell_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_out_arr[i]]
        nav_sell_to_nav[i] = sum(nav_stock_out_arr[i])/ nav_total[i]
        
        stock_buy_arr[i] = in_arr[i]
        stock_sell_arr[i] = out_arr[i]

        i = i + 1
        
    df_assign= {'DATE_TRADING': date_list, 
                'stock_list': assign_arr, 
                'acc_return': nav_total, 
                'cash': cash, 
                'ticker_count': number_of_stock,
                'nav_stock': nav_stock, 
                'max_assign': max_assign, 
                'nav_buy_to_nav': nav_buy_to_nav, 
                'nav_buy_to_nav_arr': nav_buy_to_nav_arr,
                'nav_sell_to_nav': nav_sell_to_nav, 
                'nav_sell_to_nav_arr': nav_sell_to_nav_arr,
                'nav_stock_to_nav_arr': nav_stock_assign_to_nav_arr
                }
    df_assign = pd.DataFrame(df_assign)
    df_assign['daily_return'] = df_assign['acc_return'] / df_assign['acc_return'].shift(1) - 1
    df_assign['daily_return'].fillna(value = 0, inplace = True)
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']
    if fee == True:
        df_assign = fee_create(df_assign)
    elif fee == False:
        df_assign = fee_create(df_assign, fee_buy= 0, fee_sell= 0)
    return df_assign

def assign_slot_hai_v5(df, max_slot, nav_slot, indicator_priority, date_start, date_end, fee = True):
    """ assign khá giống haiv3, với nav_slot chưa chắc bằng 1 / max_slot"""
    max_slot = int(max_slot)
    df1 = df[['DATE_TRADING', 'TICKER', 'position', indicator_priority, 'PCA-GR_1D', 'PCA-GR_1D-A_1D']].copy()
    df1.sort_values(by = ['DATE_TRADING',indicator_priority],ascending = [True,False], inplace=True)
    date_list = sorted(df1[(df1['DATE_TRADING'] >= date_start) & (df1['DATE_TRADING'] < date_end)]['DATE_TRADING'].unique())
    number_of_date_list = len(date_list)

    datetable_2 = df1[(df1['DATE_TRADING'] >= date_start) & (df1['DATE_TRADING'] <= date_end)].groupby('DATE_TRADING').agg({'TICKER': lambda x: x.tolist(), 'PCA-GR_1D-A_1D': lambda x: x.tolist()}).reset_index()
    datetable_2["TICKER"] = datetable_2["TICKER"].apply(lambda x: [] if x != x else x)
    datetable_2["PCA-GR_1D-A_1D"] = datetable_2["PCA-GR_1D-A_1D"].apply(lambda x: [] if x != x else x)
    ticker_list_arr = datetable_2["TICKER"].values
    r1d_arr = datetable_2["PCA-GR_1D-A_1D"].values
    datetable_2.drop('TICKER', axis = 1, inplace = True)

    datetable = df1[df1['position'] == 1].groupby('DATE_TRADING').agg({'TICKER': lambda x: x.tolist()}).reset_index()
    datetable = pd.merge(datetable_2, datetable, how = 'left', on = 'DATE_TRADING')
    datetable["TICKER"] = datetable["TICKER"].apply(lambda x: [] if x != x else x)

    eod_p_arr = datetable["TICKER"].values

    # list các danh sách mã
    in_arr = [None] * number_of_date_list # danh sách các mã mới xuất hiện trong danh sách có position
    out_arr = [None] * number_of_date_list # danh sách các mã rời khỏi danh sách có position
    stay_arr = [None] * number_of_date_list # danh sách các mã tiếp tục ở trong danh sách có position
    assign_arr = [None] * number_of_date_list # danh sách các mã được assign
    waiting_arr = [None] * number_of_date_list # danh sách các mã có position nhưng không được assign

    # list PCA-GR_1D-A_1D hàng ngày
    assign_r1d_arr = [None] * number_of_date_list # PCA-GR_1D-A_1D của các mã được assign

    # list các nav_stock ở các nhóm
    nav_stock_in_arr = [None] * number_of_date_list # nav_stock của các mã mới trong danh sách, mỗi ngày là 1 array
    nav_stock_out_arr = [None] * number_of_date_list # nav_stock của các mã out trong danh sách, mỗi ngày là 1 array
    nav_stock_stay_arr = [None] * number_of_date_list # nav_stock của các mã vẫn ở trong danh sách, mỗi ngày là 1 array
    nav_stock_assign_arr = [None] * number_of_date_list # nav_stock của các mã được assign, mỗi ngày là 1 array
    nav_stock_assign_to_nav_arr = [None] * number_of_date_list # nav_stock_each_stock/nav, mỗi ngày 1 array
    nav_stock = [None] * number_of_date_list # nav_stock tổng của các mã được assign, mỗi ngày là 1 con số

    stock_buy_arr = [None] * number_of_date_list # danh sách các mã được mua, mỗi ngày 1 array
    stock_sell_arr = [None] * number_of_date_list # danh sách các mã được bán, mỗi ngày 1 array
    nav_stock_to_nav = [None] * number_of_date_list # tỉ trọng nav_stock/nav, mỗi ngày 1 con số
    nav_buy_to_nav_arr = [None] * number_of_date_list # tỉ trọng nav_buy_each_stock/nav, mỗi ngày 1 array
    nav_buy_to_nav = [None] * number_of_date_list # giá trị mua/nav, mỗi ngày 1 con số
    nav_sell_to_nav_arr = [None] * number_of_date_list # tỉ trọng nav_sell_each_stock/nav, mỗi ngày 1 array
    nav_sell_to_nav = [None] * number_of_date_list # giá trị bán/nav, mỗi ngày 1 con số
    
    # các chỉ tiêu quản lý cả danh mục
    nav_total = [None] * number_of_date_list # giá trị nav_total, mỗi ngày 1 con số
    number_of_stock = [None] * number_of_date_list # số cổ phiếu mỗi ngày, mỗi ngày 1 con số
    cash = [None] * number_of_date_list # cash_value, mỗi ngày 1 con số
    max_assign = [None] * number_of_date_list # max_assign của 1 cổ phiếu, mỗi ngày 1 con số

    # ngày đầu
    out_arr[0] = []
    stay_arr[0] = []
    waiting_arr[0] = [x for x in eod_p_arr[0] if x not in set(stay_arr[0])]
    in_arr[0] = eod_p_arr[0] if len(eod_p_arr[0]) < max_slot else eod_p_arr[0][:max_slot]
    assign_arr[0] = in_arr[0] + stay_arr[0]

    assign_r1d_arr[0] = [r1d_arr[0][ticker_list_arr[0].index(j)] for j in assign_arr[0]]

    nav_total[0] = 1
    number_of_stock[0] = len(in_arr[0])

    nav_stock_in_arr[0] = [nav_total[0] * nav_slot for _ in range(len(in_arr[0]))]
    nav_stock_out_arr[0] = []
    nav_stock_stay_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    nav_buy_to_nav[0] = sum(nav_stock_in_arr[0])
    nav_buy_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_in_arr[0]]
    nav_sell_to_nav[0] = sum(nav_stock_out_arr[0])
    nav_sell_to_nav_arr[0] = []
    nav_stock_assign_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_assign_arr[0]]
    stock_buy_arr[0] = in_arr[0]
    stock_sell_arr[0] = out_arr[0]

    cash[0] = nav_total[0] - nav_stock[0]
    nav_stock_to_nav[0] = sum(nav_stock_assign_to_nav_arr[0]) / nav_total[0]
    max_assign[0] = max([x for x in nav_stock_assign_to_nav_arr[0]], default = 0)

    i = 1
    while i < len(date_list):
        # các array liên quan đến danh sách cp stay - in - out
        stay_arr[i] = [x for x in eod_p_arr[i] if x in set(assign_arr[i-1])]
        out_arr[i] = [x for x in assign_arr[i-1] if x not in set(eod_p_arr[i])]
        waiting_arr[i] = [x for x in eod_p_arr[i] if x not in set(assign_arr[i-1])]
        
        if len(stay_arr[i]) < max_slot:
            in_arr[i] = waiting_arr[i][:max_slot - len(stay_arr[i])]
        else:
            in_arr[i] = []
        
        assign_arr[i] = in_arr[i] + stay_arr[i]

        # các array liên quan đến return cp stay - in - out
        assign_r1d_arr[i] = [r1d_arr[i][ticker_list_arr[i].index(j)] for j in assign_arr[i]]

        # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
        number_of_stock[i] = len(assign_arr[i])

        nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
        nav_stock_stay_arr[i] = [nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
        nav_stock_out_arr[i] = [-1 * nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]
        nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
        nav_stock_in_arr[i] = [nav_total[i] * nav_slot for _ in range(len(in_arr[i]))]

        nav_stock_assign_arr[i] = nav_stock_in_arr[i] + nav_stock_stay_arr[i]
        nav_stock[i] = sum(nav_stock_assign_arr[i])
        cash[i] = nav_total[i] - nav_stock[i]
        nav_stock_to_nav[i] = sum(nav_stock_assign_arr[i]) / nav_total[i]
        nav_stock_assign_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_assign_arr[i]]
        max_assign[i] = max([x for x in nav_stock_assign_to_nav_arr[i]], default = 0)
        nav_buy_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_in_arr[i]]
        nav_buy_to_nav[i] = sum(nav_stock_in_arr[i])/ nav_total[i]
        nav_sell_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_out_arr[i]]
        nav_sell_to_nav[i] = sum(nav_stock_out_arr[i])/ nav_total[i]
        
        stock_buy_arr[i] = in_arr[i]
        stock_sell_arr[i] = out_arr[i]

        i = i + 1
        
    df_assign= {'DATE_TRADING': date_list, 
                'stock_list': assign_arr, 
                'acc_return': nav_total, 
                'cash': cash, 
                'ticker_count': number_of_stock,
                'nav_stock': nav_stock, 
                'max_assign': max_assign, 
                'nav_buy_to_nav': nav_buy_to_nav, 
                'nav_buy_to_nav_arr': nav_buy_to_nav_arr,
                'nav_sell_to_nav': nav_sell_to_nav, 
                'nav_sell_to_nav_arr': nav_sell_to_nav_arr,
                'nav_stock_to_nav_arr': nav_stock_assign_to_nav_arr
                }
    df_assign = pd.DataFrame(df_assign)
    df_assign['daily_return'] = df_assign['acc_return'] / df_assign['acc_return'].shift(1) - 1
    df_assign['daily_return'].fillna(value = 0, inplace = True)
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']
    if fee == True:
        df_assign = fee_create(df_assign)
    elif fee == False:
        df_assign = fee_create(df_assign, fee_buy= 0, fee_sell= 0)
    return df_assign

def assign_slot_haiv3_from_hai(position, indicator, dataframe, slot, holdtime=2, evl_begin='2011-01-01', evl_end='2022-12-31',margin = None):
    """
    position: tên của chuỗi position
    indicator: tên của indicator ưu tiên
    dataframe: tên của dataframe chứa position
    group: nhóm groupby, default là "TICKER"
    holdtime: thời gian nắm giữ tối thiểu
    evl_begin: ngày đầu tiên chạy hypothesis
    evl_end: ngày cuối cùng chạy hypothesis
    margin (str,int,float): tên cột hệ số margin cho mỗi mã mỗi ngày, hoặc một hệ số margin chung cho toàn thời gian
    !!!
    - phải có các cột :"TICKER","PCA-GR_1D-A_1D","DATE_TRADING" thì mới chạy được
    - đã xử lý vấn đề T+
    !!!
    """
    # xử lý n/a và cắt theo khung thời gian muốn chạy hypothesis
    df1 = dataframe.copy() # copy từ dataframe gốc
    df1['PCA-GR_1D'] = df1.groupby('TICKER')['PCA-GR_1D-A_1D'].shift(1) # Tính PCA-GR_1D từ PCA-GR_1D-A_1D
    df1['PCA-GR_1D'].fillna(1, inplace=True) # fillna
    df1 = df1[(df1['DATE_TRADING'] >= evl_begin) &
              ((df1['DATE_TRADING'] <= evl_end))] # cắt date_trading

    margin_rate = margin*1 if margin is not None else 1 # tại sao phải nhân 1?
    if isinstance(margin, (int, float)): # check xem datatype margin có phải là int hoặc float ko? nếu không thì tạo 1 cột tạm
        df1['margin_temp_column'] = margin
        margin = 'margin_temp_column'

    # tạo bảng đã sort mã/ngày theo thứ tự của indicator ưu tiên
    df2 = df1.copy() 
    df2.sort_values(by=['DATE_TRADING', indicator],
                    ascending=False, inplace=True)

    # define các list mã sẽ sử dụng MỖI NGÀY
    datetable = df2.groupby("DATE_TRADING")[
        "TICKER"].count().to_frame().reset_index() # đếm số Ticker tại mỗi ngày, rồi chuyển nó thành dataframe
    EOD_P_array = df2[df2[position] == 1].groupby(
        'DATE_TRADING')['TICKER'].agg(lambda x: x.tolist()).to_frame().reset_index() # chuyển hết tất cả các mã có position hàng ngày vào array EOD_P_array
    datetable.drop('TICKER',axis=1,inplace=True) # chỉ giữ lại cột DATE_TRADING và số cột
    datetable = datetable.merge(EOD_P_array,how='left',on='DATE_TRADING') # merge bảng có số ticker và ticker dạng list lại để lấy những ngày ko có mã nào đạt position
    datetable["TICKER"] = datetable["TICKER"].apply(lambda x: [] if x != x else x) # chuyển nan thành []
    EOD_P_array  = datetable["TICKER"].copy() # lấy lại array chỉ toàn ticker dạng tolist
    EOD_P_array.index = datetable["DATE_TRADING"] #lấy index cho array bằng số ngày giao dịch

    BOD_A_array = list(EOD_P_array) # đầu ngày có assign
    PnotBOD_A_array = list(EOD_P_array) # có position nhưng ko có trong danh sách được assign đầu ngày (nhóm in)
    BOD_AnotP_array = list(EOD_P_array) # đầu ngày có assign nhưng cuối ngày ko có position (nhóm bị out)
    EOD_A_array = list(EOD_P_array) # cuối ngày có assign
    # ngày đầu tiên của các list mã
    BOD_A_array[0] = [] # đầu ngày ko có mã nào
    PnotBOD_A_array[0] = EOD_P_array[0] # watchlist của ngày đầu tiên, ko được assign
    BOD_AnotP_array[0] = [] #đầu ngày có assign nhưng cuối ngày ko có position (nhóm bị out)
    EOD_A_array[0] = PnotBOD_A_array[0] if len(
        PnotBOD_A_array[0]) < slot else PnotBOD_A_array[0][:slot] # chỉ lấy số mã bằng đúng slot còn lại
    # các ngày sau đó của các list mã
    n = 1
    while n < len(EOD_P_array): # nếu n < số ngày trading thì mới dùng
        BOD_A_array[n] = EOD_A_array[n-1] #đầu ngày hôm nay bằng cuối ngày hôm trc
        PnotBOD_A_array[n] = [x for x in EOD_P_array[n]
                              if x not in set(BOD_A_array[n])] #thuộc nhóm có position nhưng ko thuộc nhóm đầu ngày có assign
        # dòng dưới này đã xử lý cả vấn đề T+
        if n > holdtime:
            BOD_AnotP_array[n] = [x for x in BOD_A_array[n] if x not in set(
                EOD_P_array[n]) and False not in [x in set(EOD_A_array[n-m]) for m in range(1, holdtime+1)]] #nếu n lớn hơn holdtime, thì nhóm cổ phiếu out sẽ là x thuộc nhóm 1) đầu ngày có assign mà 2) cuối ngày ko có position và 3) phải thuộc nhóm cuối ngày có assign cách đây n - m, với m chạy từ 1 đến holdtime + 1
        else:
            BOD_AnotP_array[n] = [x for x in BOD_A_array[n] if x not in set(
                EOD_P_array[n]) and False not in [x in set(EOD_A_array[n-m]) for m in range(1, n)]] #nếu n <= holdtime, thì nhóm cổ phiếu out sẽ là x thuộc nhóm 1) đầu ngày có assign mà 2) cuối ngày ko có position và 3) phải thuộc nhóm cuối ngày có assign cách đây n - m, với m chạy từ 1 đến holdtime
        if len(BOD_A_array[n]) < slot:
            EOD_A_array[n] = [x for x in BOD_A_array[n] if x not in set(
                BOD_AnotP_array[n])] + PnotBOD_A_array[n][:slot-len(BOD_A_array[n])] #nếu đầu ngày đc assign có số mã nhỏ hơn slot thì cuối ngày = đầu ngày và thêm mã trong watchlist với mã có index từ 0 đến (slot - số mã đang có đầu ngày)
        else:
            EOD_A_array[n] = [x for x in BOD_A_array[n]
                              if x not in set(BOD_AnotP_array[n])] # còn nếu số mã = slot thì đương nhiên đầu ngày bằng cuối ngày
        n = n + 1

    # tạo table để tí nữa explode ngược bảng list mã mỗi ngày về bảng full (đánh dấu Assign nữa)
    EOD_table = EOD_P_array.to_frame(name='EOD_P').reset_index()
    EOD_table['TICKER'] = EOD_A_array
    EOD_table.drop(columns=['EOD_P'], inplace=True)
    EOD_table['A'] = 1

    EOD_exploded_table = EOD_table.explode('TICKER') #lấy danh sách các mã có assign

    # xử lý trên bảng full để lấy các list return/ngày tương ứng với các list mã/ngày
    df1 = pd.merge(df1, EOD_exploded_table, on=[
                   'DATE_TRADING', 'TICKER'], how='left')
    df1['POS_BOD_A'] = df1.groupby('TICKER')['A'].shift(1) # để đánh dấu những ngày có hưởng trọn return
    df_return_cal = df1[df1['A'] == 1].groupby(
        "DATE_TRADING")['TICKER'].agg(lambda x: x.tolist()).reset_index() # lại tạo list cho các ticker theo ngày
    df_return_cal.rename(columns={'TICKER': 'ACHANGE_TICKER'}, inplace=True) # tổi tên list thành assign ticker
    df_return_cal_2 = df1[df1['POS_BOD_A'] == 1].groupby(
        "DATE_TRADING")[['TICKER', 'PCA-GR_1D']].agg(lambda x: x.tolist()).reset_index() # tạo thêm 1 dataframe với list ticker và return 1D
    df_return_cal_2.rename(columns={'TICKER': 'BCHANGE_TICKER'}, inplace=True)
    df_return_cal = pd.merge(df_return_cal, df_return_cal_2, on=[
        'DATE_TRADING'], how='left') # merge 2 bảng lại với nhau
    # fill na các ngày empty để tránh error
    df_return_cal["ACHANGE_TICKER"] = df_return_cal["ACHANGE_TICKER"].fillna(
        "").apply(list)
    df_return_cal["BCHANGE_TICKER"] = df_return_cal["BCHANGE_TICKER"].fillna(
        "").apply(list)
    df_return_cal["PCA-GR_1D"] = df_return_cal["PCA-GR_1D"].fillna("").apply(list)
    # tính toán return và assign mỗi ngày
    ACHANGE_ticker = list(df_return_cal['ACHANGE_TICKER'].copy())
    ACHANGE_ticker_save = copy.deepcopy(ACHANGE_ticker)
    BCHANGE_ticker = list(df_return_cal['BCHANGE_TICKER'].copy())
    PI1D = list(df_return_cal['PCA-GR_1D'].copy())
    BCHANGE_assign = list(df_return_cal['PCA-GR_1D'].copy())
    ACHANGE_assign = list(ACHANGE_ticker.copy())
    PI1D_Portfolio = list(df_return_cal['PCA-GR_1D'].copy())
    if margin is not None:
        margin_list = df1[['DATE_TRADING','TICKER',f'{margin}']].groupby('DATE_TRADING')[['TICKER', f'{margin}']].apply(lambda x: x.set_index('TICKER').to_dict()[f'{margin}']).reset_index(name='margin_list')
        margin_list = list(margin_list['margin_list'])
    # ngày đầu tiên
    BCHANGE_assign[0] = [0]
    PI1D_Portfolio[0] = 1
    # if len(ACHANGE_ticker[0])>=slot:
    #     ACHANGE_ticker[0] = ACHANGE_ticker[0][:slot]
    #     ACHANGE_assign[0] = [1/slot]*slot
    #     BCHANGE_ticker[1] = ACHANGE_ticker[0].copy()
    #     PCA-GR_1D[1] = PCA-GR_1D[1][:slot]
    # else:
    #     ACHANGE_assign[0] = [1/slot]*len(ACHANGE_ticker[0])
    
    if margin is not None:
        ACHANGE_assign[0] = [(1/slot)*margin_list[0][ticker] if ticker in margin_list[0] else 1/slot if isinstance(margin, (str)) else margin_rate/slot for ticker in ACHANGE_ticker[0]]
    else:
        ACHANGE_assign[0] = [1/slot]*len(ACHANGE_ticker[0])
    # các ngày sau đó
    n = 1
    while n < len(df_return_cal['DATE_TRADING']):
        PI1D_Portfolio[n] = sum([x * (y-1)
                                 for x, y in zip(ACHANGE_assign[n-1], PI1D[n])])+1
        BCHANGE_assign[n] = [
            x * y for x, y in zip(PI1D[n], [item * (1/PI1D_Portfolio[n]) for item in ACHANGE_assign[n-1]])]
        m = 0
        while m < len(ACHANGE_ticker[n]):
            indexer = str(ACHANGE_ticker[n][m])
            if ACHANGE_ticker[n][m] in BCHANGE_ticker[n]:
                ACHANGE_assign[n][m] = BCHANGE_assign[n][BCHANGE_ticker[n].index(
                    indexer)]
            elif margin is not None:
                ACHANGE_assign[n][m] = margin_list[n][indexer]/slot if indexer in margin_list[n] else 1/slot if isinstance(margin, (str)) else margin_rate/slot
            else:
                ACHANGE_assign[n][m] = 1/slot
            m = m+1
        n = n+1

    # explode ngược lại thành bảng full và lấy cột assign cuối ngày lắp vào dataframe mong muốn
    df_return_cal['ACHANGE_assign'] = ACHANGE_assign
    df_return_cal['ACHANGE_TICKER'] = ACHANGE_ticker_save

    df_return_cal = df_return_cal[[
        "DATE_TRADING", "ACHANGE_TICKER", "ACHANGE_assign"]]
    
    df_return_cal = df_return_cal.set_index(
        ['DATE_TRADING']).apply(pd.Series.explode).reset_index()
    df_return_cal.rename(columns={"ACHANGE_TICKER": "TICKER"}, inplace=True)
    merged_df = pd.merge(dataframe, df_return_cal, on=[
        'DATE_TRADING', 'TICKER'], how='left')
    merged_df.fillna(0, inplace=True)
    dataframe[f"ss({position},{slot},{holdtime},{dataframe.columns.get_loc(indicator)})"] = merged_df["ACHANGE_assign"]
    return f"ss({position},{slot},{holdtime},{dataframe.columns.get_loc(indicator)})"

def assign_equal_rebalance(df, time_groupby, date_start, date_end, database_version = 29, stock_break = False, fee = True):
    
    # Preprocess data
    date_count_ref = load_date_count_ref(database_version)
    df_tem = df.copy()
    df_tem = df_tem[(df_tem['DATE_TRADING'] >= date_start) & (df_tem['DATE_TRADING'] < date_end)]
    df_tem = df_tem.reset_index()
    datetable = df_tem.groupby('DATE_TRADING').agg({'TICKER': list, 'PCA-GR_1D-A_1D': list}).reset_index().reset_index()
    datetable.rename(columns = {'index':'date_trading_count'}, inplace = True)
    date_count = len(datetable.index.values)
    ticker_arr = datetable['TICKER'].values
    r1d_arr = datetable['PCA-GR_1D-A_1D'].values

    datetable_2 = df_tem[df_tem['position'] == 1].groupby('DATE_TRADING')['TICKER'].apply(list).reset_index()
    datetable_2 = pd.merge(datetable[['DATE_TRADING','date_trading_count']], datetable_2, how= 'left', on= 'DATE_TRADING')
    datetable_2 = pd.merge(datetable_2, date_count_ref, how= 'left', on= 'DATE_TRADING')
    datetable_2["TICKER"] = datetable_2["TICKER"].apply(lambda x: [] if x != x else x)

    ticker_position_arr = datetable_2["TICKER"].values
    month_arr = datetable_2["MONTH"].values

    # Metrics initialization
    nav_total = [None] * date_count # nav_total, mỗi ngày 1 số
    number_of_stock = [None] * date_count # số mã trong danh mục, mỗi ngày 1 số
    cash = [None] * date_count # cash_value, mỗi ngày 1 số
    max_assign = [None] * date_count # max_assign, mỗi ngày 1số

    in_arr = [None] * date_count # danh sách mã mới vào, array
    out_arr = [None] * date_count # danh sách mã  bị loại, array
    stay_arr = [None] * date_count # danh sách mã tiếp tục ở lại, array
    assign_arr = [None] * date_count # danh sách mã được assign, array

    assign_r1d_arr = [None] * date_count # PCA-GR_1D-A_1D của các mã được assign

    nav_stock_in_arr = [None] * date_count # nav_each_stock trong danh sách in, array
    nav_stock_out_arr = [None] * date_count # nav_each_stock trong danh sách out, array
    nav_stock_stay_diff_arr = [None] * date_count # chênh lệch giữa nav t0 của cổ phiếu và nav t-1 * pca_r1d_a1d, array
    nav_stock_assign_arr = [None] * date_count # nav_each_assign_stock , array
    nav_stock = [None] * date_count # nav_stock, number
    nav_buy_arr = [None] * date_count # nav_buy_value, number
    nav_sell_arr = [None] * date_count # nav_sell_value, number
    nav_stock_to_nav_arr = [None] * date_count # tỉ trọng từng cổ phiếu trong danh mục, array
    nav_buy_to_nav = [None] * date_count # total_buy_to_nav, number
    nav_buy_to_nav_arr = [None] * date_count # nav_buy_to_nav_each_stock, array
    nav_sell_to_nav = [None] * date_count # total_sell_to_nav, number
    nav_sell_to_nav_arr = [None] * date_count # nav_sell_to_nav_each_stock, array
    stock_buy_arr = [None] * date_count # danh sách các mã được buy, array
    stock_sell_arr = [None] * date_count # danh sách các mã được sell, array
    # nav_stock_assign_to_nav_arr = [None] * date_count 

    # Time grouping
    if time_groupby == 'MONTH_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif time_groupby == 'QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,4,7,10]
    elif time_groupby == 'AM_QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [2,5,8,11]
    elif isinstance(time_groupby, (int, float)):
        datetable_2['date_rebalance'] = datetable_2['date_trading_count'] % time_groupby
        first_date_arr = datetable_2['date_rebalance']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]

    # First day initialization
    nav_total[0] = 1

    in_arr[0] = [x for x in ticker_position_arr[0] if ((first_date_arr[0] == 1) and (month_arr[0] in month))]
    out_arr[0] = []
    stay_arr[0] = []
    assign_arr[0] = in_arr[0]

    # list PCA-GR_1D-A_1D hàng ngày
    assign_r1d_arr[0] = [r1d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]

    # list các nav_stock ở các nhóm
    nav_stock_in_arr[0] = [nav_total[0] / len(in_arr[0]) for _ in range(len(in_arr[0]))]
    nav_stock_out_arr[0] = []
    nav_stock_stay_diff_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_diff_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    nav_buy_arr[0] = nav_stock_in_arr[0]
    nav_sell_arr[0] = []
    nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]
    nav_buy_to_nav[0] = sum(nav_stock_in_arr[0])
    nav_sell_to_nav[0] = sum(nav_stock_out_arr[0])
    nav_buy_to_nav_arr[0] = nav_stock_in_arr[0]
    # nav_stock_assign_to_nav_arr[0] = [x/nav_total[0] for x in nav_stock_assign_arr[0]]

    # các chỉ tiêu quản lý cả danh mục
    cash[0] = nav_total[0] - nav_stock[0]
    nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]
    max_assign[0] = max([x for x in nav_stock_to_nav_arr[0]], default = 0)
    number_of_stock[0] = len(assign_arr[0])

    # Iteration through days
    i = 1
    while i < date_count:
        
        if ((first_date_arr[i] == 1) and (month_arr[i] in month)):
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = [x for x in ticker_position_arr[i] if x not in set(assign_arr[i-1])]
            stay_arr[i] = [x for x in ticker_position_arr[i] if x in set(assign_arr[i-1])]
            out_arr[i] = [x for x in assign_arr[i-1] if x not in set(ticker_position_arr[i])]
            assign_arr[i] = in_arr[i] + stay_arr[i]       

            # các array liên quan đến return cp stay - in - out
            assign_r1d_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(assign_arr[i]))]
            nav_stock_in_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(in_arr[i]))]
            nav_stock_stay_diff_arr[i] = [nav_total[i]/len(assign_arr[i]) - nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
            
            nav_stock_out_arr[i] = [-1 * nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]
            nav_buy_arr[i] = nav_stock_in_arr[i] + [x for x in nav_stock_stay_diff_arr[i] if x > 0]
            nav_sell_arr[i] = nav_stock_out_arr[i] + [x for x in nav_stock_stay_diff_arr[i] if x < 0]

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]
            max_assign[i] = max([x for x in nav_stock_to_nav_arr[i]], default = 0)
            nav_buy_to_nav[i] = sum(nav_buy_arr[i]) / nav_total[i]
            nav_sell_to_nav[i] = sum(nav_sell_arr[i]) / nav_total[i]
            nav_buy_to_nav_arr[i] = [x/nav_total[i] for x in nav_buy_arr[i]]
            nav_sell_to_nav_arr[i] = [x/nav_total[i] for x in nav_sell_arr[i]]
            stock_buy_arr[i] = in_arr[i] + [stay_arr[i][j] for j in range(len(nav_stock_stay_diff_arr[i])) if nav_stock_stay_diff_arr[i][j] > 0]
            stock_sell_arr[i] = out_arr[i] + [stay_arr[i][j] for j in range(len(nav_stock_stay_diff_arr[i])) if nav_stock_stay_diff_arr[i][j] < 0]
            # nav_stock_assign_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_assign_arr[i]]
        else:
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = []
            stay_arr[i] = assign_arr[i-1]
            out_arr[i] = []
            assign_arr[i] = in_arr[i] + stay_arr[i]       

            # các array liên quan đến return cp stay - in - out
            assign_r1d_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], assign_r1d_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [x for x in nav_stock_assign_arr_last_day]
            nav_stock_in_arr[i] = []
            nav_stock_stay_diff_arr[i] = [x for x in nav_stock_assign_arr_last_day]
            
            nav_stock_out_arr[i] = 0
            nav_buy_arr[i] = []
            nav_sell_arr[i] = []

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]
            max_assign[i] = max([x for x in nav_stock_to_nav_arr[i]], default = 0)
            nav_buy_to_nav[i] = sum(nav_buy_arr[i]) / nav_total[i]
            nav_sell_to_nav[i] = sum(nav_sell_arr[i]) / nav_total[i]

            nav_buy_to_nav_arr[i] = [x/nav_total[i] for x in nav_buy_arr[i]]
            nav_sell_to_nav_arr[i] = [x/nav_total[i] for x in nav_sell_arr[i]]
            stock_buy_arr[i] = []
            stock_sell_arr[i] = []
            # nav_stock_assign_to_nav_arr[i] = [x/nav_total[i] for x in nav_stock_assign_arr[i]]

        i = i + 1
    # create Dataframe
    df_assign = pd.DataFrame({
        'DATE_TRADING': datetable['DATE_TRADING'],
        'stock_list': assign_arr,
        'acc_return': nav_total,
        'cash': cash,
        'ticker_count': number_of_stock,
        'nav_stock': nav_stock,
        'max_assign': max_assign,
        'nav_buy_to_nav': nav_buy_to_nav,
        'nav_buy_to_nav_arr': nav_buy_to_nav_arr,
        'nav_sell_to_nav': nav_sell_to_nav,
        'nav_sell_to_nav_arr': nav_sell_to_nav_arr,
        'nav_stock_to_nav_arr': nav_stock_to_nav_arr,
    })

    # create metrics
    df_assign = pd.DataFrame(df_assign)
    df_assign['daily_return'] = df_assign['acc_return'] / df_assign['acc_return'].shift(1) - 1
    df_assign['daily_return'].fillna(value = 0, inplace = True)
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']
    if fee == True:
        df_assign = fee_create(df_assign)
    elif fee == False:
        df_assign = fee_create(df_assign, fee_buy= 0, fee_sell= 0)

    return df_assign

def assign_equal_rebalance_v1(df, time_groupby, date_start, date_end, database_version, stock_break = True, fee = True):
    date_count_ref = load_date_count_ref(database_version)
    df_tem = df.copy()
    df_tem = df_tem[(df_tem['DATE_TRADING'] >= date_start) & (df_tem['DATE_TRADING'] < date_end)]
    df_tem = df_tem.reset_index()
    datetable = df_tem.groupby('DATE_TRADING').agg({'TICKER': list, 'PCA-GR_1D-A_1D': list, 'PCA-RV_XDP_120D': list}).reset_index().reset_index()
    datetable.rename(columns = {'index':'date_trading_count'}, inplace = True)
    date_count = len(datetable.index.values)
    ticker_arr = datetable['TICKER'].values
    r1d_arr = datetable['PCA-GR_1D-A_1D'].values
    pca_xdp_120d_arr = datetable['PCA-RV_XDP_120D'].values

    datetable_2 = df_tem[df_tem['position'] == 1].groupby('DATE_TRADING')['TICKER'].apply(list).reset_index()
    datetable_2 = pd.merge(datetable[['DATE_TRADING','date_trading_count']], datetable_2, how= 'left', on= 'DATE_TRADING')
    datetable_2 = pd.merge(datetable_2, date_count_ref, how= 'left', on= 'DATE_TRADING')
    datetable_2["TICKER"] = datetable_2["TICKER"].apply(lambda x: [] if x != x else x)

    ticker_position_arr = datetable_2["TICKER"].values
    month_arr = datetable_2["MONTH"].values

    # Metrics initialization
    nav_total = [None] * date_count # nav_total, mỗi ngày 1 số
    number_of_stock = [None] * date_count # số mã trong danh mục, mỗi ngày 1 số
    cash = [None] * date_count # cash_value, mỗi ngày 1 số
    max_assign = [None] * date_count # max_assign, mỗi ngày 1số

    in_arr = [None] * date_count # danh sách mã mới vào, array
    out_arr = [None] * date_count # danh sách mã  bị loại, array
    stay_arr = [None] * date_count # danh sách mã tiếp tục ở lại, array
    assign_arr = [None] * date_count # danh sách mã được assign, array

    r1d_assign_arr = [None] * date_count # PCA-GR_1D-A_1D của các mã được assign
    pca_rv_xdp_120d_assign_arr = [None] * date_count # PCA-RV_XDP_120D của các mã được assign

    nav_stock_in_arr = [None] * date_count # nav_each_stock trong danh sách in, array
    nav_stock_out_arr = [None] * date_count # nav_each_stock trong danh sách out, array
    nav_stock_stay_diff_arr = [None] * date_count # chênh lệch giữa nav t0 của cổ phiếu và nav t-1 * pca_r1d_a1d, array
    nav_stock_assign_arr = [None] * date_count # nav_each_assign_stock , array
    nav_stock = [None] * date_count # nav_stock, number
    nav_stock_to_nav_arr = [None] * date_count # tỉ trọng từng cổ phiếu trong danh mục, array

    # Time grouping
    if time_groupby == 'MONTH_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif time_groupby == 'QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,4,7,10]
    elif time_groupby == 'AM_QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [2,5,8,11]
    elif isinstance(time_groupby, (int, float)):
        datetable_2['date_rebalance'] = datetable_2['date_trading_count'] % time_groupby
        first_date_arr = datetable_2['date_rebalance']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]

    # First day initialization
    nav_total[0] = 1

    in_arr[0] = [x for x in ticker_position_arr[0] if ((first_date_arr[0] == 1) and (month_arr[0] in month))]
    out_arr[0] = []
    stay_arr[0] = []
    assign_arr[0] = in_arr[0]

    # list PCA-GR_1D-A_1D hàng ngày
    r1d_assign_arr[0] = [r1d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]
    pca_rv_xdp_120d_assign_arr[0] = [pca_xdp_120d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]

    # list các nav_stock ở các nhóm
    nav_stock_in_arr[0] = [nav_total[0] / len(in_arr[0]) for _ in range(len(in_arr[0]))]
    nav_stock_out_arr[0] = []
    nav_stock_stay_diff_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_diff_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]

    # các chỉ tiêu quản lý cả danh mục
    cash[0] = nav_total[0] - nav_stock[0]
    nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]
    max_assign[0] = max([x for x in nav_stock_to_nav_arr[0]], default = 0)
    number_of_stock[0] = len(assign_arr[0])

    # Iteration through days
    i = 1
    while i < date_count:
        
        if ((first_date_arr[i] == 1) and (month_arr[i] in month)):
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = [x for x in ticker_position_arr[i] if x not in set(assign_arr[i-1])]
            stay_arr[i] = [x for x in ticker_position_arr[i] if x in set(assign_arr[i-1])]
            out_arr[i] = [x for x in assign_arr[i-1] if x not in set(ticker_position_arr[i])]
            assign_arr[i] = in_arr[i] + stay_arr[i]       

            # các array liên quan đến return cp stay - in - out
            r1d_assign_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            pca_rv_xdp_120d_assign_arr[i] = [pca_xdp_120d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], r1d_assign_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(assign_arr[i]))]
            if stock_break == True:
                nav_stock_assign_arr[i] = [x if pca_rv_xdp_120d_assign_arr[i][j] < 1 else 0 for j, x in enumerate(nav_stock_assign_arr[i])]
            nav_stock_in_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(in_arr[i]))]
            nav_stock_stay_diff_arr[i] = [nav_total[i]/len(assign_arr[i]) - nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
            
            nav_stock_out_arr[i] = [-1 * nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]
            max_assign[i] = max([x for x in nav_stock_to_nav_arr[i]], default = 0)

        else:
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = []
            stay_arr[i] = assign_arr[i-1]
            out_arr[i] = []
            assign_arr[i] = in_arr[i] + stay_arr[i]

            # các array liên quan đến return cp stay - in - out
            r1d_assign_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            pca_rv_xdp_120d_assign_arr[i] = [pca_xdp_120d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], r1d_assign_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [x for x in nav_stock_assign_arr_last_day]
            if stock_break == True:
                nav_stock_assign_arr[i] = [x if pca_rv_xdp_120d_assign_arr[i][j] < 1 else 0 for j, x in enumerate(nav_stock_assign_arr[i])]
            nav_stock_in_arr[i] = []
            nav_stock_stay_diff_arr[i] = [x for x in nav_stock_assign_arr_last_day]
            
            nav_stock_out_arr[i] = 0

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]

        i = i + 1

    df_assign = pd.DataFrame({
        'DATE_TRADING': datetable['DATE_TRADING'],
        'stock_list': assign_arr,
        'acc_return': nav_total,
        'cash': cash,
        'nav_stock': nav_stock,
        'nav_stock_to_nav_arr': nav_stock_to_nav_arr,
    })

    df_assign = trading_to_nav_calculate_function(df_assign, database_version)

    # create metrics
    df_assign = pd.DataFrame(df_assign)
    df_assign['daily_return'] = df_assign['acc_return'] / df_assign['acc_return'].shift(1) - 1
    df_assign['daily_return'].fillna(value = 0, inplace = True)
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']
    
    if fee == True:
        df_assign = fee_create(df_assign)
    elif fee == False:
        df_assign = fee_create(df_assign, fee_buy= 0, fee_sell= 0)
    
    return df_assign

def assign_equal_rebalance_v2(df, time_groupby, date_start, date_end, database_version, threshold_cut_loss, threshold_reenter, stock_break = True, fee = True):
    """ Có thêm chức năng cutloss và reenter"""
    date_count_ref = load_date_count_ref(database_version)
    df_tem = df.copy()
    df_tem = df_tem[(df_tem['DATE_TRADING'] >= date_start) & (df_tem['DATE_TRADING'] < date_end)]
    df_tem = df_tem.reset_index()
    df_tem = position_trailing_stop_create_and_reenter(df_tem, threshold_cut_loss, threshold_reenter, database_version = database_version)
    df_tem['signal_trailing_cut_loss_and_reenter'] = np.where((df_tem['position'] == df_tem['position'].shift(1)) & (df_tem['TICKER'] == df_tem['TICKER'].shift(1)),
                            df_tem['assign_trailing_cut_loss_and_reenter'] - df_tem['assign_trailing_cut_loss_and_reenter'].shift(1),
                            0 )
    datetable = df_tem.groupby('DATE_TRADING').agg({'TICKER': list, 'PCA-GR_1D-A_1D': list, 'PCA-RV_XDP_120D': list, 'signal_trailing_cut_loss_and_reenter': list, 'assign_trailing_cut_loss_and_reenter': list}).reset_index().reset_index()
    datetable.rename(columns = {'index':'date_trading_count'}, inplace = True)
    date_count = len(datetable.index.values)
    ticker_arr = datetable['TICKER'].values
    r1d_arr = datetable['PCA-GR_1D-A_1D'].values
    pca_xdp_120d_arr = datetable['PCA-RV_XDP_120D'].values
    signal_trailing_cut_loss_and_reenter_arr = datetable['signal_trailing_cut_loss_and_reenter'].values
    assign_trailing_cut_loss_and_reenter_arr = datetable['assign_trailing_cut_loss_and_reenter'].values

    datetable_2 = df_tem[df_tem['position'] == 1].groupby('DATE_TRADING')['TICKER'].apply(list).reset_index()
    datetable_2 = pd.merge(datetable[['DATE_TRADING','date_trading_count']], datetable_2, how= 'left', on= 'DATE_TRADING')
    datetable_2 = pd.merge(datetable_2, date_count_ref, how= 'left', on= 'DATE_TRADING')
    datetable_2["TICKER"] = datetable_2["TICKER"].apply(lambda x: [] if x != x else x)

    ticker_position_arr = datetable_2["TICKER"].values
    month_arr = datetable_2["MONTH"].values

    # Metrics initialization
    nav_total = [None] * date_count # nav_total, mỗi ngày 1 số
    number_of_stock = [None] * date_count # số mã trong danh mục, mỗi ngày 1 số
    cash = [None] * date_count # cash_value, mỗi ngày 1 số
    max_assign = [None] * date_count # max_assign, mỗi ngày 1số

    in_arr = [None] * date_count # danh sách mã mới vào, array
    out_arr = [None] * date_count # danh sách mã  bị loại, array
    stay_arr = [None] * date_count # danh sách mã tiếp tục ở lại, array
    assign_arr = [None] * date_count # danh sách mã được assign, array

    r1d_assign_arr = [None] * date_count # PCA-GR_1D-A_1D của các mã được assign
    pca_rv_xdp_120d_assign_arr = [None] * date_count # PCA-RV_XDP_120D của các mã được assign
    assign_trailing_cut_loss_and_reenter_assign_arr = [None] * date_count
    signal_trailing_cut_loss_and_reenter_assign_arr = [None] * date_count
    cash_for_stock_arr = [None] * date_count # cash của 1 cp có assign nhưng bị cut_loss

    nav_stock_in_arr = [None] * date_count # nav_each_stock trong danh sách in, array
    nav_stock_out_arr = [None] * date_count # nav_each_stock trong danh sách out, array
    nav_stock_stay_diff_arr = [None] * date_count # chênh lệch giữa nav t0 của cổ phiếu và nav t-1 * pca_r1d_a1d, array
    nav_stock_assign_arr = [None] * date_count # nav_each_assign_stock , array
    nav_stock = [None] * date_count # nav_stock, number
    nav_stock_to_nav_arr = [None] * date_count # tỉ trọng từng cổ phiếu trong danh mục, array

    # Time grouping
    if time_groupby == 'MONTH_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif time_groupby == 'QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [1,4,7,10]
    elif time_groupby == 'AM_QUARTER_STR':
        first_date_arr = datetable_2['MDCOUNT_POS']
        month = [2,5,8,11]
    elif isinstance(time_groupby, (int, float)):
        datetable_2['date_rebalance'] = datetable_2['date_trading_count'] % time_groupby
        first_date_arr = datetable_2['date_rebalance']
        month = [1,2,3,4,5,6,7,8,9,10,11,12]

    # First day initialization
    nav_total[0] = 1

    in_arr[0] = [x for x in ticker_position_arr[0] if ((first_date_arr[0] == 1) and (month_arr[0] in month))]
    out_arr[0] = []
    stay_arr[0] = []
    assign_arr[0] = in_arr[0]

    # list PCA-GR_1D-A_1D hàng ngày
    r1d_assign_arr[0] = [r1d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]
    pca_rv_xdp_120d_assign_arr[0] = [pca_xdp_120d_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]
    assign_trailing_cut_loss_and_reenter_assign_arr[0] = [assign_trailing_cut_loss_and_reenter_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]
    signal_trailing_cut_loss_and_reenter_assign_arr[0] = [signal_trailing_cut_loss_and_reenter_arr[0][ticker_arr[0].index(j)] for j in assign_arr[0]]
    cash_for_stock_arr[0] = [0 for _ in range(len(assign_arr[0]))]

    # list các nav_stock ở các nhóm
    nav_stock_in_arr[0] = [nav_total[0] / len(in_arr[0]) for _ in range(len(in_arr[0]))]
    nav_stock_out_arr[0] = []
    nav_stock_stay_diff_arr[0] = []
    nav_stock_assign_arr[0] = nav_stock_in_arr[0] + nav_stock_stay_diff_arr[0]
    nav_stock[0] = sum(nav_stock_assign_arr[0])
    # nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]

    # các chỉ tiêu quản lý cả danh mục
    cash[0] = nav_total[0] - nav_stock[0]
    nav_stock_to_nav_arr[0] = [x / nav_total[0] for x in nav_stock_assign_arr[0]]
    max_assign[0] = max([x for x in nav_stock_to_nav_arr[0]], default = 0)
    number_of_stock[0] = len(assign_arr[0])

    # Iteration through days
    i = 1
    while i < date_count:
        
        if ((first_date_arr[i] == 1) and (month_arr[i] in month)):
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = [x for x in ticker_position_arr[i] if x not in set(assign_arr[i-1])]
            stay_arr[i] = [x for x in ticker_position_arr[i] if x in set(assign_arr[i-1])]
            out_arr[i] = [x for x in assign_arr[i-1] if x not in set(ticker_position_arr[i])]
            assign_arr[i] = in_arr[i] + stay_arr[i]       

            # các array liên quan đến return cp stay - in - out
            r1d_assign_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            pca_rv_xdp_120d_assign_arr[i] = [pca_xdp_120d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            assign_trailing_cut_loss_and_reenter_assign_arr[i] = [assign_trailing_cut_loss_and_reenter_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            signal_trailing_cut_loss_and_reenter_assign_arr[i] = [signal_trailing_cut_loss_and_reenter_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], r1d_assign_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(assign_arr[i]))]

            cash_for_stock_arr[i] = [0 if assign_trailing_cut_loss_and_reenter_assign_arr[i][j] == 1 
                                        else x for j, x in enumerate(nav_stock_assign_arr[i])]
            nav_stock_assign_arr[i] = [x if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == 0 
                                        else 0 if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == -1 
                                        else cash_for_stock_arr[i][j] for j, x in enumerate(nav_stock_assign_arr[i])]

            if stock_break == True:
                nav_stock_assign_arr[i] = [x if pca_rv_xdp_120d_assign_arr[i][j] < 1 else 0 for j, x in enumerate(nav_stock_assign_arr[i])]
            
            nav_stock_in_arr[i] = [nav_total[i]/len(assign_arr[i]) for _ in range(len(in_arr[i]))]
            nav_stock_stay_diff_arr[i] = [nav_total[i]/len(assign_arr[i]) - nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in stay_arr[i]]
            
            nav_stock_out_arr[i] = [-1 * nav_stock_assign_arr_last_day[assign_arr[i-1].index(j)] for j in out_arr[i]]

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]
            max_assign[i] = max([x for x in nav_stock_to_nav_arr[i]], default = 0)

        else:
            # các array liên quan đến danh sách cp stay - in - out
            in_arr[i] = []
            stay_arr[i] = assign_arr[i-1]
            out_arr[i] = []
            assign_arr[i] = in_arr[i] + stay_arr[i]

            # các array liên quan đến return cp stay - in - out
            r1d_assign_arr[i] = [r1d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            pca_rv_xdp_120d_assign_arr[i] = [pca_xdp_120d_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            assign_trailing_cut_loss_and_reenter_assign_arr[i] = [assign_trailing_cut_loss_and_reenter_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]
            signal_trailing_cut_loss_and_reenter_assign_arr[i] = [signal_trailing_cut_loss_and_reenter_arr[i][ticker_arr[i].index(j)] for j in assign_arr[i]]

            # list các nav_stock ở các nhóm và các chỉ tiêu cả danh mục
            number_of_stock[i] = len(assign_arr[i])

            nav_stock_assign_arr_last_day = [x * y for x, y in zip(nav_stock_assign_arr[i-1], r1d_assign_arr[i-1])]
            nav_total[i] = sum(nav_stock_assign_arr_last_day) + cash[i-1]
            nav_stock_assign_arr[i] = [x for x in nav_stock_assign_arr_last_day]

            cash_for_stock_arr[i] = [nav_stock_assign_arr[i][j] if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == -1 
                                        else 0 if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == 1 
                                        else cash_for_stock_arr[i-1][j] for j, x in enumerate(cash_for_stock_arr[i-1])]
            
            nav_stock_assign_arr[i] = [x if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == 0 
                                        else 0 if signal_trailing_cut_loss_and_reenter_assign_arr[i][j] == -1 
                                        else cash_for_stock_arr[i][j] for j, x in enumerate(nav_stock_assign_arr[i])]

            if stock_break == True:
                nav_stock_assign_arr[i] = [x if pca_rv_xdp_120d_assign_arr[i][j] < 1 else 0 for j, x in enumerate(nav_stock_assign_arr[i])]
            nav_stock_in_arr[i] = []
            nav_stock_stay_diff_arr[i] = [x for x in nav_stock_assign_arr_last_day]
            
            nav_stock_out_arr[i] = 0

            nav_stock[i] = sum(nav_stock_assign_arr[i])
            cash[i] = nav_total[i] - nav_stock[i]
            nav_stock_to_nav_arr[i] = [x / nav_total[i] for x in nav_stock_assign_arr[i]]

        i = i + 1

    df_assign = pd.DataFrame({
        'DATE_TRADING': datetable['DATE_TRADING'],
        'stock_list': assign_arr,
        'acc_return': nav_total,
        'cash': cash,
        'nav_stock': nav_stock,
        'nav_stock_to_nav_arr': nav_stock_to_nav_arr,
    })

    df_assign = trading_to_nav_calculate_function(df_assign, database_version)

    # create metrics
    df_assign = pd.DataFrame(df_assign)
    df_assign['daily_return'] = df_assign['acc_return'] / df_assign['acc_return'].shift(1) - 1
    df_assign['daily_return'].fillna(value = 0, inplace = True)
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']

    if fee == True:
        df_assign = fee_create(df_assign)
    elif fee == False:
        df_assign = fee_create(df_assign, fee_buy= 0, fee_sell= 0)
    
    return df_assign

def break_from_acc_return_rv(df, hypothesis_choosen, rank_choosen, window, threshold, database_version):
    df[f'{rank_choosen}'] = df[f'{rank_choosen}'] + 1
    if rank_choosen != hypothesis_choosen:
        df[f'{hypothesis_choosen}'] = df[f'{hypothesis_choosen}'] + 1
    df[f'acc_return_{rank_choosen}'] = df[f'{rank_choosen}'].cumprod()
    df[f'rank_acc_return_{rank_choosen}_{window}'] = df[f'acc_return_{rank_choosen}'].rolling(window= window).apply(lambda x: pd.Series(x).rank(pct=True).iloc[-1])
    df['assign'] = 0
    index_values = df['assign'].index.values
    df[f'{hypothesis_choosen}'].fillna(value= 0, inplace= True)

    for i in index_values:
        if df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] < threshold:
            df['assign'].iloc[i] = 0
        elif df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] < 0.2:
            df['assign'].iloc[i] = 0.5
        elif df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] < 0.4:
            df['assign'].iloc[i] = 1
        elif df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] < 0.6:
            df['assign'].iloc[i] = 1
        elif df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] < 0.8:
            df['assign'].iloc[i] = 1
        elif df[f'rank_acc_return_{rank_choosen}_{window}'].iloc[i] <= 1:
            df['assign'].iloc[i] = 1

    acc_return_adj_arr = []
    stock_nav_arr = []
    cash_arr = []

    acc_return_adj = 1
    stock_nav = 0
    cash = 1

    for index in index_values:
        acc_return_adj = stock_nav*(df[f'{hypothesis_choosen}'].loc[index]) + cash
        if df['assign'].iloc[index] == df['assign'].iloc[index - 1]:
            stock_nav = stock_nav*(df[f'{hypothesis_choosen}'].loc[index])
        else:
            stock_nav = acc_return_adj * df['assign'].iloc[index]
            cash = acc_return_adj - stock_nav
        acc_return_adj_arr.append(acc_return_adj)
        stock_nav_arr.append(stock_nav)
        cash_arr.append(cash)

    df['acc_return_adj'] = acc_return_adj_arr
    df['stock_nav'] = stock_nav_arr
    df['cash'] = cash_arr

    df_adj = df.loc[:,('DATE_TRADING','acc_return_adj')]
    df_adj.rename(columns = {'acc_return_adj':'acc_return'}, inplace = True)
    evaluate_briefly(df_adj, database_version)

def cut_universe_and_compare(df, indicator, signal_kind, threshold, time_lag, time_groupby):

    print('#################################################################################################')
    print(f'\nKết quả dùng {indicator} {signal_kind} {threshold} cắt tập gốc, thì {time_lag} sẽ như thế nào?')
    # tách tập    
    date_count_ref_df = load_date_count_ref()
    date_count_ref_df = date_count_ref_df.groupby(f'{time_groupby}')['DATE_TRADING'].min().reset_index()
    gr_df_tem = df.copy()

    if signal_kind == 'greater':
        gr_df_tem['group'] = np.where(gr_df_tem[f'{indicator}'].isna(), "nan", np.where(gr_df_tem[f'{indicator}'] > threshold, "a", "b")) # group passes condition is a, other is b
    elif signal_kind == 'smaller':
        gr_df_tem['group'] = np.where(gr_df_tem[f'{indicator}'].isna(), "nan", np.where(gr_df_tem[f'{indicator}'] < threshold, "a", "b"))
    elif signal_kind == 'equal':
        gr_df_tem['group'] = np.where(gr_df_tem[f'{indicator}'].isna(), "nan", np.where(gr_df_tem[f'{indicator}'] == threshold, "a", "b"))
    elif signal_kind == 'greater_or_equal':
        gr_df_tem['group'] = np.where(gr_df_tem[f'{indicator}'].isna(), "nan", np.where(gr_df_tem[f'{indicator}'] >= threshold, "a", "b"))
    elif signal_kind == 'smaller_or_equal':
        gr_df_tem['group'] = np.where(gr_df_tem[f'{indicator}'].isna(), "nan", np.where(gr_df_tem[f'{indicator}'] <= threshold, "a", "b"))

    # 1) Theo độ lớn của indicator thì gr_nD thế nào?
    print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
    gr_df_tem[f'{indicator}_quantile'] = pd.qcut(gr_df_tem[f'{indicator}'], q = 10, labels= False, duplicates='drop')
    quantile_df = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].describe().reset_index()
    
    quantile_df_prod = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
    quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
    quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator}_quantile', f'annualize_return']], how= 'left', on= f'{indicator}_quantile')

    display(quantile_df)
    
    sns.set(rc= {'figure.figsize': (8, 4)})
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= 'mean', alpha= 1, label= 'mean')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '25%', alpha= 1, label= '25%')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '50%', alpha= 1, label= '50%')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '75%', alpha= 1, label= '75%')
    plt.xlabel(f'{indicator}_quantile')
    plt.ylabel(time_lag)
    plt.title(f'{indicator}_quantile, thì {time_lag} như thế nào?')
    plt.show()

    # 2) So sánh return 2 tập a và b?
    print(f'\n2) So sánh 2 tập a và b')

    quantile_df = gr_df_tem.groupby(['group'])[f'{time_lag}'].describe().reset_index()
    quantile_df_prod = gr_df_tem.groupby(['group'])['PCA-GR_1D-A_1D'].apply(gmean_ignore_nan).reset_index()
    quantile_df_prod[f'annualize_return'] = quantile_df_prod['PCA-GR_1D-A_1D']**250-1
    quantile_df = pd.merge(quantile_df, quantile_df_prod[['group', 'annualize_return']], how= 'left', on= 'group')
    quantile_df['mean_count_ticker'] = quantile_df['count'] / df['DATE_TRADING'].nunique()

    tem = gr_df_tem.groupby(['DATE_TRADING','group'])['PCA-GR_1D-A_1D'].mean().reset_index()
    tem_1 = tem.groupby(['group'])['PCA-GR_1D-A_1D'].prod().reset_index()
    tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
    quantile_df = pd.merge(quantile_df, tem_1[['group', 'eq1d_anlz_return']], how= 'left', on= 'group')

    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('group')['TICKER'].count().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('group')['TICKER'].count().reset_index()
    all = gr_df_tem.groupby('group')['TICKER'].count().reset_index()
    all['cnt_positive'] = pos['TICKER'] / all['TICKER']
    all['cnt_negative'] = neg['TICKER'] / all['TICKER']
    # quantile_df = pd.merge(quantile_df, all[['group','cnt_positive','cnt_negative']], how= 'left', on= 'group')

    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('group')['PCA-GR_1D-A_1D'].mean().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('group')['PCA-GR_1D-A_1D'].mean().reset_index()

    pos.rename(columns= {'PCA-GR_1D-A_1D': 'pos_mean_r1D'}, inplace= True)
    neg.rename(columns= {'PCA-GR_1D-A_1D': 'neg_mean_r1D'}, inplace= True)

    all = pd.merge(all[['group','cnt_positive','cnt_negative']], pos, how= 'left', on= 'group')
    all = pd.merge(all, neg, how= 'left', on= 'group')
    all['kelly'] = - all['cnt_positive'] * (1- all['pos_mean_r1D']) / (all['cnt_negative'] * (1-all['neg_mean_r1D']))

    display(quantile_df)
    display(all)
    # # 3) Theo số mã
    # print(f'\n3) phần này trả lời câu hỏi, distribution return sau {time_lag} của tập {indicator} {signal_kind} {threshold} và tập còn lại, \ngroupby theo TICKER, và các distribution return này qua từng mã\n')
    # gr_group_df = gr_df_tem.groupby(['TICKER','group'])[time_lag].describe().reset_index()
    # # print(f'\ntop 6cp có mean khi indicator {indicator} đạt threshold {threshold} cao nhất')
    # # display(gr_group_df[gr_group_df['group'] == 'a'][['TICKER','group','mean','25%','50%','75%']].nlargest(6,'mean'))

    # # print(f'\ntop 6cp có mean khi indicator {indicator} đạt threshold {threshold} thấp nhất')
    # # display(gr_group_df[gr_group_df['group'] == 'a'][['TICKER','group','mean','25%','50%','75%']].nsmallest(6,'mean'))        

    # compare_list = ['mean', '25%', '50%', '75%']
    # for i in compare_list:
    #     pivot_df = gr_group_df.pivot_table(values= i, index= 'TICKER', columns='group', aggfunc='mean').reset_index()
    #     pivot_df['a-b'] = pivot_df['a'] - pivot_df['b']
    #     y = pivot_df[pivot_df['a-b'] >= 0]['TICKER'].count() / pivot_df[pivot_df['a-b'].notna()]['TICKER'].count()
    #     print(f'{y} số TICKER, {i} {time_lag} của tập {indicator} {signal_kind} {threshold} cao hơn tập còn lại')

    # # 4) tỉ lệ a và b xảy ra qua thời gian
    # print(f'\n4) phần này trả lời câu hỏi, tỉ lệ tập indicator {indicator} {signal_kind} {threshold} và tập còn lại xảy ra theo thời gian, groupby theo {time_groupby} ')

    # df_cnt_total = gr_df_tem.groupby([f'{time_groupby}'])['TICKER'].count().reset_index()
    # df_cnt_group = gr_df_tem.groupby([f'{time_groupby}','group'])['TICKER'].count().reset_index()
    # df_cnt_total.rename(columns= {'TICKER':'cnt_total'}, inplace= True)
    # df_cnt_group.rename(columns= {'TICKER':'cnt_group'}, inplace= True)

    # df_cnt_group = pd.merge(df_cnt_group, df_cnt_total, how= 'left', on= [f'{time_groupby}'])
    # df_cnt_group = pd.merge(df_cnt_group, date_count_ref_df, how= 'left', on= [f'{time_groupby}'])
    # df_cnt_group['percentage'] = df_cnt_group['cnt_group']/df_cnt_group['cnt_total']

    # df_cnt_group_timely = df_cnt_group.groupby([f'{time_groupby}','group'])['percentage'].median().reset_index()
    # df_cnt_group_timely = pd.merge(df_cnt_group_timely, date_count_ref_df, how= 'left', on= f'{time_groupby}')

    # sns.set(rc= {'figure.figsize': (8, 4)})
    # sns.scatterplot(data= df_cnt_group_timely[df_cnt_group_timely['group'] == 'a'], x= 'DATE_TRADING', y= 'percentage', alpha= 0.5, label= 'a')
    # sns.scatterplot(data= df_cnt_group_timely[df_cnt_group_timely['group'] == 'b'], x= 'DATE_TRADING', y= 'percentage', alpha= 0.5, label= 'b')
    # plt.xlabel('Date Trading')
    # plt.ylabel('group')
    # plt.title(f'% số mã đạt {indicator} {signal_kind} {threshold}, median groupby theo {time_groupby}')
    # plt.show()

    # print(f'Distribution tỷ lệ xảy ra tập indicator {indicator} {signal_kind} {threshold} toàn bộ thời gian')
    # display(df_cnt_group_timely[df_cnt_group_timely['group'] == 'a']['percentage'].describe())

    # # 5) Return sau n ngày của tập đạt điều kiện và tập còn lại

    # print(f'\n5) phần này trả lời câu hỏi, distribution return sau {time_lag} của các tập indicator {indicator} {signal_kind} {threshold} và tập còn lại, \ngroupby theo {time_groupby}, và các distribution return này qua thời gian')
    # gr_group_df = gr_df_tem.groupby([f'{time_groupby}','group'])[time_lag].describe().reset_index()
    # gr_group_df = pd.merge(gr_group_df, date_count_ref_df, how= 'left', on= f'{time_groupby}')

    # sns.set(rc= {'figure.figsize': (8, 4)})
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'a'], x= 'DATE_TRADING', y= '25%', alpha= 1, label= 'a_25%')
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'a'], x= 'DATE_TRADING', y= '50%', alpha= 1, label= 'a_50%')
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'a'], x= 'DATE_TRADING', y= '75%', alpha= 1, label= 'a_75%')
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'b'], x= 'DATE_TRADING', y= '25%', alpha= 1, label= 'b_25%')
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'b'], x= 'DATE_TRADING', y= '50%', alpha= 1, label= 'b_50%')
    # sns.lineplot(data= gr_group_df[gr_group_df['group'] == 'b'], x= 'DATE_TRADING', y= '75%', alpha= 1, label= 'b_75%')
    # plt.xlabel('Date Trading')
    # plt.ylabel(time_lag)
    # plt.title(f'{time_lag} của từng group, median groupby theo {time_groupby}')
    # plt.show()

    # compare_list = ['mean', '25%', '50%', '75%']
    # for i in compare_list:
    #     pivot_df = gr_group_df.pivot_table(values= i, index= time_groupby, columns='group', aggfunc='mean').reset_index()
    #     pivot_df['a-b'] = pivot_df['a'] - pivot_df['b']
    #     y = pivot_df[pivot_df['a-b'] >= 0][time_groupby].count() / pivot_df[pivot_df['a-b'].notna()][time_groupby].count()
    #     print(f'{y} số {time_groupby}, {i} {time_lag} của tập {indicator} {signal_kind} {threshold} cao hơn tập còn lại')
    
def compare_two_samples(df, time_lag, date_start, date_end):

    print(f'\nKết quả so sánh 2 tập a và b thì {time_lag} sẽ như thế nào?')
    
    gr_df_tem = df[(df['DATE_TRADING'] > date_start) & (df['DATE_TRADING'] < date_end)].copy()

    quantile_df = gr_df_tem.groupby(['group'])[f'{time_lag}'].describe().reset_index()
    quantile_df_prod = gr_df_tem.groupby(['group'])['PCA-GR_1D-A_1D'].apply(gmean_ignore_nan).reset_index()
    quantile_df_prod[f'anlz_return'] = quantile_df_prod['PCA-GR_1D-A_1D']**250-1
    quantile_df = pd.merge(quantile_df, quantile_df_prod[['group', f'anlz_return']], how= 'left', on= 'group')
    quantile_df['mean_count_ticker'] = quantile_df['count'] / gr_df_tem['DATE_TRADING'].nunique()
    
    tem = gr_df_tem.groupby(['DATE_TRADING','group'])['PCA-GR_1D-A_1D'].mean().reset_index()
    tem_1 = tem.groupby(['group'])['PCA-GR_1D-A_1D'].prod().reset_index()
    tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
    quantile_df = pd.merge(quantile_df, tem_1[['group', 'eq1d_anlz_return']], how= 'left', on= 'group')
    
    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('group')['TICKER'].count().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('group')['TICKER'].count().reset_index()
    all = gr_df_tem.groupby('group')['TICKER'].count().reset_index()
    all['cnt_positive'] = pos['TICKER'] / all['TICKER']
    all['cnt_negative'] = neg['TICKER'] / all['TICKER']
    # quantile_df = pd.merge(quantile_df, all[['group','cnt_positive','cnt_negative']], how= 'left', on= 'group')

    pos = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] > 1].groupby('group')['PCA-GR_1D-A_1D'].mean().reset_index()
    neg = gr_df_tem[gr_df_tem['PCA-GR_1D-A_1D'] < 1].groupby('group')['PCA-GR_1D-A_1D'].mean().reset_index()

    pos.rename(columns= {'PCA-GR_1D-A_1D': 'pos_mean_r1D'}, inplace= True)
    neg.rename(columns= {'PCA-GR_1D-A_1D': 'neg_mean_r1D'}, inplace= True)

    all = pd.merge(all[['group','cnt_positive','cnt_negative']], pos, how= 'left', on= 'group')
    all = pd.merge(all, neg, how= 'left', on= 'group')
    all['kelly'] = - all['cnt_positive'] * (1- all['pos_mean_r1D']) / (all['cnt_negative'] * (1-all['neg_mean_r1D']))

    display(quantile_df[['group','count','mean','std','anlz_return','mean_count_ticker','eq1d_anlz_return']])
    display(all)

def break_from_percentage_in_bottom(df, bottom_threshold, database_version, evaluate):
    
    volm = 0.6
    start_date = '2011-01-01'
    end_date = '2022-12-31'

    df_volm = load_volm(database_version)
    indicator_list = ['PCA-GR_1D', 'PCA-RV_120D']
    df_volm = load_indicator_list(df_volm, database_version, indicator_list)
    df_cnt_volm = df_volm[df_volm['VALM-MA_70D-B_1D-RH'] > volm].groupby(['DATE_TRADING'])['PCA-RV_120D'].count().reset_index()
    df_cnt_bottom = df_volm[(df_volm['VALM-MA_70D-B_1D-RH'] > volm) & (df_volm['PCA-RV_120D'] < bottom_threshold)].groupby(['DATE_TRADING'])['PCA-RV_120D'].count().reset_index()
    df_cnt_volm.rename(columns = {'PCA-RV_120D':'cnt_volm'}, inplace = True)
    df_cnt_bottom.rename(columns = {'PCA-RV_120D':'cnt_bottom'}, inplace = True)

    df_cnt_volm = df_cnt_volm[(df_cnt_volm['DATE_TRADING'] > start_date) & (df_cnt_volm['DATE_TRADING'] < end_date)]
    df_cnt_bottom = df_cnt_bottom[(df_cnt_bottom['DATE_TRADING'] > start_date) & (df_cnt_bottom['DATE_TRADING'] < end_date)]
    df_cnt = pd.merge(df_cnt_volm, df_cnt_bottom, on= 'DATE_TRADING', how= 'left')
    df_cnt['percentage_in_bottom'] = df_cnt['cnt_bottom'] / df_cnt['cnt_volm']
    df_cnt['percentage_in_bottom_quantile'] = np.nan
    index  = df_cnt.index.values
    for i in index:
        df_cnt.loc[i,'percentage_in_bottom_quantile'] = df_cnt[df_cnt['percentage_in_bottom'] < df_cnt.loc[i,'percentage_in_bottom']]['DATE_TRADING'].count() / len(df_cnt['DATE_TRADING'])

    df.rename(columns = {'RETURN_PORTFOLIO':'daily_return'}, inplace = True)
    df_volm_06 = pd.merge(df[['DATE_TRADING','daily_return']], df_cnt[['DATE_TRADING','percentage_in_bottom_quantile']], how= 'left', on= 'DATE_TRADING')

    hypothesis_list = ['daily_return']
    break_list = ['percentage_in_bottom_quantile']

    df_volm_06['assign'] = 0

    index_values = df_volm_06['assign'].index.values

    for hypothesis in hypothesis_list:
        for break_choosen in break_list:
            df_volm_06[f'{hypothesis}'].fillna(value= 0, inplace= True)

            for i in index_values:
                if df_volm_06[f'{break_choosen}'].iloc[i] >= 1:
                    df_volm_06['assign'].iloc[i] = 0
                elif df_volm_06[f'{break_choosen}'].iloc[i] > 0.9:
                    df_volm_06['assign'].iloc[i] = 0
                elif df_volm_06[f'{break_choosen}'].iloc[i] > 0.8:
                    df_volm_06['assign'].iloc[i] = 0
                elif df_volm_06[f'{break_choosen}'].iloc[i] > 0.7:
                    df_volm_06['assign'].iloc[i] = 0
                elif df_volm_06[f'{break_choosen}'].iloc[i] > 0.6:
                    df_volm_06['assign'].iloc[i] = 0.5
                elif df_volm_06[f'{break_choosen}'].iloc[i] >= 0.5:
                    df_volm_06['assign'].iloc[i] = 1
                elif df_volm_06[f'{break_choosen}'].iloc[i] >= 0:
                    df_volm_06['assign'].iloc[i] = 1

            acc_return_adj_arr = []
            stock_nav_arr = []
            cash_arr = []

            acc_return_adj = 1
            stock_nav = 0
            cash = 1

            for index in index_values:
                acc_return_adj = stock_nav*(1 + df_volm_06[f'{hypothesis}'].loc[index]) + cash
                if df_volm_06['assign'].iloc[index] == df_volm_06['assign'].iloc[index - 1]:
                    stock_nav = stock_nav*(1 + df_volm_06[f'{hypothesis}'].loc[index])
                else:
                    stock_nav = acc_return_adj * df_volm_06['assign'].iloc[index]
                    cash = acc_return_adj - stock_nav
                acc_return_adj_arr.append(acc_return_adj)
                stock_nav_arr.append(stock_nav)
                cash_arr.append(cash)

            df_volm_06['acc_return_adj'] = acc_return_adj_arr
            df_volm_06['stock_nav'] = stock_nav_arr
            df_volm_06['cash'] = cash_arr

            # Kết quả khi chưa re-assign
            # print(f'\nKết quả của {hypothesis_choosen} khi chưa re-assign')
            # df_org = df_volm_06.loc[:,('DATE_TRADING',f'acc_{hypothesis_choosen}')]
            # df_org.rename(columns = {f'acc_{hypothesis_choosen}':'acc_return'}, inplace = True)
            # cft.evaluate_briefly(df_org)

            # Kết quả khi đã re-assign
            df_adj = df_volm_06.loc[:,('DATE_TRADING','acc_return_adj')]
            df_adj.rename(columns={'acc_return_adj':'acc_return'}, inplace= True)

            print(f'\nKết quả của {hypothesis} khi đã re-assign bằng {break_choosen}')
            if evaluate == 'full':
                evaluate_fully(df_adj, database_version)
            else:
                evaluate_briefly(df_adj, database_version)

def context_assign_create(df, context_assign):
    user = getpass.getuser()
    df_assign = pd.read_hdf(f'C:\\Users\\{user}\\OneDrive\\01.Investment\\9.Code\\0.database\\context_assign\\{context_assign}.h5')
    df_adj = pd.merge(df, df_assign, how= 'left', on ='DATE_TRADING')
    df_adj = df_adj.reset_index()
    df_adj.rename(columns= {'acc_return':'acc_return_ordinary', 'assign_y':'assign'}, inplace= True)

    index_values = df.index.values
    acc_return_adj_arr = []
    nav_stock_arr = []
    cash_adj_arr = []

    acc_return_adj = 1
    nav_stock = 0
    cash_adj = 1

    for index in index_values:
        if index == 0:
            acc_return_adj = 1
        else:
            acc_return_adj = nav_stock*(1 + df_adj['daily_return'].loc[index]) + cash_adj
            if df_adj['assign'].iloc[index] == df_adj['assign'].iloc[index - 1]:
                nav_stock = nav_stock*(1 + df_adj['daily_return'].loc[index])
            else:
                nav_stock = acc_return_adj * df_adj['assign'].iloc[index]
                cash_adj = acc_return_adj - nav_stock
        acc_return_adj_arr.append(acc_return_adj)
        nav_stock_arr.append(nav_stock)
        cash_adj_arr.append(cash_adj)

    df_adj['acc_return_adj'] = acc_return_adj_arr
    df_adj['nav_stock'] = nav_stock_arr
    df_adj['cash_adj'] = cash_adj_arr
    df_adj['daily_return_adj'] = df_adj['acc_return_adj'] / df_adj['acc_return_adj'].shift(1) - 1
    df_adj.rename(columns= {'daily_return':'daily_return_ordinary', 'daily_return_adj':'daily_return', 'acc_return_adj':'acc_return'}, inplace= True)

    return df_adj

def evaluate_indicator(df, indicator, time_lag, time_groupby):

    gr_df_tem = df.copy()

    # 1) Theo độ lớn của indicator thì gr_nD thế nào?
    print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
    gr_df_tem[f'{indicator}_quantile'] = pd.qcut(gr_df_tem[f'{indicator}'], q = 10, labels= False, duplicates='drop')
    quantile_df = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].describe().reset_index()
    
    quantile_df_prod = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
    quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
    quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator}_quantile', f'annualize_return']], how= 'left', on= f'{indicator}_quantile')

    display(quantile_df)
    
    sns.set(rc= {'figure.figsize': (8, 4)})
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= 'mean', alpha= 1, label= 'mean')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '25%', alpha= 1, label= '25%')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '50%', alpha= 1, label= '50%')
    sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '75%', alpha= 1, label= '75%')
    plt.xlabel(f'{indicator}_quantile')
    plt.ylabel(time_lag)
    plt.title(f'{indicator}_quantile, thì {time_lag} như thế nào?')
    plt.show()
    
    # 2) Độ lớn của indicator nhưng ở các năm khác nhau thì gr_nD thế nào?
    print(f'\nChia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào qua các năm')
    time_list = gr_df_tem[f'{time_groupby}'].unique()
    for time in time_list:
        quantile_df = gr_df_tem[gr_df_tem[f'{time_groupby}' == time]].groupby([f'{indicator}_quantile'])[f'{time_lag}'].describe().reset_index()
        quantile_df_prod = gr_df_tem[gr_df_tem[f'{time_groupby}'] == time].groupby([f'{indicator}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
        quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
        quantile_df = pd.merge(quantile_df[[f'{indicator}_quantile','count','mean','25%','50%','75%']], quantile_df_prod[[f'{indicator}_quantile', f'annualize_return']], how= 'left', on= f'{indicator}_quantile')
    
        sns.set(rc= {'figure.figsize': (8, 4)})
        sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= 'mean', alpha= 1, label= 'mean')
        sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '25%', alpha= 1, label= '25%')
        sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '50%', alpha= 1, label= '50%')
        sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '75%', alpha= 1, label= '75%')
        plt.xlabel(f'{indicator}_quantile')
        plt.ylabel(time_lag)
        plt.title(f'{indicator}_quantile, thì {time_lag} như thế nào?')
        plt.show()

# def evaluate_indicator_brief(df, indicator, time_lag, universe, date_start, date_end, valm, universe_rh, window_rank, window_ma, window_gr):

#     # print('#################################################################################################')
#     # print(f'\nKết quả evaluate {indicator} theo độ lớn của indicator')

#     rank_create(df, indicator = indicator, window = universe_rh, date_start =date_start, date_end = date_end, valm = valm)
#     ts_rank_create(df, indicator = indicator, window = window_rank)
#     ts_mean_create(df, indicator = indicator, window = window_ma)
#     ts_growth_create(df, indicator = indicator, window = window_gr)
#     rsi_create(df, indicator = indicator, window = window)

#     df = eval(f'{universe}_universe')(df,date_start,date_end,valm)
#     df = position_create(df, t3 = "false")
#     gr_df_tem = df[df['position'] == 1].copy()

#     # 1) evaluate indicator chính
#     # print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
#     gr_df_tem[f'{indicator}_quantile'] = pd.qcut(gr_df_tem[f'{indicator}'], q = 10, labels= False, duplicates='drop')
#     quantile_df = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].describe().reset_index()
    
#     quantile_df_prod = gr_df_tem.groupby([f'{indicator}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
#     quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
#     quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator}_quantile', f'annualize_return']], how= 'left', on= f'{indicator}_quantile')

#     tem = gr_df_tem.groupby(['DATE_TRADING',f'{indicator}_quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
#     tem_1 = tem.groupby([f'{indicator}_quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
#     tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
#     quantile_df = pd.merge(quantile_df, tem_1[[f'{indicator}_quantile', 'eq1d_anlz_return']], how= 'left', on= f'{indicator}_quantile')

#     # display(quantile_df)

#     fig, ax = plt.subplots()
#     sns.set(rc= {'figure.figsize': (8, 4)})
#     sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= 'mean', alpha= 1, label= 'mean')
#     sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '25%', alpha= 1, label= '25%')
#     sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '50%', alpha= 1, label= '50%')
#     sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= '75%', alpha= 1, label= '75%')
#     ax2 = ax.twinx()
#     sns.lineplot(data= quantile_df, x= f'{indicator}_quantile', y= 'eq1d_anlz_return', ax=ax2, alpha= 1, label= 'eq1d_anlz_return', color = 'purple')

#     plt.xlabel(f'{indicator}_quantile')
#     plt.ylabel(time_lag)
#     ax2.set(ylabel = 'eq1d_anlz_return')
#     plt.title(f'{indicator}_quantile, thì {time_lag} như thế nào?')
#     plt.show()

#     # 2) evaluate indicator-gr
#     # print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
#     indicator_gr = f'ts_return({indicator},{window_gr})'

#     gr_df_tem[f'{indicator_gr}_quantile'] = pd.qcut(gr_df_tem[f'{indicator_gr}'], q = 10, labels= False, duplicates='drop')
#     quantile_df = gr_df_tem.groupby([f'{indicator_gr}_quantile'])[f'{time_lag}'].describe().reset_index()
    
#     quantile_df_prod = gr_df_tem.groupby([f'{indicator_gr}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
#     quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
#     quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator_gr}_quantile', f'annualize_return']], how= 'left', on= f'{indicator_gr}_quantile')

#     tem = gr_df_tem.groupby(['DATE_TRADING',f'{indicator_gr}_quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
#     tem_1 = tem.groupby([f'{indicator_gr}_quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
#     tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
#     quantile_df = pd.merge(quantile_df, tem_1[[f'{indicator_gr}_quantile', 'eq1d_anlz_return']], how= 'left', on= f'{indicator_gr}_quantile')

#     # display(quantile_df)

#     fig, ax = plt.subplots()
#     sns.set(rc= {'figure.figsize': (8, 4)})
#     sns.lineplot(data= quantile_df, x= f'{indicator_gr}_quantile', y= 'mean', alpha= 1, label= 'mean')
#     sns.lineplot(data= quantile_df, x= f'{indicator_gr}_quantile', y= '25%', alpha= 1, label= '25%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_gr}_quantile', y= '50%', alpha= 1, label= '50%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_gr}_quantile', y= '75%', alpha= 1, label= '75%')
#     ax2 = ax.twinx()
#     sns.lineplot(data= quantile_df, x= f'{indicator_gr}_quantile', y= 'eq1d_anlz_return', ax=ax2, alpha= 1, label= 'eq1d_anlz_return', color = 'purple')

#     plt.xlabel(f'{indicator_gr}_quantile')
#     plt.ylabel(time_lag)
#     ax2.set(ylabel = 'eq1d_anlz_return')
#     plt.title(f'{indicator_gr}_quantile, thì {time_lag} như thế nào?')
#     plt.show()

#     # 3) evaluate indicator-ma
#     # print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
#     indicator_ma = f'ts_mean({indicator},{window_ma})'
    
#     gr_df_tem[f'{indicator_ma}_quantile'] = pd.qcut(gr_df_tem[f'{indicator_ma}'], q = 10, labels= False, duplicates='drop')
#     quantile_df = gr_df_tem.groupby([f'{indicator_ma}_quantile'])[f'{time_lag}'].describe().reset_index()
    
#     quantile_df_prod = gr_df_tem.groupby([f'{indicator_ma}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
#     quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
#     quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator_ma}_quantile', f'annualize_return']], how= 'left', on= f'{indicator_ma}_quantile')

#     tem = gr_df_tem.groupby(['DATE_TRADING',f'{indicator_ma}_quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
#     tem_1 = tem.groupby([f'{indicator_ma}_quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
#     tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
#     quantile_df = pd.merge(quantile_df, tem_1[[f'{indicator_ma}_quantile', 'eq1d_anlz_return']], how= 'left', on= f'{indicator_ma}_quantile')

#     # display(quantile_df)

#     fig, ax = plt.subplots()
#     sns.set(rc= {'figure.figsize': (8, 4)})
#     sns.lineplot(data= quantile_df, x= f'{indicator_ma}_quantile', y= 'mean', alpha= 1, label= 'mean')
#     sns.lineplot(data= quantile_df, x= f'{indicator_ma}_quantile', y= '25%', alpha= 1, label= '25%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_ma}_quantile', y= '50%', alpha= 1, label= '50%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_ma}_quantile', y= '75%', alpha= 1, label= '75%')
#     ax2 = ax.twinx()
#     sns.lineplot(data= quantile_df, x= f'{indicator_ma}_quantile', y= 'eq1d_anlz_return', ax=ax2, alpha= 1, label= 'eq1d_anlz_return', color = 'purple')

#     plt.xlabel(f'{indicator_ma}_quantile')
#     plt.ylabel(time_lag)
#     ax2.set(ylabel = 'eq1d_anlz_return')
#     plt.title(f'{indicator_ma}_quantile, thì {time_lag} như thế nào?')
#     plt.show()

#     # 4) evaluate indicator-rh
#     # print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
#     indicator_rh = f'rank({indicator},{universe_rh},xap)'
    
#     gr_df_tem[f'{indicator_rh}_quantile'] = pd.qcut(gr_df_tem[f'{indicator_rh}'], q = 10, labels= False, duplicates='drop')
#     quantile_df = gr_df_tem.groupby([f'{indicator_rh}_quantile'])[f'{time_lag}'].describe().reset_index()
    
#     quantile_df_prod = gr_df_tem.groupby([f'{indicator_rh}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
#     quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
#     quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator_rh}_quantile', f'annualize_return']], how= 'left', on= f'{indicator_rh}_quantile')

#     tem = gr_df_tem.groupby(['DATE_TRADING',f'{indicator_rh}_quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
#     tem_1 = tem.groupby([f'{indicator_rh}_quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
#     tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
#     quantile_df = pd.merge(quantile_df, tem_1[[f'{indicator_rh}_quantile', 'eq1d_anlz_return']], how= 'left', on= f'{indicator_rh}_quantile')

#     # display(quantile_df)

#     fig, ax = plt.subplots()
#     sns.set(rc= {'figure.figsize': (8, 4)})
#     sns.lineplot(data= quantile_df, x= f'{indicator_rh}_quantile', y= 'mean', alpha= 1, label= 'mean')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rh}_quantile', y= '25%', alpha= 1, label= '25%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rh}_quantile', y= '50%', alpha= 1, label= '50%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rh}_quantile', y= '75%', alpha= 1, label= '75%')
#     ax2 = ax.twinx()
#     sns.lineplot(data= quantile_df, x= f'{indicator_rh}_quantile', y= 'eq1d_anlz_return', ax=ax2, alpha= 1, label= 'eq1d_anlz_return', color = 'purple')

#     plt.xlabel(f'{indicator_rh}_quantile')
#     plt.ylabel(time_lag)
#     ax2.set(ylabel = 'eq1d_anlz_return')
#     plt.title(f'{indicator_rh}_quantile, thì {time_lag} như thế nào?')
#     plt.show()

#     # 4) evaluate indicator-rv
#     # print(f'\n1) Chia {indicator} thành 10 quantiles với độ lớn tăng dần, thì return sau {time_lag} thay đổi thế nào, chưa tách tập')
#     indicator_rv = f'ts_rank({indicator},{window_rank},xap)'
    
#     gr_df_tem[f'{indicator_rv}_quantile'] = pd.qcut(gr_df_tem[f'{indicator_rv}'], q = 10, labels= False, duplicates='drop')
#     quantile_df = gr_df_tem.groupby([f'{indicator_rv}_quantile'])[f'{time_lag}'].describe().reset_index()
    
#     quantile_df_prod = gr_df_tem.groupby([f'{indicator_rv}_quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
#     quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
#     quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'{indicator_rv}_quantile', f'annualize_return']], how= 'left', on= f'{indicator_rv}_quantile')

#     tem = gr_df_tem.groupby(['DATE_TRADING',f'{indicator_rv}_quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
#     tem_1 = tem.groupby([f'{indicator_rv}_quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
#     tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
#     quantile_df = pd.merge(quantile_df, tem_1[[f'{indicator_rv}_quantile', 'eq1d_anlz_return']], how= 'left', on= f'{indicator_rv}_quantile')

#     # display(quantile_df)

#     fig, ax = plt.subplots()
#     sns.set(rc= {'figure.figsize': (8, 4)})
#     sns.lineplot(data= quantile_df, x= f'{indicator_rv}_quantile', y= 'mean', alpha= 1, label= 'mean')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rv}_quantile', y= '25%', alpha= 1, label= '25%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rv}_quantile', y= '50%', alpha= 1, label= '50%')
#     sns.lineplot(data= quantile_df, x= f'{indicator_rv}_quantile', y= '75%', alpha= 1, label= '75%')
#     ax2 = ax.twinx()
#     sns.lineplot(data= quantile_df, x= f'{indicator_rv}_quantile', y= 'eq1d_anlz_return', ax=ax2, alpha= 1, label= 'eq1d_anlz_return', color = 'purple')

#     plt.xlabel(f'{indicator_rv}_quantile')
#     plt.ylabel(time_lag)
#     ax2.set(ylabel = 'eq1d_anlz_return')
#     plt.title(f'{indicator_rv}_quantile, thì {time_lag} như thế nào?')
#     plt.show()

def evaluate_indicator_brief_table(df, indicator, time_lag, universe, date_start, date_end, valm, param_valm, transform, param_transform):

    gr_df_tem = df.copy()
    indicator_list = [indicator]
    for t, p in zip(transform, param_transform):
        gr_df_tem[f'{t}({indicator},{p})'] = eval(f'{t}_create')(gr_df_tem, indicator = indicator, window = p)
        indicator_list.append(f'{t}({indicator},{p})')
    gr_df_tem = eval(f'{universe}_universe')(gr_df_tem,date_start,date_end,valm,param_valm)
    gr_df_tem = position_create(gr_df_tem, t3 = "false")
    gr_df_tem = gr_df_tem[(gr_df_tem['DATE_TRADING'] >= date_start) & (gr_df_tem['DATE_TRADING'] < date_end)].copy()
    indicator_type = ['original'] + transform
    number_date_trading = gr_df_tem['DATE_TRADING'].nunique()
    total_table = pd.DataFrame()
    # 1) evaluate indicator
    # các metric khi chia quantile và universe
    for i in range(0,len(indicator_list)):
        try:
            df_tem = gr_df_tem[['DATE_TRADING','TICKER',f'{indicator_list[i]}']].dropna()
            df_tem[f'{indicator_list[i]}'].replace([np.inf], 1e10, inplace=True)
            df_tem[f'{indicator_list[i]}'].replace([-np.inf], -1e10, inplace=True)
            result, bins = pd.qcut(df_tem[f'{indicator_list[i]}'], q = 10, labels= False, retbins= True, duplicates='drop')
            df_tem['quantile'] = pd.qcut(df_tem[f'{indicator_list[i]}'], q = 10, labels= False, duplicates='drop')
            # result, bins = pd.qcut(gr_df_tem[f'{indicator_list[i]}'], q = 10, labels= False, retbins= True, duplicates='drop')
            # gr_df_tem[f'quantile'] = pd.qcut(gr_df_tem[f'{indicator_list[i]}'], q = 10, labels= False, duplicates='drop')

            gr_df_tem = pd.merge( df_tem[['DATE_TRADING','TICKER', 'quantile']], gr_df_tem, how= 'left', on= ['DATE_TRADING','TICKER'])
            gr_df_tem['quantile'] = pd.to_numeric(gr_df_tem[f'quantile'], errors = 'coerce').astype('Int64')
            quantile_df = gr_df_tem[gr_df_tem['position'] == 1].groupby(['quantile'])[f'{time_lag}'].describe().reset_index()
            
            # quantile_df_prod = gr_df_tem[gr_df_tem['position'] == 1].groupby([f'quantile'])[f'{time_lag}'].apply(gmean_ignore_nan).reset_index()
            # quantile_df_prod[f'annualize_return'] = quantile_df_prod[f'{time_lag}']**250-1
            # quantile_df = pd.merge(quantile_df, quantile_df_prod[[f'quantile', f'annualize_return']], how= 'left', on= f'quantile')

            tem = gr_df_tem[gr_df_tem['position'] == 1].groupby(['DATE_TRADING','quantile'])['PCA-GR_1D-A_1D'].mean().reset_index()
            tem_1 = tem.groupby(['quantile'])['PCA-GR_1D-A_1D'].prod().reset_index()
            tem_1['eq1d_anlz_return'] = tem_1['PCA-GR_1D-A_1D']**(250/(tem['DATE_TRADING'].nunique()))-1
            quantile_df = pd.merge(quantile_df, tem_1[['quantile', 'eq1d_anlz_return']], how= 'left', on= f'quantile')
            quantile_df['mean_count_ticker'] = quantile_df['count'] / number_date_trading
            quantile_df['indicator'] = indicator_list[i]
            quantile_df['indicator_type'] = indicator_type[i]
            quantile_df['universe'] = universe
            quantile_df['lower_bound'] = 'na'
            quantile_df['upper_bound'] = 'na'
            quantile_list = np.sort(quantile_df['quantile'].unique())
            for j in quantile_list:
                quantile_df.loc[j,'lower_bound'] = bins[j]
                quantile_df.loc[j,'upper_bound'] = bins[j+1]
            quantile_df = quantile_df[['indicator', 'indicator_type', 'universe', 'quantile','lower_bound', 'upper_bound', 'mean_count_ticker','mean','std','eq1d_anlz_return']]
            total_table = pd.concat([total_table,quantile_df], ignore_index= True)
            gr_df_tem.drop('quantile', axis= 1, inplace= True)
        except:
            continue
    
    return total_table

def evaluate_hypothesis(df, database_version, date_start, date_end):

    date_count_ref_df = load_date_count_ref()
    df_date = df[(df['DATE_TRADING'] > date_start) & (df['DATE_TRADING'] < date_end)]['DATE_TRADING'].unique()
    df = pd.merge(df, date_count_ref_df, how= 'left', on='DATE_TRADING')

    # Tính ann_return
    annualized_return = (df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return'])**(1/(len(df_date)/250)) - 1
    acc_return = df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return']
    print(f'annualized_return {annualized_return}')
    print(f'acc_return {acc_return}')

    # Tính drawdown
    df['drawdown'] = df['acc_return'] / df['acc_return'].cummax() - 1
    max_drawdown = df['drawdown'].min()
    avg_drawdown = df['drawdown'].mean()
    quantile_95_drawdown = df['drawdown'].quantile(q=0.05)
    sum_drawdown = df['drawdown'].sum()

    print(f'max_drawdown {max_drawdown}')
    print(f'avg_drawdown {avg_drawdown}')
    print(f'95%_drawdown {quantile_95_drawdown}')
    print(f'Tổng drawdown {sum_drawdown}')

    # Tính std và sharpe_ratio
    df['return_1d'] = df['acc_return'] / df['acc_return'].shift(1)
    average_daily_return = (df['return_1d'] - 1).mean()
    daily_std = (df['return_1d'] - 1).std()
    annualized_sharpe_ratio = np.sqrt(252) * (average_daily_return) / daily_std
    print(f'Tính std daily return {daily_std}')
    print(f'sharpe_ratio {annualized_sharpe_ratio}')

    # Tính max_assign và max_margin
    max_assign = df['max_assign'].max()
    print(f'max_assign_for_a_ticker {max_assign}')
    max_margin = df['cash_to_nav_total'].min()
    print(f'max_margin {-max_margin}')
    

    # TÍnh return_by_year
    df_return_by_year = df.groupby('YEAR_STR')['return_1d'].prod() 
    print(f'return_by_year {df_return_by_year - 1}')

    # Tính tỉ lệ return dương qua các time_frame
    df_return_by_quarter = df.groupby('QUARTER_STR')['return_1d'].prod().reset_index()
    df_return_by_quarter.rename(columns= {'return_1d': 'quarter_return'}, inplace= True)
    cnt_quarter_return_positive = df_return_by_quarter[df_return_by_quarter['quarter_return'] > 1]['quarter_return'].count()
    cnt_quarter_return_positive_percentage = cnt_quarter_return_positive / df_return_by_quarter['quarter_return'].count()
    print(f'Tỉ lệ số quý có return dương {cnt_quarter_return_positive_percentage} ')
    quarter = df_return_by_quarter.quarter_return.describe().reset_index()

    df_return_by_month = df.groupby('MONTH_STR')['return_1d'].prod().reset_index()
    df_return_by_month.rename(columns= {'return_1d': 'month_return'}, inplace= True)
    cnt_month_return_positive = df_return_by_month[df_return_by_month['month_return'] > 1]['month_return'].count()
    cnt_month_return_positive_percentage = cnt_month_return_positive / df_return_by_month['month_return'].count()
    print(f'Tỉ lệ số tháng có return dương {cnt_month_return_positive_percentage} ')
    month = df_return_by_month.month_return.describe().reset_index()

    df_return_by_week = df.groupby('WEEK_STR')['return_1d'].prod().reset_index()
    df_return_by_week.rename(columns= {'return_1d': 'week_return'}, inplace= True)
    cnt_week_return_positive = df_return_by_week[df_return_by_week['week_return'] > 1]['week_return'].count()
    cnt_week_return_positive_percentage = cnt_week_return_positive / df_return_by_week['week_return'].count()
    print(f'Tỉ lệ số tuần có return dương {cnt_week_return_positive_percentage} ')
    week = df_return_by_week.week_return.describe().reset_index()

    df_return_by_day = df.copy()
    df_return_by_day.rename(columns= {'return_1d': 'day_return'}, inplace= True)
    cnt_day_return_positive = df_return_by_day[df_return_by_day['day_return'] > 1]['day_return'].count()
    cnt_day_return_positive_percentage = cnt_day_return_positive / df_return_by_day['day_return'].count()
    print(f'Tỉ lệ số ngày có return dương {cnt_day_return_positive_percentage} ')
    day = df_return_by_day.day_return.describe().reset_index()

    describe = pd.merge(quarter, month, how= 'left', on= 'index', suffixes= ('_quarter','_month'))
    describe = pd.merge(describe, week, how= 'left', on= 'index')
    describe = pd.merge(describe, day, how= 'left', on= 'index', suffixes= ('_week','_day'))
    display(describe)

    # Tính tỉ lệ alpha dương qua các time_frame
    try:
        indicator = 'MARKET_VNINDEX_PRICE_CLOSE-GR_1D'

        onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
        local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\Database\DATABASEv{database_version}")
        factor = get_factor_for_indicator(indicator, database_version)
        df_tem = pd.read_hdf(os.path.join(local_dtb_dir,f"I-{factor}",f'{indicator}.h5'))
        
        df = pd.merge(df, df_tem, how= 'left', on= 'DATE_TRADING')

        df_return_by_quarter_index = df.groupby('QUARTER_STR')['MARKET_VNINDEX_PRICE_CLOSE-GR_1D'].prod().reset_index()
        df_return_by_quarter_index.rename(columns= {'MARKET_VNINDEX_PRICE_CLOSE-GR_1D': 'quarter_return_index'}, inplace= True)
        df_return_by_quarter = pd.merge(df_return_by_quarter, df_return_by_quarter_index, how= 'left', on= 'QUARTER_STR')
        df_return_by_quarter['quarter_alpha'] = df_return_by_quarter['quarter_return'] - df_return_by_quarter['quarter_return_index']
        cnt_quarter_return_positive_percentage = df_return_by_quarter[df_return_by_quarter['quarter_alpha'] > 0]['quarter_alpha'].count()/df_return_by_quarter['quarter_return'].count()
        quarter_alpha = df_return_by_quarter.quarter_alpha.describe().reset_index()
        print(f'Số quý có alpha dương {cnt_quarter_return_positive_percentage}')

        df_return_by_month_index = df.groupby('MONTH_STR')['MARKET_VNINDEX_PRICE_CLOSE-GR_1D'].prod().reset_index()
        df_return_by_month_index.rename(columns= {'MARKET_VNINDEX_PRICE_CLOSE-GR_1D': 'month_return_index'}, inplace= True)
        df_return_by_month = pd.merge(df_return_by_month, df_return_by_month_index, how= 'left', on= 'MONTH_STR')
        df_return_by_month['month_alpha'] = df_return_by_month['month_return'] - df_return_by_month['month_return_index']
        cnt_month_return_positive_percentage = df_return_by_month[df_return_by_month['month_alpha'] > 0]['month_alpha'].count()/df_return_by_month['month_return'].count()
        month_alpha = df_return_by_month.month_alpha.describe().reset_index()
        print(f'Số tháng có alpha dương {cnt_month_return_positive_percentage}')

        df_return_by_week_index = df.groupby('WEEK_STR')['MARKET_VNINDEX_PRICE_CLOSE-GR_1D'].prod().reset_index()
        df_return_by_week_index.rename(columns= {'MARKET_VNINDEX_PRICE_CLOSE-GR_1D': 'week_return_index'}, inplace= True)
        df_return_by_week = pd.merge(df_return_by_week, df_return_by_week_index, how= 'left', on= 'WEEK_STR')
        df_return_by_week['week_alpha'] = df_return_by_week['week_return'] - df_return_by_week['week_return_index']
        cnt_week_return_positive_percentage = df_return_by_week[df_return_by_week['week_alpha'] > 0]['week_alpha'].count()/df_return_by_week['week_return'].count()
        week_alpha = df_return_by_week.week_alpha.describe().reset_index()
        print(f'Số tuần có alpha dương {cnt_week_return_positive_percentage}')

        df_return_by_day_index = df.copy()
        df_return_by_day_index.rename(columns= {'MARKET_VNINDEX_PRICE_CLOSE-GR_1D': 'day_return_index'}, inplace= True)
        df_return_by_day = pd.merge(df_return_by_day, df_return_by_day_index, how= 'left', on= 'DATE_TRADING')
        df_return_by_day['day_alpha'] = df_return_by_day['day_return'] - df_return_by_day['day_return_index']
        cnt_day_return_positive_percentage = df_return_by_day[df_return_by_day['day_alpha'] > 0]['day_alpha'].count()/df_return_by_day['day_return'].count()
        day_alpha = df_return_by_day.day_alpha.describe().reset_index()
        print(f'Số ngày có alpha dương {cnt_day_return_positive_percentage}')

        describe_alpha = pd.merge(quarter_alpha, month_alpha, how= 'left', on= 'index', suffixes= ('_quarter','_month'))
        describe_alpha = pd.merge(describe_alpha, week_alpha, how= 'left', on= 'index')
        describe_alpha = pd.merge(describe_alpha, day_alpha, how= 'left', on= 'index', suffixes= ('_week','_day'))
        display(describe_alpha)
    except:
        print('database có lỗi phần tính alpha')
    
    # tính ticker_count, cash, fee, turnover
    try:
        ticker_count = pd.DataFrame(df['ticker_count'].describe())
        cash_describe = pd.DataFrame(df['cash_to_nav_total'].describe())
        # display(ticker_count)
        # sns.scatterplot(data= df, x= 'DATE_TRADING', y= 'ticker_count')
        ticker_count_and_cash = pd.merge(ticker_count, cash_describe, left_index= True, right_index= True)
        print(f'ticker_count and cash theo năm')
        display(ticker_count_and_cash)
    except:
        print('eval không có ticker count')

    try:
        df['YEAR'] = df['DATE_TRADING'].dt.year
        df['fee'] =  df['nav_buy_to_nav'] * fee_buy + df['nav_sell_to_nav'] * fee_sell
        turnover = df.groupby('YEAR')['turnover'].sum().reset_index()
        fee = df.groupby('YEAR')['fee_relative'].sum().reset_index()
        fee_describe = pd.DataFrame(fee['fee_relative'].describe())
        turnover_describe = pd.DataFrame(turnover['turnover'].describe())
        fee_and_turnover = pd.merge(fee_describe, turnover_describe, left_index= True, right_index= True)
        print(f'fee và turnover theo năm')
        display(fee_and_turnover)
        
    except:
        print('eval không tính đc phí giao dịch')

    # fig, axes = plt.subplots(nrows= 3, ncols= 2, figsize = (10,10))
    fig, axes = plt.subplots(nrows= 3, ncols= 2, figsize = (10,10))
    sns.lineplot(data= df, x= 'DATE_TRADING', y= 'drawdown', ax= axes[0,0])
    sns.lineplot(data= df, x= 'DATE_TRADING', y= 'acc_return', ax= axes[0,1])
    sns.scatterplot(data= df_return_by_quarter, x= 'QUARTER_STR', y= 'quarter_return',ax= axes[1,0])
    try:
        sns.scatterplot(data= df_return_by_quarter, x= 'QUARTER_STR', y= 'quarter_alpha',ax= axes[1,1])
    finally:
        sns.lineplot(data= df, x= 'DATE_TRADING', y= 'max_assign',ax= axes[2,0])
        sns.lineplot(data= df, x= 'DATE_TRADING', y= 'cash_to_nav_total',ax= axes[2,1])

    axes[1,0].plot([0, 50], [1, 1], color="red")
    axes[1,1].plot([0, 50], [0, 0], color="red")
    # axes[2,1].plot([0, 50], [0, 0], color="red")
    # axes[1,1].plot([0, 150], [1, 1], color="red")
    # axes[2,0].plot([0, 50], [0, 0], color="red")
    # axes[2,1].plot([0, 150], [0, 0], color="red")
    plt.show()

def evaluate_hypothesis_brief(df, date_start, date_end):

    date_count_ref_df = load_date_count_ref()

    df_date = df[(df['DATE_TRADING'] > date_start) & (df['DATE_TRADING'] < date_end)]['DATE_TRADING'].unique()
    df = pd.merge(df, date_count_ref_df, how= 'left', on='DATE_TRADING')

    # Tính ann_return
    annualized_return = (df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return'])**(1/(len(df_date)/250)) - 1
    acc_return = df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return']
    print(f'annualized_return {annualized_return}')
    print(f'acc_return {acc_return}')

    # Tính drawdown
    df['drawdown'] = df['acc_return'] / df['acc_return'].cummax() - 1
    max_drawdown = df['drawdown'].min()
    avg_drawdown = df['drawdown'].mean()
    quantile_95_drawdown = df['drawdown'].quantile(q=0.05)
    sum_drawdown = df['drawdown'].sum()

    print(f'max_drawdown {max_drawdown}')
    print(f'avg_drawdown {avg_drawdown}')
    print(f'95%_drawdown {quantile_95_drawdown}')
    print(f'Tổng drawdown {sum_drawdown}')

    # Tính std và sharpe_ratio
    df['return_1d'] = df['acc_return'] / df['acc_return'].shift(1)
    average_daily_return = (df['return_1d'] - 1).mean()
    daily_std = (df['return_1d'] - 1).std()
    annualized_sharpe_ratio = np.sqrt(252) * (average_daily_return) / daily_std
    print(f'Tính std daily return {daily_std}')
    print(f'sharpe_ratio {annualized_sharpe_ratio}')
    
    # Tính max_assign, max_margin turnover bình quân
    max_assign = df['max_assign'].max()
    print(f'max_assign_for_a_ticker {max_assign}')
    max_margin = df['cash_to_nav_total'].min()
    print(f'max_margin {-max_margin}')
    
    try:
        ticker_count = df['ticker_count'].median()
        print(f'số ticker count median {ticker_count}')
        cash_describe = df['cash_to_nav_total'].median()
        print(f'cash_to_nav_total median {cash_describe}')
    except:
        print('eval không có ticker count\n')
    
    try:
        df['YEAR'] = df['DATE_TRADING'].dt.year
        df['fee'] =  df['nav_buy_to_nav'] * fee_buy + df['nav_sell_to_nav'] * fee_sell
        turnover = df.groupby('YEAR')['turnover'].sum().reset_index()
        fee = df.groupby('YEAR')['fee_relative'].sum().reset_index()
        fee_describe = fee['fee_relative'].median()
        turnover_describe = turnover['turnover'].median()
        print(f'turnover median theo năm {turnover_describe}')
        print(f'turnover median theo năm {fee_describe}')
    except:
        print('eval không tính đc phí giao dịch')

def evaluate_indicator_brief_visual(indicator_text, indicator_type, param_1_list_eval = [None], param_2_list_eval = [None], character_list = ['eq1d_anlz_return', 'mean', 'upper_bound', 'std', 'mean_count_ticker']):
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, r"Amethyst Invest\zUnsorted\File share\OnlyC\7. Indicator_findings\indicator")
    df = pd.read_excel(os.path.join(local_dtb_dir,f'{indicator_text}.xlsx'))
    matching_columns_in = [col for col in df.columns if "param_" in col]
    number_param = len(matching_columns_in)
    universe_list = df['universe'].unique()
    number_uninverse = len(universe_list)

    if number_param == 0:
        for character in character_list:
            fig, axes = plt.subplots(nrows= ((number_uninverse + 1)// 2), ncols= 2, figsize = (10, 5 * ((number_uninverse + 1)// 2)))
            plt.suptitle(f'{indicator_text}\n-{indicator_type}-{character}')
            for universe in range(0,len(universe_list)):
                    sns.lineplot(data= df[(df['universe'] == universe_list[universe]) & (df['indicator_type'] == indicator_type)], 
                                x= 'quantile', y= character, label = f'{universe_list[universe]}', ax= axes[universe // 2, universe % 2])
        
            for i in range(0, number_uninverse):
                axes[i // 2, i % 2].set_title(f'{universe_list[i]}')

    elif number_param == 1:
        param_1_list = param_1_list_eval
        for character in character_list:
            fig, axes = plt.subplots(nrows= ((number_uninverse + 1)// 2), ncols= 2, figsize = (10, 5 * ((number_uninverse + 1)// 2)))
            plt.suptitle(f'{indicator_text}\n-{indicator_type}-{character}')
            for universe in range(0,len(universe_list)):
                colors = cm.rainbow(np.linspace(0, 1, len(param_1_list)))
                for i in range(0, len(param_1_list)):
                    sns.lineplot(data= df[(df['universe'] == universe_list[universe]) & (df['param_1'] == param_1_list[i]) & (df['indicator_type'] == indicator_type)], 
                                x= 'quantile', y= character, label = f'{param_1_list[i]}', color = colors[i], ax= axes[universe // 2, universe % 2])
            for i in range(0, number_uninverse):
                axes[i // 2, i % 2].set_title(f'{universe_list[i]}')

    elif number_param == 2:
        param_1_list = param_1_list_eval
        param_2_list = param_2_list_eval
        for character in character_list:
            fig, axes = plt.subplots(nrows= ((number_uninverse + 1)// 2), ncols= 2, figsize = (10, 5 * ((number_uninverse + 1)// 2)))
            plt.suptitle(f'{indicator_text}\n-{indicator_type}-{character}')
            for universe in range(0,len(universe_list)):
                colors = cm.rainbow(np.linspace(0, 1, len(param_1_list) * len(param_2_list)))
                for k in range(0, len(param_2_list)):
                    for j in range(0, len(param_1_list)):
                        # sns.lineplot(data= df[(df['universe'] == universe_list[universe]) & (df['param_1'] == param_1_list[j]) & 
                        #                             (df['param_2'] == param_2_list[k]) & (df['indicator_type'] == indicator_type)], 
                        #                                     x= 'quantile', y= character, label = f'{param_1_list[j]}-{param_2_list[k]}-{universe_list[universe]}', color = colors[len(param_1_list) * (k-1) + j], ax= axes[universe // 2, universe % 2])
                        sns.lineplot(data= df[(df['universe'] == universe_list[universe]) & (df['param_1'] == param_1_list[j]) & 
                                                    (df['param_2'] == param_2_list[k]) & (df['indicator_type'] == indicator_type)], 
                                                            x= 'quantile', y= character, label = f'{param_1_list[j]}-{param_2_list[k]}', color = colors[len(param_1_list) * (k-1) + j], ax= axes[universe // 2, universe % 2])

            for i in range(0, number_uninverse):
                axes[i // 2, i % 2].set_title(f'{universe_list[i]}')


def evaluate_indicator_opportunity_quantile(indicator_text, eq1d_anlz_return, mean_count_ticker, method = 'greater'):
    
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, r"Amethyst Invest\zUnsorted\File share\OnlyC\7. Indicator_findings\indicator")
    total_table = pd.read_excel(os.path.join(local_dtb_dir,f'{indicator_text}.xlsx'))

    if method == 'greater':
        opportunity = total_table[(total_table['eq1d_anlz_return'] > eq1d_anlz_return)]
    elif method == 'smaller':
        opportunity = total_table[(total_table['eq1d_anlz_return'] < eq1d_anlz_return)]
    # matching_columns_in = [col for col in opportunity.columns if "param_" in col]
    param_columns = opportunity.filter(like='param_')
    try:
        opportunity['param'] = param_columns.apply(lambda row: row.tolist(), axis=1)
    except ValueError:
        pass
    opportunity = opportunity.reset_index(drop= True)
    index = opportunity.index.values
    max_index = max(index)
    opportunity_deal = pd.DataFrame()

    indicator_list = []
    indicator_type_list = []
    universe_list = []
    lower_bound_list = []
    upper_bound_list = []
    mean_count_ticker_list  = []
    param_list = []

    for i in index:
        if i == 0:
            indicator_opportunity = opportunity.loc[i,'indicator']
            indicator_type_opportunity = opportunity.loc[i,'indicator_type']
            universe_opportunity = opportunity.loc[i,'universe']
            lower_bound_opportunity = opportunity.loc[i,'lower_bound']
            param_opportunity = opportunity.loc[i,'param']
            mean_count_ticker_opportunity = opportunity.loc[i,'mean_count_ticker']

            indicator_list.append(indicator_opportunity)
            indicator_type_list.append(indicator_type_opportunity)
            universe_list.append(universe_opportunity)
            lower_bound_list.append(lower_bound_opportunity)
            param_list.append(param_opportunity)
            
            if i == max_index:
                upper_bound_opportunity = opportunity.loc[i,'upper_bound']
                upper_bound_list.append(upper_bound_opportunity)
                mean_count_ticker_list.append(mean_count_ticker_opportunity)

        elif (i > 0):
            filt = ((opportunity.loc[i, 'indicator'] == opportunity.loc[i - 1, 'indicator']) & 
            (opportunity.loc[i, 'universe'] == opportunity.loc[i - 1, 'universe']) & 
            (opportunity.loc[i, 'quantile'] - 1 == opportunity.loc[i - 1, 'quantile'])
            )

            if (filt == True):
                mean_count_ticker_opportunity = mean_count_ticker_opportunity + opportunity.loc[i,'mean_count_ticker']

            elif (filt == False):
                upper_bound_opportunity = opportunity.loc[i - 1,'upper_bound']
                upper_bound_list.append(upper_bound_opportunity)
                mean_count_ticker_list.append(mean_count_ticker_opportunity)

                indicator_opportunity = opportunity.loc[i,'indicator']
                indicator_type_opportunity = opportunity.loc[i,'indicator_type']
                universe_opportunity = opportunity.loc[i,'universe']
                lower_bound_opportunity = opportunity.loc[i,'lower_bound']
                param_opportunity = opportunity.loc[i,'param']
                mean_count_ticker_opportunity = opportunity.loc[i,'mean_count_ticker']

                indicator_list.append(indicator_opportunity)
                indicator_type_list.append(indicator_type_opportunity)
                universe_list.append(universe_opportunity)
                lower_bound_list.append(lower_bound_opportunity)
                param_list.append(param_opportunity)

            if i == max_index:
                upper_bound_opportunity = opportunity.loc[i,'upper_bound']
                upper_bound_list.append(upper_bound_opportunity)
                mean_count_ticker_list.append(mean_count_ticker_opportunity)

    opportunity_deal['indicator'] = indicator_list
    opportunity_deal['indicator_type'] = indicator_type_list
    opportunity_deal['universe'] = universe_list
    opportunity_deal['lower_bound'] = lower_bound_list
    opportunity_deal['upper_bound'] = upper_bound_list   
    opportunity_deal['mean_count_ticker'] = mean_count_ticker_list
    opportunity_deal['mean_count_ticker'] = opportunity_deal['mean_count_ticker'].round(decimals=0)
    opportunity_deal['param'] = param_list    
    opportunity_deal = opportunity_deal[opportunity_deal['mean_count_ticker'] >= mean_count_ticker]
    opportunity_deal['param_text'] = opportunity_deal['param'].apply(lambda x: ', '.join(map(str, x)))   
    
    indicator_type_df = opportunity_deal.groupby('indicator_type')['indicator'].count().reset_index()
    universe_df = opportunity_deal.groupby('universe')['indicator'].count().reset_index()
    param_df = opportunity_deal.groupby('param_text')['indicator'].count().reset_index()
    indicator_type_df = indicator_type_df.sort_values(by='indicator', ascending = False)
    universe_df = universe_df.sort_values(by='indicator', ascending = False)
    param_df = param_df.sort_values(by='indicator', ascending = False)
    display(indicator_type_df)
    display(universe_df)
    display(param_df)

    return opportunity_deal

def evaluate_indicator_time_median_value_one_param(indicator_text, database_version, time_groupby, universe, date_start, date_end, param_valm, valm, param_1_list):
    
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\\Database\\DATABASEv{database_version}\\tem\\cong")
    df_indicator = pd.read_hdf(os.path.join(local_dtb_dir,f'{indicator_text}.h5'))
    df_indicator = df_indicator.drop_duplicates(subset= ['TICKER','DATE_TRADING']).reset_index(drop= True)

    df = load_base_data(database_version = database_version, param_valm = param_valm)
    df = eval(f'{universe}_universe')(df, date_start = date_start, date_end = date_end, valm = valm, param_valm = param_valm)
    df_position = position_create(df, t3 = 'false')
    df_indicator = pd.merge(df_indicator, df_position[['DATE_TRADING','TICKER','MONTH_STR','QUARTER_STR','YEAR','position']], how= 'left', on= ['DATE_TRADING','TICKER'])
    df_groupby = df_indicator[df_position['position'] == 1].groupby(f'{time_groupby}').median().reset_index()
    df_groupby = df_groupby.reset_index()

    colors = cm.rainbow(np.linspace(0, 1, len(param_1_list)))

    for i in range(0,len(param_1_list)):
        indicator = indicator_text.format(param_1 = param_1_list[i])
        sns.lineplot(data = df_groupby, x= f'{time_groupby}', y= f'{indicator}', color = colors[i], label = param_1_list[i])

    return df_groupby

def evaluate_indicator_time_median_value_two_param(indicator_text, database_version, time_groupby, universe, date_start, date_end, param_valm, valm, param_1_list, param_2_list):
        
    onedrive_dir = os.path.expandvars("%OneDriveConsumer%")
    local_dtb_dir = os.path.join(onedrive_dir, f"Amethyst Invest\\Database\\DATABASEv{database_version}\\tem\\cong")
    df_indicator = pd.read_hdf(os.path.join(local_dtb_dir,f'{indicator_text}.h5'))
    df_indicator = df_indicator.drop_duplicates(subset= ['TICKER','DATE_TRADING']).reset_index(drop= True)

    df = load_base_data(database_version = database_version, param_valm = param_valm)
    df = eval(f'{universe}_universe')(df, date_start = date_start, date_end = date_end, valm = valm, param_valm = param_valm)
    df_position = position_create(df, t3 = 'false')
    df_indicator = pd.merge(df_indicator, df_position[['DATE_TRADING','TICKER','MONTH_STR','QUARTER_STR','YEAR','position']], how= 'left', on= ['DATE_TRADING','TICKER'])
    df_groupby = df_indicator[df_position['position'] == 1].groupby(f'{time_groupby}').median().reset_index()

    number_subplots = len(param_2_list)
    fig, axes = plt.subplots(nrows= ((number_subplots + 1)// 2), ncols= 2, figsize = (10, 5 * ((number_subplots + 1)// 2)))
    plt.suptitle(f'{indicator_text}\n-{time_groupby}_value-')
    for j in range(0,len(param_2_list)):
        colors = cm.rainbow(np.linspace(0, 1, len(param_1_list)))
        
        for i in range(0,len(param_1_list)):
            indicator = indicator_text.format(param_1 = param_1_list[i], param_2 = param_2_list[j])
            if number_subplots > 2:
                sns.lineplot(data = df_groupby, x= f'{time_groupby}', y= f'{indicator}', color = colors[i], ax= axes[(j // 2), j % 2],label = param_1_list[i])
                axes[j // 2, j % 2].set_title(f'Param_2: {param_2_list[j]}')
            elif number_subplots == 2:
                sns.lineplot(data = df_groupby, x= f'{time_groupby}', y= f'{indicator}', color = colors[i], ax= axes[j % 2],label = param_1_list[i])
                axes[j % 2].set_title(f'Param_2: {param_2_list[j]}')
            else:
                sns.lineplot(data = df_groupby, x= f'{time_groupby}', y= f'{indicator}', color = colors[i], label = param_1_list[i])

    return df_groupby

def evaluate_hypothesis_v1(df, database_version):
    
    date_list = sorted(df['DATE_TRADING'].unique())

    # return metric
    annualized_return = (df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return'])**(1/(len(date_list)/250)) - 1
    acc_return = df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return']
    df['yearly_return'] = df['daily_return'] + 1
    df['YEAR'] = df['DATE_TRADING'].dt.year
    df_return_by_year = df.groupby('YEAR')['yearly_return'].prod().reset_index()
    df_return_by_year['yearly_return'] = df_return_by_year['yearly_return'] - 1
    turnover = df.groupby('YEAR')['turnover'].sum().reset_index()
    turnover_median = turnover['turnover'].median()

    fee = df.groupby('YEAR')['fee_relative'].sum().reset_index()

    df_yearly = pd.merge(df_return_by_year, turnover, how= 'left', on= 'YEAR')
    df_yearly = pd.merge(df_yearly, fee, how= 'left', on= 'YEAR')
    df_yearly.set_index('YEAR', inplace = True)
    df_yearly_transpose = df_yearly.transpose()

    print(f'annualized_return {annualized_return}')
    print(f'acc_return {acc_return}')

    # Tính drawdown
    df['drawdown'] = df['acc_return'] / df['acc_return'].cummax() - 1
    max_drawdown = df['drawdown'].min()
    avg_drawdown = df['drawdown'].mean()
    quantile_95_drawdown = df['drawdown'].quantile(q=0.05)
    sum_drawdown = df['drawdown'].sum()

    print(f'max_drawdown {max_drawdown}')
    print(f'avg_drawdown {avg_drawdown}')
    print(f'95%_drawdown {quantile_95_drawdown}')
    print(f'Tổng drawdown {sum_drawdown}')

    # Tính std và sortino_ratio
    daily_std = (df['daily_return'] - 1).std()
    rf_rate_year = 7/100
    rf_rate_day = (rf_rate_year + 1) ** (1 / 250) - 1
    return_diff_rf = df['daily_return']
    downside_return = return_diff_rf[return_diff_rf < 0]
    downside_return_std = np.std(downside_return)
    portfolio_return_array = df['daily_return']
    sortino_ratio = (np.average(portfolio_return_array) - rf_rate_day) / downside_return_std * (250 ** 0.5)

    print(f'std daily return {daily_std}')
    print(f'sortino_ratio {sortino_ratio}')

    display(df_yearly_transpose)

    # cash, ticker_count, deal_length distribution
    cash_describe = pd.DataFrame(df['cash_to_nav_total'].describe())
    cash_median = df['cash_to_nav_total'].median()
    ticker_count_describe = pd.DataFrame(df['ticker_count'].describe())
    ticker_count_median = df['ticker_count'].median()
        # tính deal_length
    df_pca = load_pca(database_version=database_version)
    deal_df = pd.DataFrame()
    date_list = np.array(date_list)
    df_exploded = df[['DATE_TRADING','stock_list']].explode('stock_list')
    date_start = min(date_list)
    date_end = max(date_list)

    df_exploded = df_exploded.sort_values(by = ['stock_list','DATE_TRADING']).reset_index(drop = True)
    df_exploded['position'] = 1
    df_exploded.rename(columns = {'stock_list':'TICKER'}, inplace = True)
    df_exploded = pd.merge(df_pca[['DATE_TRADING','TICKER','PCA']], df_exploded, how= 'left', on= ['DATE_TRADING','TICKER'])
    df_exploded.fillna(value= 0, inplace= True)
    df_exploded = df_exploded[(df_exploded['DATE_TRADING'] >= date_start) & (df_exploded['DATE_TRADING'] <= date_end)].reset_index(drop= True)

    df_exploded['position_diff'] = np.where(df_exploded['TICKER'] == df_exploded['TICKER'].shift(1), df_exploded['position'] - df_exploded['position'].shift(1), np.nan)
    df_exploded = df_exploded[(df_exploded['position_diff'] != 0) | (df_exploded['position'] == 1) ].reset_index(drop= True)

    date_trading = df_exploded['DATE_TRADING'].values
    ticker = df_exploded['TICKER'].values
    position = df_exploded['position'].values
    pca_arr = df_exploded['PCA'].values

    ticker_arr = []
    date_start_arr = []
    date_end_arr = []
    pca_start_arr = []
    pca_end_arr = []

    for n in range(len(date_trading)):
        # print(n)
        if (n == 0):
            if (position[n] == 1):
                ticker_deal = ticker[n]
                date_start_deal = date_trading[n]
                pca_start_deal = pca_arr[n]
                ticker_arr.append(ticker_deal)
                date_start_arr.append(date_start_deal)
                pca_start_arr.append(pca_start_deal)
                # ticker_arr = np.array(ticker_arr, ticker_deal)
                # date_start_arr = np.array(date_start_arr, date_start_deal)
                # pca_start_arr = np.array(pca_start_arr, pca_start_deal)

        elif (n != 0):
            if (ticker[n] == ticker[n-1]):
                if (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 0) and (position[n-1] == 1):
                    date_end_deal = date_trading[n]
                    pca_end_deal = pca_arr[n]
                    date_end_arr.append(date_end_deal)  
                    pca_end_arr.append(pca_end_deal)

            elif (ticker[n] != ticker[n-1]):
                if (position[n-1] == 1) and ((position[n] == 0)):
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

                elif (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 1) and (position[n-1] == 1):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]

                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

        elif (n == (len(date_trading) - 1)) and (position[n] == 1):
            date_end_deal = date_trading[n]
            pca_end_deal = pca_arr[n]
            date_end_arr.append(date_end_deal)
            pca_end_arr.append(pca_end_deal)

    date_count = []

    for i in range(len(ticker_arr)):
        # date_count_deal = len([x for x in date_list if date_start_arr[i] < x <= date_end_arr[i]])
        # date_count_deal = date_list.index(date_end_arr[i]) - date_list.index(date_start_arr[i]) 
        date_count_deal = (np.where(date_list == date_end_arr[i])[0][0] if np.any(date_list == date_end_arr[i]) else -1) - (np.where(date_list == date_start_arr[i])[0][0] if np.any(date_list == date_start_arr[i]) else -1 )
        
        date_count.append(date_count_deal)

    deal_length_median = np.median(date_count)
    deal_df['TICKER'] = ticker_arr
    deal_df['deal_length'] = date_count
    deal_length = pd.DataFrame(deal_df['deal_length'].describe())

    # merge các distribution
    distribution = pd.merge(cash_describe, ticker_count_describe, left_index= True, right_index= True)
    distribution = pd.merge(distribution, deal_length, left_index= True, right_index= True)

    display(distribution)

    # Tính max_assign
    max_assign = df['max_assign'].max()
    nav_stock_to_nav = df['nav_stock_to_nav_arr'].values

    sorted_array = [sorted(i[:5], reverse= True) for i in nav_stock_to_nav]
    max_5_assign = [sum(i[:5]) for i in sorted_array]
    max_5_assign = max(max_5_assign)

    sorted_array = [sorted(i[:10], reverse= True) for i in nav_stock_to_nav]
    max_10_assign = [sum(i[:10]) for i in sorted_array]
    max_10_assign = max(max_10_assign)

    print(f'max_assign {max_assign}')
    print(f'max_5_assign {max_5_assign}')
    print(f'max_10_assign {max_10_assign}')

    sns.lineplot(data= df, x= 'DATE_TRADING', y= 'acc_return')
    plt.title('acc_return')
    plt.show()

    sns.lineplot(data= df, x= 'DATE_TRADING', y= 'drawdown')
    plt.title('drawdown')
    plt.show()

    return annualized_return, max_drawdown, daily_std, sortino_ratio, ticker_count_median, turnover_median, cash_median, deal_length_median

def evaluate_hypothesis_for_machine_v1(df, database_version):
    df_pca = load_pca(database_version= database_version)
    date_list = sorted(df['DATE_TRADING'].unique())

    # return metric
    annualized_return = (df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return'])**(1/(len(date_list)/250)) - 1
    # acc_return = df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return']
    df['yearly_return'] = df['daily_return'] + 1
    df['YEAR'] = df['DATE_TRADING'].dt.year
    turnover = df.groupby('YEAR')['turnover'].sum().reset_index()
    turnover_median = turnover['turnover'].median()

    # Tính drawdown
    df['drawdown'] = df['acc_return'] / df['acc_return'].cummax() - 1
    max_drawdown = df['drawdown'].min()
    # avg_drawdown = df['drawdown'].mean()
    # quantile_95_drawdown = df['drawdown'].quantile(q=0.05)
    # sum_drawdown = df['drawdown'].sum()

    # Tính std và sortino_ratio
    daily_std = (df['daily_return'] - 1).std()
    rf_rate_year = 7/100
    rf_rate_day = (rf_rate_year + 1) ** (1 / 250) - 1
    return_diff_rf = df['daily_return']
    downside_return = return_diff_rf[return_diff_rf < 0]
    downside_return_std = np.std(downside_return)
    portfolio_return_array = df['daily_return']
    sortino_ratio = (np.average(portfolio_return_array) - rf_rate_day) / downside_return_std * (250 ** 0.5)

    # cash, ticker_count distribution
    cash_median = df['cash_to_nav_total'].median()
    ticker_count_median = df['ticker_count'].median()

    # tính deal_length
    date_list = np.array(date_list)
    df_exploded = df[['DATE_TRADING','stock_list']].explode('stock_list')
    date_start = min(date_list)
    date_end = max(date_list)

    df_exploded = df_exploded.sort_values(by = ['stock_list','DATE_TRADING']).reset_index(drop = True)
    df_exploded['position'] = 1
    df_exploded.rename(columns = {'stock_list':'TICKER'}, inplace = True)
    df_exploded = pd.merge(df_pca[['DATE_TRADING','TICKER','PCA']], df_exploded, how= 'left', on= ['DATE_TRADING','TICKER'])
    df_exploded.fillna(value= 0, inplace= True)
    df_exploded = df_exploded[(df_exploded['DATE_TRADING'] >= date_start) & (df_exploded['DATE_TRADING'] <= date_end)].reset_index(drop= True)

    df_exploded['position_diff'] = np.where(df_exploded['TICKER'] == df_exploded['TICKER'].shift(1), df_exploded['position'] - df_exploded['position'].shift(1), np.nan)
    df_exploded = df_exploded[(df_exploded['position_diff'] != 0) | (df_exploded['position'] == 1) ].reset_index(drop= True)

    date_trading = df_exploded['DATE_TRADING'].values
    ticker = df_exploded['TICKER'].values
    position = df_exploded['position'].values
    pca_arr = df_exploded['PCA'].values

    ticker_arr = []
    date_start_arr = []
    date_end_arr = []
    pca_start_arr = []
    pca_end_arr = []

    for n in range(len(date_trading)):
        # print(n)
        if (n == 0):
            if (position[n] == 1):
                ticker_deal = ticker[n]
                date_start_deal = date_trading[n]
                pca_start_deal = pca_arr[n]
                ticker_arr.append(ticker_deal)
                date_start_arr.append(date_start_deal)
                pca_start_arr.append(pca_start_deal)

        elif (n != 0):
            if (ticker[n] == ticker[n-1]):
                if (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 0) and (position[n-1] == 1):
                    date_end_deal = date_trading[n]
                    pca_end_deal = pca_arr[n]
                    date_end_arr.append(date_end_deal)  
                    pca_end_arr.append(pca_end_deal)

            elif (ticker[n] != ticker[n-1]):
                if (position[n-1] == 1) and ((position[n] == 0)):
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

                elif (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 1) and (position[n-1] == 1):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]

                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

        elif (n == (len(date_trading) - 1)) and (position[n] == 1):
            date_end_deal = date_trading[n]
            pca_end_deal = pca_arr[n]
            date_end_arr.append(date_end_deal)
            pca_end_arr.append(pca_end_deal)

    date_count = []

    for i in range(len(ticker_arr)):
        date_count_deal = (np.where(date_list == date_end_arr[i])[0][0] if np.any(date_list == date_end_arr[i]) else -1) - (np.where(date_list == date_start_arr[i])[0][0] if np.any(date_list == date_start_arr[i]) else -1 )
        date_count.append(date_count_deal)

    deal_length_median = np.median(date_count)

    return annualized_return, max_drawdown, daily_std, sortino_ratio, ticker_count_median, turnover_median, cash_median, deal_length_median

def compare_position_analysis(df,threshold):
    position_compare = pd.DataFrame()
    cols = df.columns
    for col in cols:
        c = sum(df[col])
        for ano_col in [x for x in cols if x != col]:
            a = df[col] - df[ano_col]
            b = sum([x for x in a if x == 1])
            e = 1 - b/c
            row = pd.DataFrame({'indicator': [col],
                                'indicator_compare': [ano_col],
                                'in_group_1_not_in_group_2': [b],
                                'in_group_1': [c],
                                'ratio': [e]})
            position_compare = pd.concat([position_compare, row], ignore_index= True)
    number_of_row = position_compare.last_valid_index()
    number_of_row_pass_threshold = position_compare[position_compare['ratio'] < threshold].reset_index().last_valid_index()
    same_ratio = 1 - number_of_row_pass_threshold/number_of_row
    return same_ratio, position_compare

def assign_anh_em(df_anh, df_em, database_version, fee = True):
    df_assign = pd.merge(df_anh, df_em, how= 'left', on= ['DATE_TRADING'], suffixes= ('_df_anh','_df_em'))
    df_assign['daily_return'] = df_assign['daily_return_df_anh'] + df_assign['daily_return_df_em'] * df_assign['cash_to_nav_total_df_anh'].clip(lower=0)
    df_assign['cash'] = df_assign['cash_df_em'] * df_assign['cash_to_nav_total_df_anh'].clip(lower=0)
    df_assign['nav_stock'] = df_assign['nav_stock_df_anh'] + df_assign['nav_stock_df_em']
    df_assign['stock_list_not_unique'] = df_assign['stock_list_df_anh'] + df_assign['stock_list_df_em']
    df_assign['acc_return'] = (df_assign['daily_return']+1).cumprod()
    df_assign['cash_to_nav_total'] = df_assign['cash'] / df_assign['acc_return']
    # df_assign['nav_stock_df_anh_arr'] = df_assign['nav_stock_to_nav_df_anh'] * df_assign['acc_return_df_anh']

    # tính tỉ trọng từng cổ phiếu mỗi ngày
    nav_stock_to_nav_df_em_adj_arr = [None] * len(df_assign.index)
    for index in range(0, len(df_assign.index)):
        nav_stock_to_nav_df_em_adj_arr[index] = [x * df_assign.loc[index, 'cash_to_nav_total_df_anh'] for x in df_assign.loc[index, 'nav_stock_to_nav_arr_df_em']]

    df_assign['nav_stock_to_nav_df_em_adj_arr'] = nav_stock_to_nav_df_em_adj_arr
    df_assign['nav_stock_to_nav_not_unique_arr'] = df_assign['nav_stock_to_nav_arr_df_anh'] + df_assign['nav_stock_to_nav_df_em_adj_arr']

    nav_stock_to_nav_arr = [None] * len(df_assign.index)
    stock_list_arr = [None] * len(df_assign.index)

    for index in range(0,len(df_assign.index)):
        x = df_assign.loc[index,'stock_list_not_unique']
        y = df_assign.loc[index,'nav_stock_to_nav_not_unique_arr']
        result_dict = defaultdict(float)

        for i in range(len(x)):
            result_dict[x[i]] += y[i]
        result_x = list(result_dict.keys())
        result_y = [result_dict[key] for key in result_x]
        stock_list_arr[index] = result_x
        nav_stock_to_nav_arr[index] = result_y
        
    df_assign['nav_stock_to_nav_arr'] = nav_stock_to_nav_arr 
    df_assign['stock_list'] = stock_list_arr # tính tỉ trọng cổ phiếu mỗi ngày đến đây là hết

    # tính nav từng cổ phiếu tại mỗi ngày:
    nav_stock_arr = [None] * len(df_assign.index)
    for index in range(0, len(df_assign.index)):
        nav_stock_arr[index] = [x * df_assign.loc[index, 'acc_return'] for x in df_assign.loc[index, 'nav_stock_to_nav_arr']] # done

    # tính nav_buy_to_nav
    # chênh lệch giữa nav hm nay và nav hôm qua * r1d
    df_assign = trading_to_nav_calculate_function(df_assign, database_version)

    if fee == True:
        df_assign_after_fee = fee_create(df_assign)
    else:
        df_assign_after_fee = fee_create(df_assign, fee_buy= 0, fee_sell= 0)
    
    return df_assign_after_fee

def adj_assign_all_hypo_follow_function(df, df_adj, database_version, round, fee = True):
    
    df = pd.merge(df, df_adj, how = 'left', on= 'DATE_TRADING')
    df_assign_adj = pd.DataFrame()
    index = df.index.values
    delta_assign_adj = [None] * len(index)
    assign_adj = [None] * len(index)

    for i in index:
        if i == 0:
            delta_assign_adj[i] = 1 - df.loc[i, 'assign_adj']
            assign_adj[i] = df.loc[i, 'assign_adj']
        else:
            delta_assign_adj[i] = abs(df.loc[i, 'assign_adj'] - assign_adj[i-1])
            if delta_assign_adj[i] > round:
                assign_adj[i] = df.loc[i, 'assign_adj']
            else:
                assign_adj[i] = assign_adj[i-1]

    df['assign_adj'] = assign_adj
    # df_assign_adj['nav_stock'] = df['nav_stock'] * df['assign_adj']
    # df_assign_adj['cash'] = (1 - df['assign_adj'])* df['cash'] + df['cash']
    df_assign_adj['DATE_TRADING'] = df['DATE_TRADING']
    df_assign_adj['stock_list'] = df['stock_list']
    df_assign_adj['ticker_count'] = df['ticker_count']
    df_assign_adj['max_assign'] = df['max_assign'] * df['assign_adj']
    # df_assign_adj['nav_buy_to_nav'] = df['nav_buy_to_nav'] * df['assign_adj']
    # df_assign_adj['nav_sell_to_nav'] = df['nav_sell_to_nav'] * df['assign_adj']

    nav_buy_to_nav_arr = [None] * len(index)
    nav_sell_to_nav_arr = [None] * len(index)
    nav_stock_to_nav_arr = [None] * len(index)
    nav_stock_to_nav = [None] * len(index)

    for i in index:
        nav_buy_to_nav_arr[i] = [df.loc[i,'assign_adj'] * x for x in df.loc[i,'nav_buy_to_nav_arr']]
        nav_sell_to_nav_arr[i] = [df.loc[i,'assign_adj'] * x for x in df.loc[i,'nav_sell_to_nav_arr']]
        nav_stock_to_nav_arr[i] = [df.loc[i,'assign_adj'] * x for x in df.loc[i,'nav_stock_to_nav_arr']]
        nav_stock_to_nav[i] = sum(nav_stock_to_nav_arr[i])

    df_assign_adj['nav_buy_to_nav_arr'] = nav_buy_to_nav_arr
    df_assign_adj['nav_sell_to_nav_arr'] = nav_sell_to_nav_arr
    df_assign_adj['nav_stock_to_nav_arr'] = nav_stock_to_nav_arr
    df_assign_adj['nav_stock_to_nav'] = nav_stock_to_nav

    df_r1d = load_pca(database_version)
    indicator_list = ['PCA-GR_1D-A_1D']
    df_r1d = load_indicator_list(df_r1d, database_version, indicator_list)
    min_date = df['DATE_TRADING'].min()
    max_date = df['DATE_TRADING'].max()
    df_r1d = df_r1d[(df_r1d['DATE_TRADING'] >= min_date) & (df_r1d['DATE_TRADING'] <= max_date)]
    datetable = df_r1d.groupby('DATE_TRADING').agg({'TICKER': list, 'PCA-GR_1D-A_1D': list}).reset_index().reset_index()
    ticker_arr = datetable['TICKER'].values
    r1d_arr = datetable['PCA-GR_1D-A_1D'].values

    daily_return = [None] * len(index)
    daily_return[0] = 0
    for i in range(len(index)-1):
        if len(df_assign_adj.loc[i, 'stock_list']) == 0:
            daily_return_tem = 0  
            daily_return[i+1] = 0

        else:
            # daily_return_tem = [None] * len(df_assign_adj.loc[i, 'stock_list'])
            daily_return_tem = []
            for j in range(len(df_assign_adj.loc[i, 'stock_list'])):
                index_ticker = ticker_arr[i].index(df_assign_adj.loc[i, 'stock_list'][j])
                daily_return_tem.append((r1d_arr[i][index_ticker] - 1) * df_assign_adj.loc[i, 'nav_stock_to_nav_arr'][j])
            daily_return[i+1] = sum(daily_return_tem)

    df_assign_adj['daily_return'] = daily_return
    df_assign_adj['acc_return'] = (df_assign_adj['daily_return'] + 1).cumprod()
    df_assign_adj['nav_stock'] = df_assign_adj['acc_return'] * df_assign_adj['nav_stock_to_nav']
    df_assign_adj['cash'] = df_assign_adj['acc_return'] - df_assign_adj['nav_stock']
    df_assign_adj['cash_to_nav_total'] = df_assign_adj['cash'] / df_assign_adj['acc_return']
    df_assign_adj['daily_return_absolute'] = df_assign_adj['acc_return'] - df_assign_adj['acc_return'].shift(1)
    df_assign_adj['daily_return_absolute'].fillna(value= 0, inplace= True)

    df_assign_adj = trading_to_nav_calculate_function(df_assign_adj, database_version)

    if fee == True:
        df_assign_adj_after_fee = fee_create(df_assign_adj)
        return df_assign_adj_after_fee
    else:
        df_assign_adj_after_fee = fee_create(df_assign_adj, fee_buy= 0, fee_sell= 0)
        return df_assign_adj_after_fee

def evaluate_hypothesis_for_compare_2_hypothesis(df, database_version):
    date_list = sorted(df['DATE_TRADING'].unique())

    # return metric
    annualized_return = (df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return'])**(1/(len(date_list)/250)) - 1
    acc_return = df.loc[(max(df[df['acc_return'] > 0].index.values)),'acc_return']
    df['yearly_return'] = df['daily_return'] + 1
    df['YEAR'] = df['DATE_TRADING'].dt.year
    df_return_by_year = df.groupby('YEAR')['yearly_return'].prod().reset_index()
    df_return_by_year['yearly_return'] = df_return_by_year['yearly_return'] - 1
    turnover = df.groupby('YEAR')['turnover'].sum().reset_index()
    turnover_median = turnover['turnover'].median()

    fee = df.groupby('YEAR')['fee_relative'].sum().reset_index()

    df_yearly = pd.merge(df_return_by_year, turnover, how= 'left', on= 'YEAR')
    df_yearly = pd.merge(df_yearly, fee, how= 'left', on= 'YEAR')
    df_yearly.set_index('YEAR', inplace = True)
    df_yearly_transpose = df_yearly.transpose()

    # Tính drawdown
    df['drawdown'] = df['acc_return'] / df['acc_return'].cummax() - 1
    max_drawdown = df['drawdown'].min()
    avg_drawdown = df['drawdown'].mean()
    quantile_95_drawdown = df['drawdown'].quantile(q=0.05)
    sum_drawdown = df['drawdown'].sum()

    # Tính std và sortino_ratio
    daily_std = (df['daily_return'] - 1).std()
    rf_rate_year = 7/100
    rf_rate_day = (rf_rate_year + 1) ** (1 / 250) - 1
    return_diff_rf = df['daily_return']
    downside_return = return_diff_rf[return_diff_rf < 0]
    downside_return_std = np.std(downside_return)
    portfolio_return_array = df['daily_return']
    sortino_ratio = (np.average(portfolio_return_array) - rf_rate_day) / downside_return_std * (250 ** 0.5)



    # cash, ticker_count, deal_length distribution
    cash_describe = pd.DataFrame(df['cash_to_nav_total'].describe())
    cash_median = df['cash_to_nav_total'].median()
    ticker_count_describe = pd.DataFrame(df['ticker_count'].describe())
    ticker_count_median = df['ticker_count'].median()
        # tính deal_length
    df_pca = load_pca(database_version=database_version)
    deal_df = pd.DataFrame()
    date_list = np.array(date_list)
    df_exploded = df[['DATE_TRADING','stock_list']].explode('stock_list')
    date_start = min(date_list)
    date_end = max(date_list)

    df_exploded = df_exploded.sort_values(by = ['stock_list','DATE_TRADING']).reset_index(drop = True)
    df_exploded['position'] = 1
    df_exploded.rename(columns = {'stock_list':'TICKER'}, inplace = True)
    df_exploded = pd.merge(df_pca[['DATE_TRADING','TICKER','PCA']], df_exploded, how= 'left', on= ['DATE_TRADING','TICKER'])
    df_exploded.fillna(value= 0, inplace= True)
    df_exploded = df_exploded[(df_exploded['DATE_TRADING'] >= date_start) & (df_exploded['DATE_TRADING'] <= date_end)].reset_index(drop= True)

    df_exploded['position_diff'] = np.where(df_exploded['TICKER'] == df_exploded['TICKER'].shift(1), df_exploded['position'] - df_exploded['position'].shift(1), np.nan)
    df_exploded = df_exploded[(df_exploded['position_diff'] != 0) | (df_exploded['position'] == 1) ].reset_index(drop= True)

    date_trading = df_exploded['DATE_TRADING'].values
    ticker = df_exploded['TICKER'].values
    position = df_exploded['position'].values
    pca_arr = df_exploded['PCA'].values

    ticker_arr = []
    date_start_arr = []
    date_end_arr = []
    pca_start_arr = []
    pca_end_arr = []

    for n in range(len(date_trading)):
        # print(n)
        if (n == 0):
            if (position[n] == 1):
                ticker_deal = ticker[n]
                date_start_deal = date_trading[n]
                pca_start_deal = pca_arr[n]
                ticker_arr.append(ticker_deal)
                date_start_arr.append(date_start_deal)
                pca_start_arr.append(pca_start_deal)
                # ticker_arr = np.array(ticker_arr, ticker_deal)
                # date_start_arr = np.array(date_start_arr, date_start_deal)
                # pca_start_arr = np.array(pca_start_arr, pca_start_deal)

        elif (n != 0):
            if (ticker[n] == ticker[n-1]):
                if (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 0) and (position[n-1] == 1):
                    date_end_deal = date_trading[n]
                    pca_end_deal = pca_arr[n]
                    date_end_arr.append(date_end_deal)  
                    pca_end_arr.append(pca_end_deal)

            elif (ticker[n] != ticker[n-1]):
                if (position[n-1] == 1) and ((position[n] == 0)):
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

                elif (position[n] == 1) and (position[n-1] == 0):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)

                elif (position[n] == 1) and (position[n-1] == 1):
                    ticker_deal = ticker[n]
                    date_start_deal = date_trading[n]
                    pca_start_deal = pca_arr[n]
                    date_end_deal = date_trading[n-1]
                    pca_end_deal = pca_arr[n-1]

                    ticker_arr.append(ticker_deal)
                    date_start_arr.append(date_start_deal)
                    pca_start_arr.append(pca_start_deal)
                    date_end_arr.append(date_end_deal)
                    pca_end_arr.append(pca_end_deal)

        elif (n == (len(date_trading) - 1)) and (position[n] == 1):
            date_end_deal = date_trading[n]
            pca_end_deal = pca_arr[n]
            date_end_arr.append(date_end_deal)
            pca_end_arr.append(pca_end_deal)

    date_count = []

    for i in range(len(ticker_arr)):
        # date_count_deal = len([x for x in date_list if date_start_arr[i] < x <= date_end_arr[i]])
        # date_count_deal = date_list.index(date_end_arr[i]) - date_list.index(date_start_arr[i]) 
        date_count_deal = (np.where(date_list == date_end_arr[i])[0][0] if np.any(date_list == date_end_arr[i]) else -1) - (np.where(date_list == date_start_arr[i])[0][0] if np.any(date_list == date_start_arr[i]) else -1 )
        
        date_count.append(date_count_deal)

    deal_length_median = np.median(date_count)
    deal_df['TICKER'] = ticker_arr
    deal_df['deal_length'] = date_count
    deal_length = pd.DataFrame(deal_df['deal_length'].describe())

    # merge các distribution
    distribution = pd.merge(cash_describe, ticker_count_describe, left_index= True, right_index= True)
    distribution = pd.merge(distribution, deal_length, left_index= True, right_index= True)

    # Tính max_assign
    max_assign = df['max_assign'].max()
    nav_stock_to_nav = df['nav_stock_to_nav_arr'].values

    sorted_array = [sorted(i[:5], reverse= True) for i in nav_stock_to_nav]
    max_5_assign = [sum(i[:5]) for i in sorted_array]
    max_5_assign = max(max_5_assign)

    sorted_array = [sorted(i[:10], reverse= True) for i in nav_stock_to_nav]
    max_10_assign = [sum(i[:10]) for i in sorted_array]
    max_10_assign = max(max_10_assign)


    return df, df_yearly_transpose, distribution, annualized_return, acc_return, max_drawdown, avg_drawdown, quantile_95_drawdown, sum_drawdown, daily_std, sortino_ratio, 
    
def evaluate_2_hypothesis(df1, df2, database_version, n = 120):
    df, df_yearly_transpose, distribution, annualized_return, acc_return, max_drawdown, avg_drawdown, quantile_95_drawdown, sum_drawdown, daily_std, sortino_ratio = evaluate_hypothesis_for_compare_2_hypothesis(df1, database_version)
    df_2, df_yearly_transpose_2, distribution_2, annualized_return_2, acc_return_2, max_drawdown_2, avg_drawdown_2, quantile_95_drawdown_2, sum_drawdown_2, daily_std_2, sortino_ratio_2 = evaluate_hypothesis_for_compare_2_hypothesis(df2, database_version)

    data = {'hypothesis': ['hypothesis_1', 'hypothesis_2'],
            'annualized_return': [annualized_return, annualized_return_2],
            'acc_return': [acc_return, acc_return_2],
            'max_drawdown': [max_drawdown, max_drawdown_2],
            'avg_drawdown': [avg_drawdown, avg_drawdown_2],
            'quantile_95_drawdown': [quantile_95_drawdown, quantile_95_drawdown_2],
            'sum_drawdown': [sum_drawdown, sum_drawdown_2],
            'daily_std': [daily_std, daily_std_2],
            'sortino_ratio': [sortino_ratio, sortino_ratio_2]
            }
    data = pd.DataFrame(data)
    display(data)

    print('yearly_metric_hypothesis_1')
    display(df_yearly_transpose)
    print('yearly_metric_hypothesis_2')
    display(df_yearly_transpose_2)
    print('distribution_metric_hypothesis_1')
    display(distribution)
    print('distribution_metric_hypothesis_2')
    display(distribution_2)
    df_merge = pd.merge(df,df_2, on= 'DATE_TRADING', how= 'left', suffixes=('_1', '_2'))

    sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= 'acc_return_1', label = 'hypothesis_1')
    sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= 'acc_return_2', label = 'hypothesis_2')
    plt.title('acc_return')
    plt.show()

    sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= 'drawdown_1', label = 'hypothesis_1')
    sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= 'drawdown_2', label = 'hypothesis_2')
    plt.title('drawdown')
    plt.show()

    if n > 0:
        df1[f'return_trailing_{n}d'] = evaluate_return_trailing(df1, n)
        df1[f'drawdown_trailing_{n}d'] = evaluate_drawdown_trailing(df1, n)

        df2[f'return_trailing_{n}d'] = evaluate_return_trailing(df2, n)
        df2[f'drawdown_trailing_{n}d'] = evaluate_drawdown_trailing(df2, n)

        df_merge = pd.merge(df1,df2, on= 'DATE_TRADING', how= 'left', suffixes=('_1', '_2'))

        sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= f'return_trailing_{n}d_1', label = 'hypothesis_1')
        sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= f'return_trailing_{n}d_2', label = 'hypothesis_2')
        plt.title(f'return_trailing_{n}d')
        plt.show()

        sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= f'drawdown_trailing_{n}d_1', label = 'hypothesis_1')
        sns.lineplot(data= df_merge, x= 'DATE_TRADING', y= f'drawdown_trailing_{n}d_2', label = 'hypothesis_2')
        plt.title(f'drawdown_trailing_{n}d')
        plt.show()

def evaluate_return_trailing(df, n, dislay_chart = False):
    df[f'return_trailing_{n}d'] = df['acc_return'] / df['acc_return'].shift(n)
    if dislay_chart == True:
        plt.figure(figsize= (20, 6))
        sns.lineplot(data= df, x= 'DATE_TRADING', y= f'return_trailing_{n}d')
        plt.title(f'return_trailing_{n}d')
        plt.show()
    return df[f'return_trailing_{n}d']

def evaluate_drawdown_trailing(df, n, dislay_chart = False):
    arr = [None] * len(df.index.values)
    for i in df.index.values:
        if i > n:
            df_rolling = df[(df['DATE_TRADING'] > df.loc[i-n,'DATE_TRADING']) & (df['DATE_TRADING'] <= df.loc[i,'DATE_TRADING'])]
            df_rolling[f'acc_return_ath_{n}d'] = df_rolling['acc_return'].cummax()
            x = df_rolling.loc[i, 'acc_return'] / df_rolling.loc[i,f'acc_return_ath_{n}d'] - 1
            arr[i] = x
        else:
            df_rolling = df[(df['DATE_TRADING'] <= df.loc[i,'DATE_TRADING'])]
            df_rolling[f'acc_return_ath_{n}d'] = df_rolling['acc_return'].cummax()
            x = df_rolling.loc[i, 'acc_return'] / df_rolling.loc[i,f'acc_return_ath_{n}d'] - 1
            arr[i] = x  
    df[f'drawdown_trailing_{n}d'] = arr
    if dislay_chart == True:
        plt.figure(figsize= (20, 6))
        sns.lineplot(data= df, x= 'DATE_TRADING', y= f'drawdown_trailing_{n}d')
        plt.title(f'drawdown_trailing_{n}d')
        plt.show()
    return df[f'drawdown_trailing_{n}d']

