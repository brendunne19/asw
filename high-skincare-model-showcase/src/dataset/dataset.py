import src.utils as utils

import pandas as pd
import my_blob as blob

class GenerateDataset:
    def __init__(self, MonthParams):
        
        self.MonthParams = MonthParams
    
    
    def run_sql_prediction_proc(self, MonthParams) -> None:

        """Run sql proc that prepares table of data. Needs update from TODOS in README"""

        con = utils.get_ADM_connection()
        cursor = con.cursor()

        cursor.callproc('mfr_high_skincare_model_data_prediction_auto', [MonthParams.month_start, MonthParams.month_end])

        con.close()


    def run_sql_training_proc(self, MonthParams) -> None:

        """Run sql proc that prepares table of data. Needs update from TODOS in README"""

        con = utils.get_ADM_connection()
        cursor = con.cursor()

        cursor.callproc('mfr_high_skincare_model_data_auto', [MonthParams.month_start, MonthParams.month_end])

        con.close()

    
    def get_training_data(self, MonthParams) -> pd.DataFrame:

        """Collect and return final dataframe from sql proc that does have the high_skincare_flag
         and upload it to the blob."""
        
        con = utils.get_ADM_connection()
        cursor = con.cursor()

        cursor.execute('select * from bdunne.mfr_high_skincare_model_training_auto')
        df = pd.DataFrame(
            data=cursor.fetchall(), 
            columns=[desc[0].lower() for desc in cursor.description]
        )

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/raw/{MonthParams.month_start}_to_{MonthParams.month_end}_raw_high_data.csv', 
                              f'data/raw/{MonthParams.month_start}_to_{MonthParams.month_end}_raw_high_data.csv',
                              df)
                                           
        return df
    

    def get_prediction_data(self, MonthParams) -> pd.DataFrame:

        """Collect and return data from sql proc that doesn't have the high_skincare_flag and 
        upload it to the blob."""

        con = utils.get_ADM_connection()
        cursor = con.cursor()

        cursor.execute('select * from bdunne.mfr_high_skincare_model_prediction_auto')
        df = pd.DataFrame(
            data=cursor.fetchall(), 
            columns=[desc[0].lower() for desc in cursor.description]
        )

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/raw/{MonthParams.month_start}_to_{MonthParams.month_end}_raw_high_data.csv', 
                              f'data/raw/{MonthParams.month_start}_to_{MonthParams.month_end}_raw_high_data.csv',
                              df)
                                           
        return df


    def table_does_not_exist_error_fix(self) -> None:

        """If we receive a table does not exist error from the sql proc, 
        we attempt to drop and create all 3 tables temporarily, 
        and then retry run_sql_proc().
        """

        pass

    
    def table_already_exists_error_fix(self) -> None:

        """If we receive a table does already exists error from the sql proc, 
        we attempt to drop and create all 3 tables temporarily, 
        and then retry run_sql_proc().
        """

        pass