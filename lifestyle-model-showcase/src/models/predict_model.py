# local files
from conf.core import config as conf
from src.utils import *

# proprietary imports
import my_oracle as ora
import my_blob as blob

# global imports
import pandas as pd
import numpy as np
from datetime import date
import os
from sklearn.preprocessing import StandardScaler
import pickle

class MonthParams:

    """Define the parameters for each monthly run."""

    def __init__(self, month_idnt, month_name, model_month_label) -> None:
  
        self.bu_key = conf.bu_key
        self.bu_code = conf.bu_code
        self.month_idnt = month_idnt
        self.month_label = str(month_name) + str(month_idnt)[2:4]
        self.model_month_label = model_month_label
        self.max_mth_idnt = str(int(self.month_idnt - 1)) if str(self.month_idnt)[4:] != '01' else str(int(self.month_idnt - 89)) 
        self.rfm_date = '01-' + str(month_name) + '-' + str(month_idnt)[:4]
        self.model_label = conf.model_label
        self.seed = 42 # random seed for reproducibility
        self.age_max_date = self.rfm_date
        self.period_length = conf.period_length
        self.output_table_name = f'{self.bu_code}_lseg_output_d_{self.month_label}'
        self.siebel_table_name = f'{self.bu_code}_lseg_output_d_for_siebel_{self.month_label}'

# this originates from make_dataset.ipynb
def run_script(table_name, MonthParams):

    parameters = {    
        'bu_code' : MonthParams.bu_code,
        'bu_key' : MonthParams.bu_key,
        'month_label' : MonthParams.month_label,
        'rfm_date' : MonthParams.rfm_date,
        'max_mth_idnt' : MonthParams.max_mth_idnt,
        'period_length' : MonthParams.period_length
        }
    
    # Open sql template and populate with parameters
    sql = open('src/data/sql_templates/'+table_name+'.sql', 'r').read()
    sql = sql.format(**parameters)
    # Write copy to path
    with open('src/data/populated_sql/'+table_name+'_'+str(date.today())+'.sql', 'w') as file:
        file.write(sql)
        
    # Set up connection and sql commands
    sql_commands = sql.split(';')
    sql_commands.pop()
    cur = ora.get_oracle_connection('CRMBMAP')
    
    # Run sql script
    for command in sql_commands:
        execute_sql_allow_drops_to_fail(cur, command)


class ClassificationProcess:

    """A class for creating the features, making transformations, then running the classification."""

    def __init__(self, MonthParams):

        self.MonthParams = MonthParams

        # load blob files
        self.df = ora.get_oracle_data('CRMBMAP', f"select * from {MonthParams.bu_code}_lseg_mem_f_{MonthParams.month_label}")

    def build_features(self, MonthParams) -> None:

        """Prepare data by replacing NaN/inf values and general cleaning of data"""

        df = self.df

        # remove rows where total_sales is null or zero
        df = df[~df['tot_sales'].isna()]
        df = df[df['tot_sales'] > 0]

        # for categories not shopped, can just fill with zeros
        cols_with_nulls = ['fra_wom_sales', 'fra_men_sales', 'mup_eye_sales', 'mup_fac_sales', 'mup_lip_sales',
                   'skc_wom_sales', 'gif_set_sel_sales', 'prv_lab_sales']
        for col in cols_with_nulls:
            df[col] = df[col].fillna(0)

        # Create core KPIs
        df['atv'] = df['tot_sales'] / df['tot_trxs']
        df['acv'] = df['tot_sales']
        df['atf'] = df['tot_trxs']
        df['ppu'] = df['tot_sales'] / df['tot_items']

        # Turn category features into category share
        cat_share_cols = cols_with_nulls.copy()
        for col in cat_share_cols:
            df[col] = df[col] / df['tot_sales']

        # remove rows where items <= 0
        df = df[df['tot_items'] > 0]

        # coerce contact_key data type to object
        df['contact_key'] = df['contact_key'].astype('object')

        # drop extra columns
        df = df.drop(['tot_sales', 'tot_trxs', 'tot_items'], axis = 1)

        blob.upload_dataframe_to_blob(f'lifestyle-model/data/interim/{MonthParams.bu_code}/{MonthParams.bu_code}_lseg_test_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv', 
                              f'data/interim/{MonthParams.bu_code}_lseg_test_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv'
                              , df)

    def prep_data_for_prediction(self, MonthParams) -> None:

        "Trasnform data for classification and split into training and test sets, upsampling if necessary."

        df = blob.download_dataframe_from_blob(f'lifestyle-model/data/interim/{MonthParams.bu_code}/{MonthParams.bu_code}_lseg_test_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv', 
                              f'data/interim/{MonthParams.bu_code}_lseg_test_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv')

        # remove and save male shoppers
        self.male_shoppers = df[df['gen_m_flag'] == 1].copy()
        df = df[df['gen_m_flag'] == 0]

        # extract contact_keys and drop unneeded columns
        self.contacts_new_bu = df[['contact_key']]
        df = df.drop(['contact_key', 'gen_m_flag'], axis = 1)

        # scale core KPI features
        cols_to_scale = ['atv', 'acv', 'atf', 'ppu']
        scaler_new_bu = StandardScaler()
        scaler_new_bu.fit(df[cols_to_scale].copy())

        scaled_new_bu = pd.DataFrame(
            scaler_new_bu.transform(df[cols_to_scale].copy()),
            columns = cols_to_scale
        )

        for col in cols_to_scale:
            df[col] = np.array(scaled_new_bu[col])

        self.final_df = df
        

    def model_predict_and_upload(self, MonthParams) -> None:

        "Use model trained on MFR to predict for this BU."

        contacts_new_bu = self.contacts_new_bu
        male_shoppers = self.male_shoppers

        # get model trained on MFR 
        os.chdir(r"D:\ds-projects\segmentation\lifestyle-segmentation\mfr\mce-mit-training")
        with open(f'models/lgbm_{MonthParams.model_label}_{MonthParams.model_month_label}.pkl', 'rb') as buff:
            model = pickle.load(buff)

        preds = model.predict(self.final_df)
        
        contacts_new_bu['pred'] = preds
        male_shoppers['pred'] = 6

        contacts_new_bu = pd.concat([contacts_new_bu, male_shoppers[['contact_key', 'pred']]], ignore_index = True)

        # upload predictions
        os.chdir(fr"D:\ds-projects\segmentation\lifestyle-segmentation\{MonthParams.bu_code}")
        blob.upload_dataframe_to_blob(f'lifestyle-model/data/processed/{MonthParams.bu_code}/{MonthParams.bu_code}_lseg_pred_d_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv', 
                              f'data/processed/{MonthParams.bu_code}_lseg_pred_d_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                              contacts_new_bu)