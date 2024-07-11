from datetime import date, datetime, timedelta

import cx_Oracle
import my_oracle_extension as orae
import pandas as pd
from dateutil.relativedelta import FR, relativedelta


def get_mth_name(fiscal_mth_idnt: str) -> str:

    """Get the first 3 letters of the current fiscal month."""

    query = f"""select 
        distinct substr(fiscal_mth_desc, 0, 3)
    from
        crm_target.b_time
    where
        fiscal_mth_idnt = {fiscal_mth_idnt}"""

    try:
        month_name = orae.smart_execute_query(query=query)
    
    except Exception as e:
            raise e
    
    return month_name.iloc[0,0]


def drop_adm_table_if_exists(cur: cx_Oracle.Cursor, table: str) -> None:

    """Drop ADM table if it exists."""

    try:
        cur.execute("DROP TABLE {}".format(table))
        

    except cx_Oracle.DatabaseError as e:

        # Pass any failed drops - there are some by design
        if str(e) == "ORA-00942: table or view does not exist":
            print("Passing following error: \n", e)
            
            pass
        else:
            raise e


def execute_sql_allow_drops_to_fail(cur: cx_Oracle.Cursor, sql_command: str) -> None:

    """Execute a SQL command and continue if a drop fails."""

    try:
        cur.execute(sql_command)
        
    except cx_Oracle.DatabaseError as e:
        if str(e) == "ORA-00942: table or view does not exist":
            print("Passing following error: \n", e)
            
            pass
        else:
            raise e


def split_dataframe(df: pd.DataFrame, chunk_size: int) -> list:

    """A class for splitting a dataframe into a list of dataframes based on
    a specified row number of each chunk."""

    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i * chunk_size : (i + 1) * chunk_size])

    return chunks
