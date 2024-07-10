from conf.core import config as conf
from conf.creds import my_creds

import cx_Oracle

class MonthParams:

    """Define the parameters for each monthly run."""

    def __init__(self, month_start, month_end) -> None:
  
        self.bu_key = conf.bu_key
        self.bu_code = conf.bu_code
        self.month_start = month_start
        self.month_end = month_end
        self.model_label = conf.model_label
        self.seed = 42 # random seed for reproducibility
        self.output_table_name = f'mfr_high_skincare_output_{self.month_end}'


def get_ADM_connection():
    
    dsnStr = cx_Oracle.makedsn(my_creds['server_name'], my_creds['port'], service_name=my_creds['service'])
    con = cx_Oracle.connect(user=my_creds['username'], password=my_creds['password'], dsn=dsnStr)

    return con