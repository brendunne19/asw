drop table MFR_LSEG_TARGET_D_FEB24;

create table MFR_LSEG_TARGET_D_FEB24 AS (
    
    select  distinct contact_key
    ,       seg_num
    from    CRM_TARGET.SEG_LIFESTYLE
    where   bu_key = 16
    and     seg_start_dt <= '01-FEB-24'
    and     (seg_end_dt >= '01-FEB-24' or seg_end_dt is null)
    
);