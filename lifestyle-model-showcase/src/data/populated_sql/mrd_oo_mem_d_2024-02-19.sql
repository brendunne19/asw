drop table MRD_OO_202401;

create table MRD_OO_202401 as (

    select  bu_key
    ,       bu_code
    ,       contact_key
    ,       case when (web_txns > 0 and store_txns > 0) then 'Multichannel'
                 when web_txns > 0 then 'Pure Online'
                 else 'Pure Offline'
                 end as cust_type
    
    from (
        
        select  t.bu_key
        ,       t.bu_code
        ,       t.contact_key
        
        ,       count(distinct case when nvl(w.web_store_flag, 'N') = 'N' then t.order_num end) as store_txns
        ,       count(distinct case when nvl(w.web_store_flag, 'N') = 'Y' then t.order_num end) as web_txns

        from    B_TRANSACTION t
        inner join
                B_PRODUCT p
                on p.product_key = t.product_key 
                and p.bu_key = t.bu_key
        inner join
                CRM_TARGET.B_STORE s
                on s.store_key = t.store_key
                and s.bu_key = t.bu_key
        left join
                RCOVELL.WEB_STORES w
                on w.store_key = t.store_key
                and w.bu_key = t.bu_key
        inner join
                CRM_TARGET.B_TIME dt
                on dt.date_key = t.transaction_dt_key

        where   (case when t.bu_code in ('MIT') then 1 when p.kpi_exclusion_flag = 'N' then 1 else 0 end) = 1
        and     t.transaction_type_name = 'Item'
        and     (fiscal_mth_idnt between (to_char(add_months(to_date(202401, 'YYYYMM'), -11), 'YYYYMM')) AND 202401)
        and     member_sale_flag = 'Y'
        and     item_amt <> 0
        and     t.product_key not in (1215708500,1247732966,386825,454782050,454802796,336368,335605,288052,3888706,1831026353,1673361840,24721664,454800686,367330,64375,12421337,1619243965,1673361841,346930,391568,454798578,1247732966,1673361839,1673361842,284428,263331)
        and     p.product_key <> 1215708500
        and     nvl(p.product_hier_1_l1_name, 'NULL') <> 'TECHNICAL'
        and     t.store_key not in '55220'
        and     t.bu_key in (5, 16, 17, 20, 21, 22)

        group by
                t.bu_key
        ,       t.bu_code
        ,       t.contact_key

    ) t

);