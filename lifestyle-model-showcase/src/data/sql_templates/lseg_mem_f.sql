drop table {bu_code}_LSEG_MEM_F_{month_label};

create table {bu_code}_LSEG_MEM_F_{month_label} AS (

    select  distinct t.contact_key
    ,       sum(case when product_hier_2_l3_name = 'FRAGRANCES WOMEN' then item_amt end) as fra_wom_sales
    ,       sum(case when product_hier_2_l3_name = 'FRAGRANCES MEN' then item_amt end) as fra_men_sales
    ,       sum(case when product_hier_2_l3_name = 'MAKE-UP EYES' then item_amt end) as mup_eye_sales
    ,       sum(case when product_hier_2_l3_name = 'MAKE-UP FACE' then item_amt end) as mup_fac_sales
    ,       sum(case when product_hier_2_l3_name = 'MAKE-UP LIPS' then item_amt end) as mup_lip_sales
    ,       sum(case when product_hier_2_l3_name = 'SKINCARE WOMEN' then item_amt end) as skc_wom_sales
    ,       sum(case when product_hier_2_l3_name = 'GIFT SETS SELECTIVE' or g.product_ean_num is not null then item_amt end) as gif_set_sel_sales
    ,       sum(case when brand_type_name = 'Private Label' then item_amt 
                        when upper(brand_name) like 'MARIONNAUD%' or upper(brand_name) like 'MRN%' then item_amt end) as prv_lab_sales
    
    ,       sum(item_amt) as tot_sales
    ,       count(distinct order_num) as tot_trxs
    ,       sum(case when t.bu_key = 17 and p.brand_name in ('CHEQUE MARIONNAUD', 'BUONI MARIONNAUD', 'GIFT MARIONNAUD') then 0 else item_quantity_val end) as tot_items
    
    ,       max(case when seg_num = 'VIP' then 1 else 0 end) as rfm_vip_flag
    ,       max(case when seg_num = 'LOYAL' then 1 else 0 end) as rfm_loy_flag
    ,       max(case when cust_type in ('Multichannel', 'Pure Online') then 1 else 0 end) as online_flag
    ,       max(case when gender_name = 'M' then 1 else 0 end) as gen_m_flag

    from    B_TRANSACTION t
    inner join
            B_PRODUCT p
            on p.product_key = t.product_key
    left join
            (
                select  distinct product_ean_num
                from    ACHAN.MCE_GIFT_SKUS
                where   bu_key = {bu_key}
            ) g
            on g.product_ean_num = p.product_ean_num
    left join
            (
                select  distinct contact_key
                ,       seg_num
                from    CRM_TARGET.SEG_RFM
                where   bu_key = {bu_key}
                and     seg_start_dt <= '{rfm_date}'
                and     (seg_end_dt >= '{rfm_date}' or seg_end_dt is null)
            ) rfm
            on rfm.contact_key = t.contact_key
    left join
            MRD_OO_{max_mth_idnt} o
            on o.contact_key = t.contact_key
    inner join
            (
                select  distinct contact_key
                ,       gender_name
                from    CRM_TARGET.B_CONTACT
                where   bu_key = {bu_key}
            ) c
            on c.contact_key = t.contact_key
    inner join
            CRM_TARGET.B_TIME dt
            on dt.date_key = t.transaction_dt_key

    where   t.bu_key = {bu_key}
    and     p.bu_key = {bu_key}
    and     (case when t.bu_key = 17 then 1 when nvl(p.kpi_exclusion_flag, 'N') = 'N' then 1 else 0 end) = 1
    and     t.transaction_type_name = 'Item'
    and     t.member_sale_flag = 'Y'
    and     (fiscal_mth_idnt between (to_char(add_months(to_date({max_mth_idnt}, 'YYYYMM'), -{period_length}), 'YYYYMM')) AND {max_mth_idnt})

    group by
            t.contact_key

);