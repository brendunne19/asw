drop table {bu_code}_LSEG_PROF_F_{month_label};

create table {bu_code}_LSEG_PROF_F_{month_label} AS (
    
    select  distinct t.contact_key
    ,       order_num
    ,       case when upper(brand_name) like 'MARIONNAUD%' or upper(brand_name) like 'MRN%' then 'Private Label'
                 else brand_type_name end as brand_type_name
    ,       case when g.product_ean_num is not null then 'GIFT SETS SELECTIVE' else product_hier_2_l3_name end as product_hier_2_l3_name
    ,       sum(item_amt) as tot_sales
    ,       sum(item_quantity_val) as tot_items
    ,       sum(item_spread_discount_amt) as tot_discount

    ,       c.birth_dt
    ,       c.gender_name

    ,       rfm.seg_num

    ,       max(case when  s.web_store_flag is not null then 1 else 0 end) as web_store_flag

    from    B_TRANSACTION t
    inner join
            CRM_TARGET.B_CONTACT c
            on c.contact_key = t.contact_key
            and c.bu_key = t.bu_key
    left join
            (
                select  distinct contact_key
                ,       max(seg_num) as seg_num
                from    CRM_TARGET.SEG_RFM
                where   bu_key = {bu_key}
                and     seg_start_dt <= '{rfm_date}'
                and     (seg_end_dt >= '{rfm_date}' or seg_end_dt is null)
                group by
                        contact_key
            ) rfm
            on rfm.contact_key = t.contact_key
    left join
            CRM_datalab.web_stores s
            on s.store_key = t.store_key
            and s.bu_key = t.bu_key
    inner join
            CRM_TARGET.B_PRODUCT p
            on p.product_key = t.product_key
            and p.bu_key = t.bu_key
    left join
            (
                select  distinct product_ean_num
                from    ACHAN.MCE_GIFT_SKUS
                where   bu_key = {bu_key}
            ) g
            on g.product_ean_num = p.product_ean_num
    inner join
            CRM_TARGET.B_TIME dt
            on dt.date_key = t.transaction_dt_key
    
    where   t.bu_key = {bu_key}
    and     p.bu_key = {bu_key}
    and     (case when t.bu_key = 17 then 1 when nvl(p.kpi_exclusion_flag, 'N') = 'N' then 1 else 0 end) = 1
    and     member_sale_flag = 'Y'
    and     transaction_type_name = 'Item'
    and     (fiscal_mth_idnt between (to_char(add_months(to_date({max_mth_idnt}, 'YYYYMM'), -{period_length}), 'YYYYMM')) and {max_mth_idnt})

    group by
            t.contact_key
    ,       order_num
    ,       case when upper(brand_name) like 'MARIONNAUD%' or upper(brand_name) like 'MRN%' then 'Private Label'
                 else brand_type_name end
    ,       case when g.product_ean_num is not null then 'GIFT SETS SELECTIVE' else product_hier_2_l3_name end

    ,       c.birth_dt
    ,       c.gender_name

    ,       rfm.seg_num
    
);