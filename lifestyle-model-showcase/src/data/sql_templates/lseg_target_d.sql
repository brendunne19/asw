drop table {bu_code}_LSEG_TARGET_D_{month_label};

create table {bu_code}_LSEG_TARGET_D_{month_label} AS (
    
    select  distinct contact_key
    ,       seg_num
    from    CRM_TARGET.SEG_LIFESTYLE
    where   bu_key = {bu_key}
    and     seg_start_dt <= '{rfm_date}'
    and     (seg_end_dt >= '{rfm_date}' or seg_end_dt is null)
    
);