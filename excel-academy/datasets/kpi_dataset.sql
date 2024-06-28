/* 
Excel Academy - KPI Dataset Example
    - if your code isn't identical, don't worry too much, this is more about
    getting the Excel right than the SQL :)
    - as long as the output gives a pretty similar dataset, you're good to go!
*/

select
    t.bu_code,
    d.fiscal_day_desc,
    d.fiscal_wk_idnt,
    case when ws.web_store_flag = 'Y' then 'Online' else 'Store' end as channel, -- this could be done by just getting web_store_flag and changing it later in excel too
    rfm.seg_num,
    case when c.gender_name = 'F' then 'Female' 
         when c.gender_name = 'M' then 'Male'
         else 'Unspecified' end as gender, --this could also be done later in excel
    case when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 16 and 20 then 'Under 20'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 21 and 25 then '21-25'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 26 and 35 then '26-35'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 36 and 45 then '36-45'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 46 and 55 then '46-55'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 56 and 65 then '56-65'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 66 and 100 then '65+'
        else 'Unspecified' end as age,
    sum(t.item_amt) as sales,
    count(distinct t.contact_key) as members,
    count(distinct t.order_num) as orders,
    sum(t.item_quantity_val) as items
from
    crm_target.b_transaction t 
    join crm_target.b_product p on t.product_key = p.product_key
    join crm_target.b_time d on t.transaction_dt_key = d.date_key
    join crm_target.seg_rfm rfm on t.contact_key = rfm.contact_key
    left join rcovell.web_stores ws on t.store_key = ws.store_key
    join crm_target.b_contact c on t.contact_key = c.contact_key
where
    t.bu_key in (5,20,21,22) -- MCE (Marionnaud Central Europe are smaller and so faster to query compared to the bigger units
    and t.transaction_type_name = 'Item'
    and t.member_sale_flag = 'Y'
    and t.contact_key > 0 -- extra check for members
    and p.kpi_exclusion_flag = 'N'
    and d.fiscal_mth_idnt = 202401
group by 
    t.bu_code,
    d.fiscal_day_desc,
    d.fiscal_wk_idnt,
    case when ws.web_store_flag = 'Y' then 'Online' else 'Store' end,
    rfm.seg_num,
    case when c.gender_name = 'F' then 'Female' 
         when c.gender_name = 'M' then 'Male'
         else 'Unspecified' end,
    case when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 16 and 20 then 'Under 20'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 21 and 25 then '21-25'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 26 and 35 then '26-35'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 36 and 45 then '36-45'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 46 and 55 then '46-55'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 56 and 65 then '56-65'
        when trunc(months_between(d.calendar_dt, c.birth_dt) / 12) between 66 and 100 then '65+'
        else 'Unspecified' end 
order by 3,2