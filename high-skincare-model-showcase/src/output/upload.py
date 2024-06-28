import src.utils as utils

import cx_Oracle
import csv
from loguru import logger

class UploadResults:

    def create_output_table(self, MonthParams) -> None:

        """Create empty table to export output to in ADM."""

        # drop table if exists
        drop_query = f"DROP TABLE BDUNNE.{MonthParams.output_table_name}"

        con = utils.get_ADM_connection()
        cursor = con.cursor()

        try:
            
            cursor.execute(drop_query)
            con.commit()
        
        except cx_Oracle.DatabaseError as e:

            # Pass any failed drops - there are some by design
            if str(e) == "ORA-00942: table or view does not exist":
                logger.info("Passing following error: \n" + e)
                pass
            else:
                raise e
        
        # create empty output table
        create_query = f"""CREATE TABLE BDUNNE.{MonthParams.output_table_name} (
                                        contact_key number(20),
                                        high_skincare_flag number(20)
                                        )"""
        
        try:
            
            cursor.execute(create_query)
            con.commit()

        except Exception as e:
            
            raise e
        
        con.close()
        

    def export_output_table(self, MonthParams) -> None:

        """insert output table from csv into adm in chunks."""

        chunk_size = 100_000

        insert_query = f"""INSERT INTO BDUNNE.{MonthParams.output_table_name} 
                            values (:1, :2)"""
        
        conn = utils.get_ADM_connection()
        
        cur = conn.cursor()

        csv_file = f'data/processed/{MonthParams.month_start}_to_{MonthParams.month_end}_model_predictions_df.csv'

        with open(csv_file, "r") as file:

            csv_reader = csv.reader(file, delimiter=",")

            data = []

            for i, line in enumerate(csv_reader):

                if i != 0:

                    data.append(
                        (
                            line[1],
                            line[2],
                        )
                    )
                    if len(data) % chunk_size == 0:
                        cur.executemany(insert_query, data)
                        data = []
            
            if data:
                cur.executemany(insert_query, data)

            conn.commit()

            conn.close()