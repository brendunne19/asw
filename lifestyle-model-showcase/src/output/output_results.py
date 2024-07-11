# proprietary imports

import my_oracle as ora

# global imports
import cx_Oracle
import csv
from loguru import logger

import src.output.my_creds as my_creds

class OutputResults:

    def __init__(self, MonthParams) -> None:

        self.MonthParams = MonthParams


    def create_output_table(self, MonthParams) -> None:

        """Create empty table to export output to in ADM."""

        # drop table if exists
        drop_query = f"DROP TABLE ACHAN.{MonthParams.output_table_name}"

        try:
            
            ora.execute_oracle_query(db_instance='CRMBMAP', query=drop_query)
        
        except cx_Oracle.DatabaseError as e:

            # Pass any failed drops - there are some by design
            if str(e) == "ORA-00942: table or view does not exist":
                logger.info("Passing following error: \n", e)
                pass
            else:
                raise e
        
        # create empty output table
        create_query = f"""CREATE TABLE ACHAN.{MonthParams.output_table_name} (
                                        contact_key number(20),
                                        seg_num number(20)
                                        )"""
        
        try:
            
            ora.execute_oracle_query(db_instance='CRMBMAP', query=create_query)

        except Exception as e:
            
            raise e
        

    def export_output_table(self, MonthParams) -> None:

        """insert output table from blob into adm in chunks (for MCE probs unnecessary)."""

        chunk_size = 100_000

        insert_query = f"""INSERT INTO ACHAN.{MonthParams.output_table_name} 
                            values (:1, :2)"""
        
        conn = cx_Oracle.connect(
                        my_creds.CRMBMAP["USERNAME"],
                        my_creds.CRMBMAP["PASSWORD"],
                        my_creds.CRMBMAP["HOSTNAME"],
                        encoding="UTF8",
                    )
        
        cur = conn.cursor()

        csv_file = f'data/processed/{MonthParams.bu_code}_lseg_pred_d_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv'

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

    def create_siebel_table(self, MonthParams) -> None:

        """Create empty table for IT in ADM."""

        # drop table if exists
        drop_query = f"DROP TABLE ACHAN.{MonthParams.siebel_table_name}"

        try:
            
            ora.execute_oracle_query(db_instance='CRMBMAP', query=drop_query)
        
        except cx_Oracle.DatabaseError as e:

            # Pass any failed drops - there are some by design
            if str(e) == "ORA-00942: table or view does not exist":
                logger.info("Passing following error: \n", e)
                pass
            else:
                raise e
        
        # create empty output table
        create_query = f"""CREATE TABLE {MonthParams.siebel_table_name}
                        (      mem_num       varchar2(100)
                        ,      bu_name       varchar2(100)
                        ,      type          varchar2(30)
                        ,      active_flag   char(1)
                        ,      segment_type  varchar2(30)
                        ,      segment_num   varchar2(100)
                        ,      segment_name  varchar2(100)
                        ,      start_dt      date
                        ,      end_dt        date
                        ,      source        varchar2(30)
                        ,      error_flag    char(1)
                        ,      row_num       number(20,0)
                        )"""
        
        try:
            
            ora.execute_oracle_query(db_instance='CRMBMAP', query=create_query)

        except Exception as e:
            
            raise e
        
    def fill_siebel_table(self, MonthParams) -> None:

        """Insert output table into siebel table."""

        conn = cx_Oracle.connect(
                        my_creds.CRMBMAP["USERNAME"],
                        my_creds.CRMBMAP["PASSWORD"],
                        my_creds.CRMBMAP['HOSTNAME'],
                        encoding="UTF8",
                    )
        
        cur = conn.cursor()

        # have to change table behaviour for IT
        special_query = f"ALTER TABLE {MonthParams.siebel_table_name} MOVE COMPRESS NOLOGGING"
        
        cur.execute(special_query)
        conn.commit()

        insert_query = f"""insert into {MonthParams.siebel_table_name} 
                        select 
                            distinct member_num as mem_num,
                            '{MonthParams.bu_code}' as bu_name,
                            'Segment' as type,
                            'Y' as active_flag,
                            'Lifestyle' as segment_type,
                            seg_num as segment_num,
                            case when seg_num = 1 then 'Infrequent Fragrance-Only Shoppers'
                                when seg_num = 2 then 'Conservative Perfumistas'
                                when seg_num = 3 then 'Occasional Digital Gifters'
                                when seg_num = 4 then 'Premium Beauty Addicts'
                                when seg_num = 5 then 'Marionnaud Connoisseurs'
                                when seg_num = 6 then 'Male Shoppers'
                            end as segment_name,
                            to_date('{str(MonthParams.month_idnt) + '01'}','yyyymmdd') as start_dt,
                            null as end_dt,
                            'SQL' as source,
                            'N' as error_flag,
                            rownum as row_num
                        from
                            achan.{MonthParams.output_table_name} b

                            left join 
                                    (
                                    select distinct contact_key, member_key 
                                    from crm_target.b_mem_contact_card 
                                    where bu_key = {MonthParams.bu_key}
                                    and     contact_key not in (select  distinct contact_key
                                                                from    CRM_TARGET.B_MEM_CONTACT_CARD
                                                                where   bu_key = {MonthParams.bu_key}
                                                                group by
                                                                        contact_key
                                                                having  count(distinct member_key) > 1
                                                                )
                                    ) mcc on b.contact_key = mcc.contact_key
                            
                            inner join 
                                    (
                                    select distinct member_key, member_num
                                    from crm_target.b_member 
                                    where bu_key = {MonthParams.bu_key}
                                    ) m on mcc.member_key = m.member_key
                        """
        cur.execute(insert_query)
        conn.commit()

        duplicate_query = f"""DELETE FROM achan.{MonthParams.siebel_table_name}
                            WHERE rowid not in
                            (SELECT MIN(rowid)
                            FROM achan.{MonthParams.siebel_table_name}
                            GROUP BY mem_num)"""
        
        cur.execute(duplicate_query)
        conn.commit()

        lost_query = f"""select count(distinct contact_key) as orig_mems from ACHAN.{MonthParams.output_table_name}
                            union
                            select count(distinct mem_num) as final_mems from ACHAN.{MonthParams.siebel_table_name}"""
        
        mem_df = ora.get_oracle_data(db_instance='CRMBMAP', query=lost_query)

        orig_mems = int(mem_df.iloc[1]) # the rows are reversed with the union
        final_mems = int(mem_df.iloc[0])

        logger.info(F'INFO: Lost {round((orig_mems - final_mems) / orig_mems * 100, 2)}% of original members due to duplicates in contact_key/member_num.')

        conn.close()


