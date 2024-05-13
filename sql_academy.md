# SQL Academy



## Table of Contents
- [1 Getting Started](#1-getting-started)
    - [1.1 Oracle SQL](#11-oracle-sql) 
    - [1.2 Downloading SQL](#12-downloading-sql)
    - [1.3 Opening and Saving a File](#13-opening-and-saving-a-file)
    - [1.4 SQL Language & Database Concepts](#14-sql-language--database-concepts)
    - [1.5 Setting Up Connections](#15-setting-up-connections)
- [2 Using the Database](#2-using-the-database)
    - [2.1 AS Watson Data Model (ADM) Structure & Data Tables](#21-as-watson-data-model-adm-structure--data-tables)
    - [2.2 Business Units](#22-business-units)
    - [2.3 AS Watson Calendar](#23-as-watson-calendar)
    - [2.4 Currency](#24-currency)
- [3 SQL Coding - Part 1](#3-sql-coding---part-1)
    - [3.1 Basic SQL Querying Concepts](#31-basic-sql-querying-concepts)
        - [3.1.1 Select Statements](#311-select-statements)
        - [3.1.2 Where, And & Setting Conditions](#312-where-and--setting-conditions)
        - [3.1.3 Aggregate Functions](#313-aggregate-functions)
        - [3.1.4 Like Clause](#314-like-clause)
        - [3.1.5 Distinct Clause](#315-distinct-clause)
        - [3.1.6 Joining Tables](#315-joining-tables)
        - [3.1.7 Case When](#317-case-when)
    - [3.2 B_TRANSACTION Table](#32-b_transaction-table)
    - [3.3 Main KPIs](#33-main-kpis)
    - [3.4 Time Periods](#34-main-time-periods)
    - [3.5 Examples](#35-examples)
    - [3.6 B_PRODUCT Table](#36-b_product-table)
    - [3.7 Transactional Base Table](#37-transactional-base-table)
    - [3.8 Final Note](#38-final-note)
- [4 Exercises - Part 1](#4-exercises---part-1)
    - [4.1 Warm Up Questions - B_TRANSACTION only](#41-warm-up-questions---b_transaction-only)
    - [4.2 Exercises 1](#42-exercises-1)
    - [4.3 Exercises 2](#43-exercises-2)


- [Answers](#answers)
    - [4.1 Warm Up Questions - B_TRANSACTION only](#41-warm-up-questions---answers)
    - [4.2 Exercises 1](#42-exercises-1-answers)

## 1 Getting Started 
[<u>Back to Top</u>](#sql-academy)

### 1.1 Oracle SQL
- We use Oracle SQL
- There are other versions, including SQL Server, PostgreSQL, MySQL, SQLite etc. but we do not use these.
- There are minor differences, but you may find that a solution you find online might use a function that is in SQL Server but not Oracle SQL or visa versa.
- When using Google to find an answer (Stack Overflow is your best friend), make sure to add Oracle SQL to get the relevant result.
- Note that Databricks for the EDP environment uses Spark SQL which has some different syntax to Oracle SQL, but this is something that you might use later into your time at AS Watson. 

### 1.2 Downloading SQL
- <u>[SQL Developer](https://aswatsonuk.sharepoint.com/sites/ASWGD/Shared%20Documents/Forms/AllItems.aspx?csf=1&web=1&e=6f1lwM&OR=Teams%2DHL&CT=1666772057858&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMjA5MDQwMDcxMiIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D&cid=ff58d4e3%2Dc07a%2D4c8a%2D8d81%2Df7b71ac83e11&FolderCTID=0x012000372904FE328ED84D95719C40897751FE&id=%2Fsites%2FASWGD%2FShared%20Documents%2F1%2E%20Analytics%2F02%2E%20Data%20Management%2F00%2E%20General%2FTools&viewid=bd31f600%2D1e1a%2D4ba8%2Db27b%2Dc105f08eec46)</u>
- Unzip the folder ‘sqldeveloper-18.2.0.183.1748-x64’ to your C drive ‘C:\Users\{Username}’
- Pin to task bar so that you can find it easily

### 1.3 Opening and Saving a File
- To open a file drag it into a SQL window that isn’t running any code. (if new window, need to open a connection first)
- To open a blank file:

    <img src="image.png" width=162> 
    <img src="image-2.png" width=450> 
- To save an untitled file either press “Ctrl + S” or select “File” then “Save As” and save the file in the follow path: 

    <img src="image-3.png" height=120>

### 1.4 SQL Language & Database Concepts

- SQL = Structured Query Language 
- Originally designed for creating and manipulating data stored in a relational database 
- We use 3 data bases: 
    - CRMBMAP – known as MRD Instance
    - CRMBKVP – known as KV Instance
    - CRMBSDP – Known as SD Instance
- Schemas are collections of database objects, namely tables, but also procedures, packages etc. 
- For example, if you want to look at ICI Paris Netherlands data, this can only be accessed in the CRMBKVP schema (Check Business Units excel for which schema to use)
- CRM_TARGET schema holds all transactional and member data 
- You will probably get your own schema, which is debatably quite exciting.

### 1.5 Setting Up Connections
- Connecting to the database under a new schema: 
    1. Select “View” and then “Connections”. Under Connections, press the Plus button
    2. Name the connection, enter the username and password. Copy and use the same hostname and port. 
    3. Change the Service Name to reflect which instance you would like to connect to. 
    4. Select “Test” and is the connection was successful, then press “Save”
- Note you will have to repeat this 
   for each instance 

    ![alt text](image-1.png)


# 2 Using the Database
[<u>Back to Top</u>](#sql-academy)

### 2.1 AS Watson Data Model (ADM) Structure & Data Tables
- <u>[ASW ADM Data Model](https://aswatsonuk.sharepoint.com/:x:/r/sites/ASWGD/_layouts/15/Doc.aspx?sourcedoc=%7B3AD22FDD-FD8B-41CE-B887-2342F8124305%7D&file=EU%20ADM%20Data%20Model%20%26%20More.xlsx&action=default&mobileredirect=true&wdLOR=c0C157FCF-63DE-4B0F-B7BB-9A66FE1E1577)</u>
- Shows the link between the main tables in ADM and all the rules for each BU
    <img src="image-5.png" width=600>

### 2.2 Business Units
- <u>[Business Units](https://aswatsonuk.sharepoint.com/:x:/r/sites/ASWGD/_layouts/15/Doc.aspx?sourcedoc=%7B29874E8B-EB31-4477-897E-F2AE3FBAD053%7D&file=Business%20Units.xlsx&action=default&mobileredirect=true)</u>
- Each BU has a different bu_key and bu_code so that we can easily distinguish between them in the data tables
- We often refer to MCE – Marionnaud Central Europe as: MHU, MRO, MCZ and MSK 
- On the second column you can see which instance you need to have selected in order to access that BU's data
    ![alt text](image-7.png)


### 2.3 AS Watson Calendar
- <u>[Calendar](https://aswatsonuk.sharepoint.com/:x:/r/sites/ASWGD/_layouts/15/Doc.aspx?sourcedoc=%7B43BB6B4B-FE9C-473D-867C-F9C19EEEB24F%7D&file=Calendrier%202010%20-%202023%20AS%20WATSON.xls&action=default&mobileredirect=true)</u>
- We follow a financial/fiscal calendar which shifts the first day of every month to be a Monday.
- ![alt text](image-9.png)


### 2.4 Currency
- Sales in the database are all in local currencies
- When we group together more than one BU we will need to convert the currency to a common one. 
- Most commonly either converted to EUR (€) or HKD  
    <img src="image-10.png" width=350>


# 3 SQL Coding - Part 1

### 3.1 Basic SQL Querying Concepts
[<u>Back to Top</u>](#sql-academy)

### 3.1.1 Select Statements
- Two basic ‘clauses’ for querying data from a table:
    1. tell it what you want ```select```
    2. tell it where to get it from ```from```
- Selecting everything in a specified table:
    ```
    select *
    from table_name
    ```
- Run code using CTRL + Enter or highlight and click <img src="image-11.png" height=15> in the top left
- Every query should have a ```;``` at the end
- If we wanted to select just one column:
    ```
    select column_name
    from table_name;
    ```
- You can name a column using ```as```
    ```
    select column_name as new_name
    from table_name;
    ```

### 3.1.2 Where, And & Setting Conditions
- If we want to filter a table to enter select certain features we use a where clause.
- Filter only female members e.g.:
    ```
    select * 
    from table_name
    where gender = ‘F’;
    ```
- An ```and``` clause will be used if we are using more than one filter/exclusion.
- Example: filter by female and older than 25 years
    ```
    select *
    from table_name
    where gender = ‘F’
    and age > 25;
    ```


### 3.1.3 Aggregate Functions
- We use built in functions to aggregate data 
- Has to be used whenever an aggregate function has been used 
- `group by` – e.g. if we wanted sales by date:
    ```
    select transaction_dt_key, sum(sale_amt)
    from crm_target.b_transaction
    group by transaction_dt_key ; 
    ```
- Wide range of aggregate and analytical functions which can be used: 

    - `sum()` – sums the values on selected column 
    - `count()` – counts the # of values returned on selected column 
    - `count(distinct )` – counts the # of unique valued returned on selected column 
    - `min()` – returns the smallest value on selected column 
    - `max()` – returns the largest value on selected column 
    - `avg()` – returns the mean average of values on selected column


### 3.1.4 Like Clause
- When it is unknown what the correct format of a variable is in one of the tables (as they might differ BU to BU – e.g. brand names in the b_product table), we can use like function to help us out. 
- Note that this is typically quite inefficient, so avoid if possible.
- It is case sensitive so usually we use `upper(brand_name) like ‘%CLINIQUE%’` which converts the brand_name value to uppercase
- It is used in the where clause and is used like: 
    ```
    select brand_name
    from crm_target.b_product 
    where bu_key = 13
    and brand_name like ‘%CLINIQUE%’
    group by brand_name ;
    ```

### 3.1.5 Distinct Clause
- In order to get unique values from an output, use the distinct keyword.
- Used after the `select`, this will only return unique rows.

- E.g. `select distinct contact_key from table_name`
    - Returns only unique contact keys
    - This can be used in conjunction with a counting argument to count unique shoppers
        - E.g. `select count(distinct contact_key) from table_name`


### 3.1.6 Joining Tables
- You can join tables together to get more data 
- Documentation: https://www.w3schools.com/sql/sql_join.asp
- There are a few types of joins but the terminology for joining the tables is the same
- Note that `join` is the same as `inner join`, but `inner join` was used in older versions of SQL.
 ![alt text](image-14.png)
- You will mostly use `join` and `left join`, but the others can occasionally be handy.
- Something to note:
    - You might see some very old code using (+), but Oracle does not recommend using this anymore.

    ![alt text](image-15.png)
- Duplicate columns
    -   ```
        select 
            a.contact_key
        ,	b.contact_key
        from crm_target.b_transaction a
        join crm_target.b_contact b on a.contact_key = b.contact_key
        ```
    - If each table contains the same column name, you will need to specify which column from each table to join on
    - Give each table an alias here we use `a` and `b`
    - Another example:
        ```
        select 
            p.product_name
        ,	sum(t.item_amt) as sales
        from crm_target.b_transaction t 
        inner join crm_target.b_product p on p.product_key = t.product_key
         where t.bu_key = 17 
        and t.transaction_dt_key between 20220101 and 20220120
        and member_sale_flag = ‘Y’
        group by p.product_name;
        ```
        
    

### 3.1.7 Case When
- If we wanted to create a variable based of a condition (‘IF’ statement for example), we can use `case when`:
    ```
    select 
        case when column_1 = condition_1 then ‘A’
            when column_1 = condition_2 then ‘B’
            else ‘C’ end as letters
    ,	column_2
    from table_name
    group by case when column_1 = condition_1 then ‘A’
            when column_1 = condition_1 then ‘B’
            else ‘C’ end, column_2;
    ```
- Often used for creating age bands

    <img src="image-16.png" width=400>


### 3.2 B_TRANSACTION Table
[<u>Back to Top</u>](#sql-academy)

- ```CRM_TARGET.B_TRANSACTION``` ![alt text](image-12.png)
- Contains all transactional data 
- We use ```transaction_dt_key``` (date of transaction) to set which dates we want to see data for
- There are multiple ```transation_type_name``` (header rows) in the ```b_transaction``` table. The most used are:
    - Sale – shows the total sale breakdown for the purchase
    - Item – breaks the purchase down to item level 
    - Promotion – breaks the purchase down into Promotions which were used
    - Point – shows the point breakdown for the purchase (for member transactions)
- `member_key` / `contact_key` are unique numbers used to represent members. 
- A non-member will have a contact key of 0
- `member_sale_flag` can be used to distinguish a member transaction from a non member transaction. 



### 3.3 Main KPIs
[<u>Back to Top</u>](#sql-academy)

- ATV – $\text{average transaction value}=\frac{\text{total sales}}{\text{total transactions}}$

- ATF – $\text{average transaction frequency}=\frac{\text{total transactions}}{\text{no. of members}}$

- ACV – $\text{average customer value}=\frac{\text{total sales}}{\text{no. of members}}$

- IPT – $\text{items per transaction}=\frac{\text{no. of items}}{\text{total transactions}}$

- PPU – $\text{price per unit}=\frac{\text{total sales}}{\text{no. of items}}$

- YoY change – $\text{year on year change} = \frac{\text{this year value}}{\text{last year value}} - 1$ &nbsp; &nbsp; &nbsp; &nbsp; *(multiply by 100 for %)*

- MSP – $\text{member sales participation}=\frac{\text{member sales}}{\text{total sales}}\times 100$

- $\text{6 month active rate}=\frac{\text{no. of members shopped in last 6 months}}{\text{no. of members shopped in last 3 years}}$


### 3.4 Main Time Periods
- YTD – Year to Date – e.g. YTD March 2022 = Jan 2022 to March 2022
- MTD – Month to Date – e.g. first 3 weeks of MTD May 2022 = W18-20 May 2022
- WTD – Week to Date – a given week period- e.g. WTD Week 11 = Week 11 only
- MAT – Moving Annual Total - last 12 months of data – e.g. MAT April 2022 = May 2021 to April 2022 
- LTM – Last 12 Months – same as MAT
- YoY – Year on Year – This Year vs Last Year


### 3.5 Examples
- Total number of members shopping in Marionnaud Austria in January 2022
    ```
    select count(distinct contact_key) 
    from CRM_TARGET.B_TRANSACTION
    where bu_key = 13
    and transaction_dt_key between 20220103 and 20220130
    and member_sale_flag = ‘Y’
    and contact_key > 0
    and transaction_type_name = ‘Item’;
    ```
- Total Sales in MFR, YTD May 2022
    ```
    select sum(item_amt) 
    from CRM_TARGET.B_TRANSACTION
    where bu_key = 16
    and transaction_dt_key between 20220103 and 20220529
    and transaction_type_name = ‘Item’; 
    ```

### 3.6 B_PRODUCT Table
- `CRM_TARGET.B_PRODUCT`
    ![alt text](image-13.png)
- This table shows the information for every product sold
- We use product hierarchies to determine different categories and sub-categories BUs use (found in EU ADM model Document) 
- When calculation KPIs, we use always use the following exclusion: 
`kpi_exclusion_flag = ‘N’`
- *Used for all BUs – exception for MIT, see ADM data model document* 



### 3.7 Transactional Base Table
- Some of the larger BUs can take longer to run, so we have base tables created to use instead of joining the `b_transaction` and the `b_product` table 
- These are in place for: 
    - ICI – `ACHAN.ICI_NLBE_WTOR`
    - KV – `CRM_TARGET.T_ORDITEM_KV`
    - SD – `CRM_TARGET.T_ORDITEM_SD`
- These tables already include some of the transactional and product exclusions e.g. `transaction_type_name` 
- Use instead of the `b_transaction` table for ICINL,ICIBE,KVNL,KVBE,SD


### 3.8 Recap and Final Note
- Basic Code Structure
    ```
    select 
        column_1
    ,  sum(column_2)
    from table_name
    where condition_1
    and condition_2
    group by column_1;
    ```
- SQL is not case sensitive for syntax but is for record contents.
- It does not have significant whitespace like Python, so you don’t need to worry about indentation, although try to keep things neat.
- Typical best practice is to use all-caps, but this doesn’t matter too much.
- However, if you would like to specify a record, e.g. Estée Lauder, you will need to write it exactly as it is listed in the database, matching the upper and lowercase letters.
- You can always use something like select distinct brand_name and find your desired record to see how it is formatted.

# 4 Exercises - Part 1

### 4.1 Warm Up Questions - B_TRANSACTION only
[<u>Answers</u>](#41-warm-up-questions-answers)

1. Return all transactions that happened in MIT on the 1st of January 2023.

2. Return all unique members who shopped MFR on the 1st of January 2023.

3. What were the total Member Sales on the 30th of May 2023 in MAT?

4. How many rows are in the B_TRANSACTION table on the 16th of September 2023 for MHU? Hint: count(*) returns the number of rows.

5. How many items were bought in MCZ on the 25th of March 2023?


### 4.2 Exercises 1 
[<u>Answer</u>](#42-exercises-1-answers)

1. How many Dolce and Gabbana products are listed in B_PRODUCT which are sold in MCH?

2. For all transactions that occurred in 2023 Week 15 in MCZ, return the following columns: `bu_key, contact_key, transaction_dt_key, order_num, product_sku, product_name, item_amt and item_quantity_val`

3. Return the following KPIs for 2023 week 50 (ATV, ATF, ACV, IPT, PPU) in MSK.

4. Total sales and Member sales in 2023 week 2 in MFR.

5. What was the most popular SKIN CARE product SKU in MHU in 2023 in terms of total sales?

## 4.2 Adding more tables and Exercises 2

### B_STORE / WEB_STORES

- `select * from crm_target.b_store;`
- shows information for every store, e.g. `store_name`, `store_code` etc.
- `RCOVELL.WEB_STORES` : The `web_store_flag` is not regularly updated, so we use another table to distinguish online sales, `select * from rcovell.web_stores` to see what is in this table

### B_TIME

- `select * from crm_target.b_time;`
- join to the transaction table use `date_key` from the time table and `transaction_dt_key` from the transaction table
- can be very helpful for finding fiscal week/month/year

### Exercises 2

[Answers](#43-exercises-2-answers)

1. Top 5 stores by Member Sales in MAT for week 20 2023.

2. Member sales KPIs for (ATV, ATF, ACV, IPT, PPU) in MCZ in 2023, by fiscal quarter (Q1-Q4)

3. Top 5 men's fragrance SKUs sold in The Perfume Shop (TPS) within Liverpool throughout the December 2023 period.

4. For each week of January 2023, what percentage of members shopped on weekdays and on weekends in MIT?


## Answers

### 4.1 Warm Up Questions (Answers)
[<u>Back to Questions</u>](#41-warm-up-questions---b_transaction-only)

1.  Code:  
    ```
    select *
    from crm_target.b_transaction
    where bu_key = 17
    and transaction_dt_key = 20230101;
    ```
    <img src="image-17.png" width=500> 

2.  Code:  
    ```
    select 
        distinct(contact_key)
    from crm_target.b_transaction
    where bu_key = 16
    and transaction_dt_key = 20230101
    and contact_key > 0
    and member_sale_flag = 'Y';
    ```
    <img src="image-18.png" width=100> 

3.  Code:  
    ```
    select 
        sum(item_amt) as member_sales
    from crm_target.b_transaction
    where bu_key = 13
    and transaction_dt_key = 20230530
    and contact_key > 0
    and member_sale_flag = 'Y';
    ```
    <img src="image-19.png" width=100> 

4. Code:
    ```
    select 
        sum(item_amt) as member_sales
    from crm_target.b_transaction
    where bu_key = 13
    and transaction_dt_key = 20230530
    and contact_key > 0
    and member_sale_flag = 'Y';
    ```
    <img src="image-19.png" width=100> 

### 4.2 Exercises 1 (Answers)
[<u>Back to Question</u>](#42-exercises-1)
1. Code:
    ```
    select 
        count(distinct produt_sku)
    from
        crm_target.b_product
    where
        bu_key = 140
        and brand_name like '%Dolce%'
    ;
    ```
    
2. Code:
    ```
    select
        t.bu_key,
        contact_key,
        transaction_dt_key,
        order_num,
        product_sku,
        product_name,
        item_amt,
        item_quantity_val,
    from
        crm_target.b_transaction t
        join crm_target.b_produt p on t.product_key = p.produt_key
    where
        t.bu_key = 20
        and transaction_dt_key between 20230410 and 20230416
    ;
    ```

3. Code:
    ```
    select
        sum(item_amt) / count(distinct order_num) as ATV,
        count(distinct order_num) / count(distinct contact_key) as ATF,
        sum(item_amt) / count(distinct contact_key) as ACV,
        sum(item_quantity_val) / count(distinct order_num) as IPT,
        sum(item_amt) / sum(item_quantity_val) as PPU
    from
        crm_target.b_transaction t
        join crm_target.b_product p on t.product_key = p.product_key,
    where
        t.bu_key = 21
        and transaction_dt_key between 20231211 and 20231217
        and contact_key > 0 
        and member_sale_flag = 'Y'
        and transaction_type_name = 'Item'
        and kpi_exclusion_flag = 'N'
    ;
    ```

    > Sense-checking KPIs: These can often by checked on a report in WV in the 201 to make sure your numbers seem right

4. There are two ways to go about this query. First, we can use two separate queries for each case, whether a sale is from a member or not:

    ```
    -- total sales
    select
        sum(item_amt) as total_sales
    from
        crm_target.b_transaction t
        join crm_target.b_product p on t.product_key = t.product_key
    where
        t.bu_key = 16
        and transaction_dt_key between 20230109 and 20230115
        and transaction_type_name = 'Item'
        and kpi_exclusion_flag = 'N'
    ;

    -- member_sales
    select
        sum(item_amt) as member_sales
    from
        crm_target.b_transaction t
        join crm_target.b_product p on t.product_key = t.product_key
    where
        t.bu_key = 16
        and transaction_dt_key between 20230109 and 20230115
        and transaction_type_name = 'Item'
        and kpi_exclusion_flag = 'N'
        and member_sale_flag = 'Y'
        and contact_key > 0
    ;
    ```
    However, there is a cleaner and more efficient way of finding the results. You may have noticed the above queries are very similar, just with two slightly different cases in the `where` clause. We can use a `case when` statement to make our lives easier here.

    ```
        select
        sum(item_amt) as total_sales,
        sum( case when contact_key > 0 and member_sale_flag = 'Y' then item_amt end) as member_sales
    from
        crm_target.b_transaction t
        join crm_target.b_product p on t.product_key = t.product_key
    where
        t.bu_key = 16
        and transaction_dt_key between 20230109 and 20230115
        and transaction_type_name = 'Item'
        and kpi_exclusion_flag = 'N'
    ;
    ```

5. Code
    ```
    select
        product_sku,
        brand_name,
        product_name,
        volume_val,
        sum(item_amt) as total_sales
    from    
        crm_target.b_transaction t
        join crm_target.b_product p on t.product_key = p.product_key
    where
        t.bu_key = 5
        and transaction_dt_key between 20230102 and 20231231
        and kpi_exclusion_flag = 'N'
        and product_hier_3_l1_name = 'SKIN CARE'
    group by
        product_sku
    order by 
        total_sales desc
    ;
    ```

### 4.3 Exercises 2 (Answers)

[Questions](#42-adding-more-tables-and-exercises-2)

1. Code:
    ```
    select
        t.store_key,
        s.store_name,
        sum(item_amt) as member_sales
    from
        crm_target.b_transaction t 
        join crm_target.b_product p on t.product_key = p.product_key
        join crm_target.b_store s on t.store_key = s.store_key
        join crm_target.b_time d on t.transaction_dt_key = d.date_key
    where
        t.bu_key = 13
        and d.fiscal_wk_idnt = 202220
        and transaction_type_name = 'Item'
        and member_sale_flag = 'Y'
        and contact_key > 0
        and p.kpi_exclusion_flag = 'N'
    group by 
        t.store_key
        s.store_name
    order by 
        member_sales desc
    ;
    ```
