import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)  
import os
import re
from tqdm import tqdm

def load_claim_auto(directory, skip_rows=13, lhnv = None):
    # Regular expression to find a four-digit year in the file name
    year_pattern = re.compile(r'\b(\d{4})\b')

    # List to keep track of the names of the DataFrames stored as globals
    global_df_names = []

    # Iterate through each file in the specified directory
    for file in sorted(os.listdir(directory)):
        if file.endswith('.xlsx') and not file.startswith('~$'):
            
            # Find the year in the file name
            match = year_pattern.search(file)
            if match:
                year = match.group(1)
                file_path = os.path.join(directory, file)
                try:
                    """ IMPORT DATA"""
                    print(f"\n\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n--------------------------------------------------------------------------\nImporting: {file}")
                    # Load and clean data specifying the engine
                    df = pd.read_excel(file_path, header=None, skiprows=skip_rows, engine='openpyxl')
                    df.drop(df.columns[-1], axis = 1, inplace = True)  # remove na col at the end

                    # Dynamically determine headers based on the first non-empty cell per column
                    headers = []
                    for col in df.columns:
                        if pd.notna(df.iloc[1, col]):
                            headers.append(df.iloc[1, col])
                        elif pd.notna(df.iloc[0, col]) and pd.isna(df.iloc[1, col]):
                            headers.append(df.iloc[0, col])
                        else:
                            print(f'No headers found for {col}')

                    # Set the determined headers as column names
                    df.columns = headers
                    df = df.drop([0, 1])
                    df.reset_index(drop = True, inplace=True)
                    print(f'   Rows = {df.shape[0]}')
                    # print(f'Columns = {df.shape[1]}')
            
            
                    """ RENAME COLUMNS"""
                    print("--------------------------------------------------------------------------\nRenaming Columns:")
                    df_clm_dict = {
                        'mã đơn vị quản lý': 'MA_DVI',
                        'Mã đơn vị xử lý': 'MA_DVI_XL',
                        'Mã khai thác': 'MA_KT',
                        'Mã khách hàng': 'MA_KH',
                        'Số hồ sơ': 'SO_HSBT',
                        'Ngày mở HSBT': 'NGAY_MO_HSBT',
                        'Ngày thông báo': 'NGAY_THONG_BAO',
                        'Ngày xảy ra': 'NGAY_XAY_RA',
                        'Số ngày tồn': 'SO_NGAY_TON',
                        'Ngày giải quyết': 'NGAY_GIAI_QUYET',
                        'Phòng': 'PHONG_BT',
                        'Cán bộ bồi thường': 'CAN_BO_BT',
                        'Nghiệp vụ': 'MA_LHNV',
                        'Tên LHNV': 'TEN_LHNV',
                        'Số hợp đồng': 'SO_HD',
                        'Tên khách hàng': 'TEN_KH',
                        'Địa chỉ': 'DIA_CHI',
                        'Nguồn KT': 'NGUON_KT',
                        'Số GCN': 'SO_GCN',
                        'Biển xe': 'SO_BIEN_XE',
                        'Số khung/Số máy': 'SO_KHUNG/SO_MAY',
                        'Đối tượng bảo hiểm': 'TEN_DTBH',
                        'Tuổi xe': 'TUOI_XE',
                        'Ngày cấp': 'NGAY_CAP',
                        'Ngày HL': 'NGAY_HL',
                        'Ngày KT': 'NGAY_KT',
                        'Mã NT': 'MA_NGUYEN_TE',
                        'Số tiền bảo hiểm': 'STBH',
                        'Phí bảo hiểm VNĐ': 'PHI_BH',
                        'Nhóm': 'NHOM_XE', 
                        'Loại xe': 'LOAI_XE',
                        'Nguyên nhân': 'NGUYEN_NHAN_BT',
                        'Số tiền tổn thất': 'STTT',
                        'Số tiền bồi thường': 'STBT', 
                        'Ngày thanh toán bồi thường': 'NGAY_TT_BT',
                        'Gara': 'GARA',
                        'Hạch toán': 'HACH_TOAN',
                        'Ghi chú': 'GHI_CHU'
                    }

                    df.rename(columns={col: df_clm_dict[col] for col in df.columns if col in df_clm_dict}, inplace=True)

                    
                    """ SEPARATE SO MAY and SO KHUNG"""
                    print("--------------------------------------------------------------------------\nSeparating SO MAY/SO KHUNG:")
                    df[['SO_KHUNG', 'SO_MAY']] = df['SO_KHUNG/SO_MAY'].str.split('/', expand=True)
                    df.drop('SO_KHUNG/SO_MAY', axis = 1, inplace = True)
                    
                        
                    """ REMOVE UNNECESSARY COLUMNS"""
                    print("--------------------------------------------------------------------------\nRemoving Unneeded Columns:")
                    removed_cols = [
                        'Lĩnh vực kinh doanh',
                        'Cán bộ cấp đơn',
                        'Tổng giảm trừ', 
                        'STT',
                        'Số CV KN',
                        'Ngày hồ sơ đầy đủ', 
                        'Khu vực', 
                        'Điện thoại', 
                        'Danh mục cơ sở', 
                        'Email', 
                        'Số tiền bảo hiểm đưa vào tái',  
                        'Ngày thanh toán phí',
                        'Kiểu ĐBH', 
                        'Tỷ lệ ĐBH', 
                        'Thu đòi đồng BH', 
                        'Tỷ lệ tái CĐ', 
                        'Thu đòi tái bảo hiểm CĐ', 
                        'Tỷ lệ tái TT', 
                        'Thu đòi tái bảo hiểm TT',
                        'Giảm trừ tỷ lệ bảo hiểm',
                        'Giảm trừ khấu hao',
                        'Giảm trừ chế tài',
                        'Giảm trừ khác',
                        'Miễn thường',
                        'Thu hồi bồi thường',
                        'Phí giám định'
                    ]

                    # Removing columns, check if the columns exist
                    for col in removed_cols:
                        if col in df.columns:
                            df.drop(columns=col, inplace=True)
                        else:
                            print(f"   Column {col} not found in DataFrame.")                       


                    """ FILTER FOR LHNV"""
                    if lhnv:
                        print("--------------------------------------------------------------------------\nFiltering for LHNV:")    
                        rows_b4 = df.shape[0]    
                        df = df[df['MA_LHNV'] == lhnv]
                        print(f'   Removed: {(rows_b4 - df.shape[0]):,.0f} Rows, ({((rows_b4 - df.shape[0])/rows_b4*100):.2f}%)')


                    """ CONVERT DATE COLUMNS"""           
                    print("--------------------------------------------------------------------------\nReformatting Date Cols:")
                    dates_columns = [
                        "NGAY_MO_HSBT",
                        "NGAY_THONG_BAO",
                        "NGAY_XAY_RA",
                        "NGAY_GIAI_QUYET",
                        "NGAY_CAP",
                        "NGAY_HL",
                        "NGAY_KT",
                        "NGAY_TT_BT"
                    ]

                    for dates_col in dates_columns:
                        if dates_col in df.columns:  # Ensure column exists before converting
                            original_na_count = df[dates_col].isna().sum()
                            df[dates_col] = pd.to_datetime(df[dates_col], errors='coerce', dayfirst=True)
                            new_na_count = df[dates_col].isna().sum()
                            detected_errors = new_na_count - original_na_count
                            if detected_errors > 0:
                                print(f"   Detected {detected_errors} Incorrect Dates in {dates_col}")
                        else:
                            print(f"   Column {dates_col} not found in DataFrame.")


                    """ CONVERT NUMERICAL COLUMNS"""
                    print("--------------------------------------------------------------------------\nReformatting Num Cols:")
                    num_columns = [
                        'TUOI_XE',
                        'STBH',
                        'PHI_BH',
                        'STTT',
                        'STBT'
                    ]
                    
                    for num_col in num_columns:
                        if num_col in df.columns:  # Ensure column exists before converting
                            original_na_count = df[num_col].isna().sum()
                            df[num_col] = pd.to_numeric(df[num_col], errors='coerce')
                            new_na_count = df[num_col].isna().sum()
                            detected_errors = new_na_count - original_na_count
                            if detected_errors > 0:
                                print(f"   Detected {detected_errors} Incorrect Values in {num_col}")
                        else:
                            print(f"   Column {num_col} not found in DataFrame.")
                    
                    
                    # """ PROCESS DUPLICATED/COINSURED ROWS """
                    # print("--------------------------------------------------------------------------\nProcessing Dup/Coins Rows:")
                    # """ Step 1 - Remove Duplicated Transactions and Aggregate """
                    # _nrows_bf1 = df.shape[0]
                    # _clms_bf1 = df['STBT'].sum()
                    # # Identify duplicates that need to be summed
                    # duplicates_to_sum = df.duplicated(subset=['MA_DVI', 'SO_HSBT', 'STBT'], keep=False)
                    # df_duplicates = df[duplicates_to_sum]

                    # # Aggregate the data for duplicates
                    # df_agg = df_duplicates.groupby(['MA_DVI', 'SO_HSBT']).agg({
                    #     'STBT': 'sum'
                    # }).reset_index()

                    # # Remove the original duplicated rows from df
                    # df = df[~duplicates_to_sum]

                    # # Append aggregated results back to the main DataFrame
                    # df = pd.concat([df, df_agg], ignore_index=True)

                    # print(f"Step 1 - Remove Duplicates\n   -Removed {(_nrows_bf1 - df.shape[0]):,.0f} Rows\n   -Change in Tot Claims = {(_clms_bf1 - df['STBT'].sum()):,.0f} ({((_clms_bf1 - df['STBT'].sum())/_clms_bf1*100):,.0f}%)")

                    # """ Step 2 - Aggregate Claims with Multiple Transactions into One"""  # Policies with same Claim ID, department ID, and different Claim amounts 
                    # _nrows_bf2 = df.shape[0]
                    # _clms_bf2 = df['STBT'].sum()
                    # df['HACH_TOAN'] = df['HACH_TOAN'].astype(bool)
                    # df_many_trans = df[df.duplicated(subset=['MA_DVI', 'SO_HSBT'], keep = False)]
                    # df_many_trans_agg = df_many_trans.groupby(by = 'SO_HSBT')[['STBT']].sum()
                    # _many_trans_chuaht = df.duplicated(subset=['MA_DVI', 'SO_HSBT'], keep = False) & ~df["HACH_TOAN"]

                    # df = df[~_many_trans_chuaht] # Bo nhung dong trung va chua HT (giu da HT lam cot chinh)

                    # for index, row in df_many_trans_agg.iterrows():
                    #     SO_HSBT = index
                    #     STBT = row['STBT']

                    #     df.loc[df['SO_HSBT'] == SO_HSBT, ['STBT']] = STBT

                    # print(f"Step 2 - Adjust for Multiple Claims\n   -Removed {(_nrows_bf2 - df.shape[0]):,.0f} Rows\n   -Change in Tot Claims = {(_clms_bf2 - df['STBT'].sum()):,.0f} ({((_clms_bf2 - df['STBT'].sum())/_clms_bf2*100):,.0f}%)")

                    # """ Step 3 - Aggregate Claims with Internal Coinsurance into One """  # Poclies with same Claim ID, different Department ID
                    # _nrows_bf3 = df.shape[0]
                    # _clms_bf3 = df['STBT'].sum()
                    # df["IS_MAIN"] = df.apply(lambda x: x["SO_HSBT"][:3] == x["MA_DVI"], axis=1)

                    # df_many_qly = df[df.duplicated(subset=['SO_HSBT'], keep = False)]
                    # df_many_qly_agg = df_many_qly.groupby(by = 'SO_HSBT')[['STBT']].sum()
                    # _many_qly_notmain = df.duplicated(subset=['SO_HSBT'], keep = False) & ~df["IS_MAIN"]

                    # df = df[~_many_qly_notmain] # Bo nhung dong trung va khong phai dvi qly chinh 

                    # for index, row in df_many_qly_agg.iterrows():
                    #     SO_HSBT = index
                    #     STBT = row['STBT']

                    #     df.loc[df['SO_HSBT'] == SO_HSBT, ['STBT']] = STBT

                    # print(f"Step 3 - Adjust for Internal Insurance\n   -Removed {(_nrows_bf3 - df.shape[0]):,.0f} Rows\n   -Change in Tot Claims = {(_clms_bf3 - df['STBT'].sum()):,.0f} ({((_clms_bf3 - df['STBT'].sum())/_clms_bf3*100):,.0f}%)")

                       
                        
                    """ FILTER OUT TEST ROWS """
                    print("--------------------------------------------------------------------------\nFiltering Test Rows:")
                    rows_b4 = df.shape[0]
                    claims_b4 = df['STBT'].sum()
                    df = df[~(df['NGAY_TT_BT'].isna() & (df['STBT'] <= 1000))]  
                    print(f"   Removed {(rows_b4 - df.shape[0]):,.0f} Rows\n   Change in Tot Claims = {(claims_b4 - df['STBT'].sum()):,.0f} ({((claims_b4 - df['STBT'].sum())/claims_b4*100):,.0f}%)")
                        
                    
                    """ REMOVE ROWs WITH MISSING EFF DATE """
                    print("--------------------------------------------------------------------------\nRemoving Rows Missing NGAY_HL:")    
                    rows_b4 = df.shape[0]    
                    df = df[df['NGAY_HL'].notna()]
                    print(f'   Removed: {(rows_b4 - df.shape[0]):,.0f} Rows, ({((rows_b4 - df.shape[0])/rows_b4*100):.2f}%)')
                    
                    
                    " STANDARDIZE PLATE IDs"
                    print("--------------------------------------------------------------------------\nStandardizing SO_BIEN_XE:")    
                    pattern = r'^\d{2}[A-Za-z]\d{4,5}$' 
                    _copy = df['SO_BIEN_XE'].copy()
                    df.loc[:,'SO_BIEN_XE'] = df['SO_BIEN_XE'].str.replace('[^a-zA-Z0-9]', '', regex=True)
                    df.loc[:,'SO_BIEN_XE'] = df['SO_BIEN_XE'].str.strip().str.upper()
                    df.loc[df['SO_BIEN_XE'] == '', 'SO_BIEN_XE'] = pd.NA
                    df.loc[~df['SO_BIEN_XE'].str.match(pattern, na = False), 'SO_BIEN_XE'] = pd.NA
                    
                    print(f'   Changed: {sum(df['SO_BIEN_XE'] == _copy)} values')
                    print(f'   Converted: {df['SO_BIEN_XE'].isna().sum() - _copy.isna().sum()} to NAs')
                    del _copy
                    
                    
                    """ PRINT EFF_YEAR COUNTS IN EACH DF"""
                    print("--------------------------------------------------------------------------\nEff Year Count:")
                    df['NAM_HL'] = df['NGAY_HL'].dt.year 
                    print(f"Effective Year Count in CY{year}: {df['NAM_HL'].value_counts()}")
                        
                    
                    """ SAVE DF TO GLOBAL VARIABLE"""
                    print("--------------------------------------------------------------------------\nSaving DF:")
                    # Assign DataFrame to a global variable dynamically using the year
                    df_name = f'df_clm_{year}'
                    globals()[df_name] = df
                    global_df_names.append(df_name)
                    print(f"Summary of CY{year}:\n   -NUM CLAIMS = {df.shape[0]:,.0f}\n   -TOTAL CLAIMS = {df['STBT'].sum():,.0f}")
                    print('--------------------------------------------------------------------------\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                    
                except Exception as e:
                    print(f"Failed to process {file}: {e}")
            else:
                print(f"No year found in the file name {file}")

    # Print all global DataFrame names created
    print("\n\n\n==========================================================================\n==========================================================================\nSuccessfully Imported:", ", ".join(global_df_names))
    
    """ CONCAT INTO ONE DF"""
    all_dataframes = [globals()[name] for name in global_df_names if name in globals()]
    df_clm = pd.concat(all_dataframes, ignore_index=True)
    print(f"   Total Rows = {df_clm.shape[0]:,.0f}\n   Total Claims = {df_clm['STBT'].sum():,.0f}")
    
    print("==========================================================================\n==========================================================================")
    for name in global_df_names:
        del globals()[name]
        
    global_df_names.clear()
    
    return df_clm

