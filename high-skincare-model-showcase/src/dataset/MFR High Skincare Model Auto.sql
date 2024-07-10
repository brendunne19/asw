-----------------------------------------------------------------------------
------------- COLLECTING TEST DATASETS FOR MFR SKINCARE MODELS --------------
-----------------------------------------------------------------------------

begin mfr_high_skincare_model_data_auto(202202, 202301);
END;

--------------------------CREATING TEMP TABLES -----------------------------
DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_MEMBERS_auto;
DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_DATA_auto;
DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_auto;

CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_MEMBERS_auto AS select * from crm_target.b_time where date_key = 20230101;
CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_DATA_auto as select * from crm_target.b_time where date_key = 20230101;
CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_auto AS select * from crm_target.b_time where date_key = 20230101;
----------------------------------- PROC ------------------------------------
create or replace procedure mfr_high_skincare_model_data_auto (
    
    start_month number, 
    end_month number) 

is

    member_list_del varchar2(30000);
    member_list varchar2(30000);
    member_data_del varchar2(30000);
    member_data varchar2(30000);
    member_level_del varchar2(30000);
    member_level varchar2(30000);
    end_of_period_date varchar2(50);
    flag_start_month varchar2(50);
    flag_end_month varchar2(50);
    ly_start_month varchar2(50);
    ly_end_month varchar2(50);

begin

-- FINDING THE EOP DATE FOR AGE AND RFM CALCS, and the ly and ny months
select max(calendar_dt) + 1 into end_of_period_date from crm_target.b_time where fiscal_mth_idnt = end_month;
select distinct fiscal_mth_idnt + 100 into flag_start_month from crm_target.b_time where fiscal_mth_idnt = start_month;
select distinct fiscal_mth_idnt + 100 into flag_end_month from crm_target.b_time where fiscal_mth_idnt = end_month;
select distinct fiscal_mth_idnt - 100 into ly_start_month from crm_target.b_time where fiscal_mth_idnt = start_month;
select distinct fiscal_mth_idnt - 100 into ly_end_month from crm_target.b_time where fiscal_mth_idnt = end_month; 


-- GET LIST OF SKINCARE MEMBERS IN PERIOD
member_list_del := 'DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_MEMBERS_auto';
execute immediate (member_list_del);
commit;

member_list := '
CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_MEMBERS_auto AS
(
     SELECT
        DISTINCT CONTACT_KEY
     FROM crm_Target.b_transaction T
     join crm_target.b_product p on t.product_key = p.product_key
     JOIN CRM_TARGET.B_TIME TM
        ON TM.DATE_KEY = T.TRANSACTION_DT_KEY
     WHERE T.BU_KEY = 16
        AND PRODUCT_HIER_2_L2_NAME = ''SKINCARE''
        AND CONTACT_KEY > 0
        AND MEMBER_SALE_FLAG = ''Y''
        AND KPI_EXCLUSION_FLAG = ''N''
        and transaction_type_name = ''Item''
        AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||'''
GROUP BY
   CONTACT_KEY
)';
execute immediate(member_list);
commit;
    

-- TABLE TO BRING BACK DATA FROM TY AND LY FOR PERIOD
member_data_del := 'DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_DATA_auto';
execute immediate(member_data_del);
commit;

member_data :='
CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_DATA_auto AS
SELECT
    CONTACT_KEY
,   member_key
,   TRANSACTION_DT_KEY
,   fiscal_mth_idnt
,   ORDER_NUM 
,   BRAND_NAME
,   PRODUCT_HIER_2_L2_NAME
,   ITEM_AMT
,   ITEM_QUANTITY_VAL
,   PRODUCT_KEY
FROM
    (SELECT 
        M.CONTACT_KEY
    ,   t.member_key
    ,   TRANSACTION_DT_KEY
    ,   fiscal_mth_idnt
    ,   ORDER_NUM 
    ,   BRAND_NAME
    ,   PRODUCT_HIER_2_L2_NAME
    ,   ITEM_AMT
    ,   ITEM_QUANTITY_VAL
    ,   T.PRODUCT_KEY
    FROM crm_target.b_transaction T
    JOIN CRM_TARGET.B_TIME TM
      ON TM.DATE_KEY = T.TRANSACTION_DT_KEY
    JOIN mfr_HIGH_SKINCARE_MODEL_TRAINING_MEMBERS_auto M
      ON M.CONTACT_KEY = T.CONTACT_KEY
    join crm_target.b_product p on T.product_key = p.product_key
    WHERE T.BU_KEY = 16
      AND T.CONTACT_KEY > 0
      AND MEMBER_SALE_FLAG = ''Y''
      AND KPI_EXCLUSION_FLAG = ''N''
      AND FISCAL_MTH_IDNT BETWEEN '''||ly_start_month||''' AND '''||flag_end_month||'''
    GROUP BY
        M.CONTACT_KEY
    ,   t.member_key
    ,   TRANSACTION_DT_KEY
    ,   fiscal_mth_idnt
    ,   ORDER_NUM 
    ,   BRAND_NAME
    ,   PRODUCT_HIER_2_L2_NAME
    ,   ITEM_AMT
    ,   ITEM_QUANTITY_VAL
    ,   T.PRODUCT_KEY
    )
';
execute immediate(member_data);
commit;


-- AGGREGATE DATA TO A MEMBER LEVEL
member_level_del := 'DROP TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_auto';
execute immediate(member_level_del);
commit;

member_level := '
CREATE TABLE mfr_HIGH_SKINCARE_MODEL_TRAINING_auto AS
SELECT
    DISTINCT T.CONTACT_KEY
,   case when (c.EMAIL_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_EMAIL_FLAG = ''N'' and VALID_EMAIL_FORMAT = ''Y'') then 1 else 0 end as email_flag
,   case when (c.SMS_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_SMS_FLAG = ''N'' and PHONE_REFERENCE_DESC not in (''UN'', ''Uns'', ''xxx'', ''-'') ) then 1 else 0 end as sms_flag
,   case when (c.ADDRESS_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_DM_FLAG = ''N'' ) then 1 else 0 end as dm_flag
,   case when sum(case when t.fiscal_mth_idnt between '''||flag_start_month||''' and '''||flag_end_month||''' and t.product_hier_2_l2_name = ''SKINCARE'' then t.item_amt end) > 135 then 1 else 0 end as high_skincare_flag
,   SUM(CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS Ty_SALES
,   SUM(CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS Ty_UNITS
,   COUNT(DISTINCT CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ORDER_NUM END) AS Ty_VISITS
,   SUM(CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||ly_start_month||''' AND '''||ly_end_month||''' THEN ITEM_AMT END) AS ly_SALES
,   SUM(CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||ly_start_month||''' AND '''||ly_end_month||''' THEN ITEM_QUANTITY_VAL END) AS ly_UNITS
,   COUNT(DISTINCT CASE WHEN FISCAL_MTH_IDNT BETWEEN '''||ly_start_month||''' AND '''||ly_end_month||''' THEN ORDER_NUM END) AS ly_VISITS
,   round((MAX(CASE WHEN FISCAL_MTH_IDNT <= '''||end_month||''' THEN to_date(TRANSACTION_DT_KEY, ''yyyymmdd'') END) - MIN(CASE WHEN FISCAL_MTH_IDNT >= '''||start_month||''' THEN to_date(TRANSACTION_DT_KEY, ''yyyymmdd'') END)) / COUNT(DISTINCT ORDER_NUM),2) AS DAYS_BETWEEN_TRXS
,   MAX(CASE WHEN FISCAL_MTH_IDNT <= '''||end_month||''' THEN to_date(TRANSACTION_DT_KEY, ''yyyymmdd'') END) AS LAST_PURCHASE_DATE
,   MAX(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND FISCAL_MTH_IDNT <= '''||end_month||''' THEN to_date(TRANSACTION_DT_KEY, ''yyyymmdd'') END) AS LAST_SKINCARE_PURCHASE_DATE
,   BIRTH_DT
,   case when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 16 and 20 then ''Under 20''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 21 and 25 then ''21-25''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 26 and 35 then ''26-35''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 36 and 45 then ''36-45''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 46 and 55 then ''46-55''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 56 and 65 then ''56-65''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 66 and 100 then ''65+''
    else ''Unspecified'' end as age
,   GENDER_NAME
,   ENROL_DT
,   FIRST_PURCHASE_DT
,   seg_num
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS SKINCARE_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS SKINCARE_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND FISCAL_MTH_IDNT BETWEEN '''||ly_start_month||''' AND '''||ly_end_month||''' THEN ITEM_AMT END) AS PREVIOUS_YR_SKINCARE_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''MAKE-UP'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS MAKE_UP_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''MAKE-UP'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS MAKE_UP_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''FRAGRANCES'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS FRAGRANCE_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''FRAGRANCES'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS FRAGRANCE_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''GIFT SETS'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS GIFT_SETS_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''GIFT SETS'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS GIFT_SETS_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SUNCARE'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS SUNCARE_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SUNCARE'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS SUNCARE_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''OTHER'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS OTHER_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''OTHER'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS OTHER_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''ACCESSORIES'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS ACCESSORIES_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''ACCESSORIES'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_QUANTITY_VAL END) AS ACCESSORIES_UNITS
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''CLARINS'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS CLARINS_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''SISLEY'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS SISLEY_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''LANCOME'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS LANCOME_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''QIRINESS'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS QIRINESS_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''LAUDER'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS LAUDER_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''CHANEL'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS CHANEL_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''GUERLAIN'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS GUERLAIN_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''IOMA'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS IOMA_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''FILORGA'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS FILORGA_SALES
,   SUM(CASE WHEN PRODUCT_HIER_2_L2_NAME = ''SKINCARE'' AND BRAND_NAME = ''SHISEIDO'' AND FISCAL_MTH_IDNT BETWEEN '''||start_month||''' AND '''||end_month||''' THEN ITEM_AMT END) AS SHISEIDO_SALES
FROM mfr_HIGH_SKINCARE_MODEL_TRAINING_DATA_auto T
JOIN CRM_TARGET.B_CONTACT C
    ON T.CONTACT_KEY = C.CONTACT_KEY
LEFT JOIN CRM_TARGET.B_MEMBER M
    ON T.member_key = M.MEMBER_KEY
left join crm_target.seg_rfm r on r.contact_key = t.contact_key 
WHERE C.BU_KEY = 16
    and t.contact_key not in (select contact_key from mfr_gs_lookup_allb)
    and item_amt > 0
    and seg_start_dt <= '''||end_of_period_date||''' AND (seg_end_dt >= '''||end_of_period_date||''' or seg_end_dt is null)
GROUP BY 
    T.CONTACT_KEY
,   case when (c.EMAIL_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_EMAIL_FLAG = ''N'' and VALID_EMAIL_FORMAT = ''Y'') then 1 else 0 end
,   case when (c.SMS_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_SMS_FLAG = ''N'' and PHONE_REFERENCE_DESC not in (''UN'', ''Uns'', ''xxx'', ''-'') ) then 1 else 0 end
,   case when (c.ADDRESS_CORRECT_FLAG = ''Y'' and c.SUPPRESS_INTERNAL_DM_FLAG = ''N'' ) then 1 else 0 end
,   BIRTH_DT
,   case when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 16 and 20 then ''Under 20''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 21 and 25 then ''21-25''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 26 and 35 then ''26-35''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 36 and 45 then ''36-45''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 46 and 55 then ''46-55''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 56 and 65 then ''56-65''
        when trunc(months_between('''||end_of_period_date||''', c.birth_dt) / 12) between 66 and 100 then ''65+''
    else ''Unspecified'' end
,   GENDER_NAME
,   ENROL_DT
,   FIRST_PURCHASE_DT
,   seg_num
';
execute immediate(member_level);
commit;

end;