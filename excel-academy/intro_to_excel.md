# AS Watson Excel Academy

![AS Watson and Databricks Logos](images/ASWxExcelLogo.png)

## Table of Contents

[1.0 Shortcuts and Formulas](#10-shortcuts-and-formulas)
* [1.1 Logical Functions](#11-logical-functions-if-and-or-not-and-ifs)
* [1.2 SUMIFS](#12-sumifs)
* [1.3 VLOOKUP](#13-vlookup)
* [1.4 Other Useful Functions](#14-other-useful-functions)

[2.0 Report Building Techniques](#20-report-building-techniques)
* [2.1 Creating Charts](#21-creating-charts)
* [2.2 Pivot Tables](#22-pivot-tables)
* [2.3 Pivot Charts](#23-pivot-charts)
* [2.4 Drop Downs](#24-drop-downs)

[3.0 Exercises](#30-exercises)
* [3.1 Cereal Dataset](#31-exercise-1-cereal-dataset)
* [3.2 KPI Dataset](#32-exercise-2-kpi-dataset)
* [3.3 ]

## 1.0 Shortcuts and Formulas

[Back to Top](#as-watson-edp-academy)

#### Moving Around an Excel File

* Double clicking the box in the bottom right of the active cell applies the formula down the column until there is no more data. This is useful when there is a large amount of data – saves you scrolling for ages. Make sure to lock the required cells in the formula though!

* CTRL + arrow key: Will move cursor to the end of the current object

* CTRL + A: selects all of the current object

* CTRL + SHIFT + L: Quickly adds filter drop down to a table

* CTRL + T: Automatically creates a table of what is highlighted

* CTRL + ALT + V: paste special values options 

* CTRL + F: Find and replace values

* F4: When referencing cells, you can use F4 to "lock" the cell values

* F2: If looking at a formula, this can be used to see what cells/columns the formula is referencing

#### ALT Shortcuts

ALT shortcuts don't rely on you pressing all the keys at once, so you can hit them in the right order and it will carry out the command.

* ALT + H + O + I: Changes all the column widths to fit all the filled cells in each highlighted column

* ALT + =: If you highlight a table of numbers, then this will sum the relevant columns and rows

[Back to Top](#as-watson-edp-academy)

### 1.1 Logical Functions: `IF`, `AND`, `OR`, `NOT` and `IFS` 

In Excel, the IF function allows you to make a logical comparison between a value and what you expect by testing for a condition and returning a result if that condition is True or False.

* `=IF(Something is True, then do something, otherwise do something else)`

But what if you need to test multiple conditions, where let’s say all conditions need to be True or False (AND), or only one condition needs to be True or False (OR), or if you want to check if a condition does NOT meet your criteria? All 3 functions can be used on their own, but it’s much more common to see them paired with IF functions.

Here are overviews of how to structure AND, OR and NOT functions individually. When you combine each one of them with an IF statement, they read like this:

* AND: `=IF(AND(Something is True, Something else is True), Value if True, Value if False)`

* OR: `=IF(OR(Something is True, Something else is True), Value if True, Value if False)`

* NOT: `=IF(NOT(Something is True), Value if True, Value if False)`

If you need more than one condition in your `IF` statement, then you can use `IFS` like so:

* `= IFS(Something is True 1, Value if True 1, Something is True 2, Value if True 2, Something is True 3, Value if True 3, …)`

For further information, and *examples* see [here](https://support.microsoft.com/en-us/office/using-if-with-and-or-and-not-functions-in-excel-d895f58c-b36c-419e-b1f2-5c193a236d97).

### 1.2 `SUMIFS`

[Back to Top](#as-watson-edp-academy)

The SUMIFS function adds all of its arguments that meet multiple criteria. For example, you would use SUMIFS to sum the number of stores in a BU who (1) have more than 1,000 monthly shoppers and (2) who reside in a particular city.

* `=SUMIFS(Column to Sum, Column 1 to Check, Criteria 1, Column 2 to Check, Criteria 2,...)`

For further information, and *examples* see [here](https://support.microsoft.com/en-us/office/sumifs-function-c9e748f5-7ea7-455d-9406-611cebce642b).

**Useful Trick**

When we export tables from ADM, we often have them in a similar form to below:
| A | B | C | D |
| ------ | ------------ | ---------- | ----- |
| **BU Key** | **Fiscal Month** | **Store Code** | **Sales** |
| 16 | 202401 | 4019 | 1,200,457 |
| 16 | 202402 | 4027 | 1,345,729 |
| ... | ... | ... | ... |

We can use `SUMIFS` in a clever way to quickly get aggregated information we might want, for example, all the sales for the same BU key and fiscal month, we could do as follows:

* `=SUMIFS(D:D, A:A, @A:A, B:B, @B:B)`

The @ symbol is needed to return information from the same row, but is a bit confusing still. See [here](https://stackoverflow.com/questions/69700385/what-does-the-symbol-mean-in-excel-formula-outside-a-table) for a deeper explanation. If we put this in our table, this will look like so:

| A | B | C | D | E |
| ------ | ------------ | ---------- | ----- | -|
| **BU Key** | **Fiscal Month** | **Store Code** | **Sales** | **Aggregated Sales** |
| 16 | 202401 | 4019 | 1,200,457 | 2,546,186 |
| 16 | 202401 | 4027 | 1,345,729 | 2,546,186 |
| ... | ... | ... | ... | ... |

So, if we had different months or different bu keys, then they would get aggregated the same way it has here, which can be very handy when using much larger tables, and trying to work out %'s of sales or anything similar.

### 1.3 `VLOOKUP`

[Back to Top](#as-watson-edp-academy)

Use VLOOKUP when you need to find things in a table or a range by row. For example, look up a price of an automotive part by the part number, or find an employee name based on their employee ID.

In its simplest form, the VLOOKUP function says:

* `=VLOOKUP(What you want to look up, where you want to look for it, the column number in the range containing the value to return, return an Approximate or Exact match – indicated as 1/TRUE, or 0/FALSE)`

### 1.4 Other Useful Functions

* `=LEFT/RIGHT(abcd, n)`: returns the first n digits from the left/right of abcd

* `=INDEX( MATCH() )`: can be used together to return a value from a grid, in a similar fashion to `VLOOKUP`

* `=IFERROR(value if no error, value if error)`: returns one value if there is no error, returns another if there is, this is useful to make spreadsheets readable if dividing by zero

* `=SUM()`: sums a given range

* Using a \$ in a formula locks whatever the \$ is before, e.g. $A1:$B6 will lock A and B but not 1 and 6. To lock both use $A$1 etc. This is useful when needing repeated formulas in other columns. For example if you are always referring to a fixed cell for BU code, you can lock this for all formulas. There is also a shortcut for this with F4, as seen in the [shortcuts section](#moving-around-an-excel-file).


## 2.0 Report Building Techniques:

[Back to Top](#as-watson-edp-academy)

### 2.1 Creating Charts

To create a chart using data from a table in Excel, we can follow these steps:

1. Highlight the table you wish to visualise
2. Select “Insert” tab in the toolbar
3. Select recommended charts then choose the most appropriate chart 
4. To add different features to the chart, select the “Chart Design” tab.

The type of chart you want to use depends on how you’d like to visualise the date. For example, line charts can be used to visualise how a KPI changes over time, whereas a bar chart can be used to different proportions like year on year change in sales


### 2.2 Pivot Tables

[Back to Top](#as-watson-edp-academy)

#### Creating a Pivot Table

When we have a large set of data in Excel with many columns, we sometimes may want to summarise only a sub-set of the table. A fast way to do this would be to use a pivot table. 
To create a pivot we follow these steps: 

1. Highlight the table/data you wish to make a Pivot Table with
2. Go to “Insert” and select “Pivot Table” 
3. A pop up will appear, and choose the options you'd like

#### Selecting Fields

Drag and drop the fields from the top of the “Pivot Table Fields” into the “Filter”, “Columns”, “Rows” and “Values”. 
* The “Filter” allows you to use that field as a filter for the table 
* The “Columns” will place the fields along the top of the table 
* The “Rows” will place the fields along the side of the table 
* The “Values” will be the variables used in the table 

#### Calculated Fields

If we want to calculate some fields which don’t exist in our data, we can do this for use in our pivot tables. To do this we use the following steps: 
1. On the ribbon at the top, select “PivotTable Analyze”, and select “Fields, Items, & Sets”. Then press “Calculated Field”.
2. In the pop up, name the field, and create the formula you would like to use using the existing fields in the pivot table. Once completed press “OK”
3. The created field should now appear under the other fields in the pivot chart. 

#### Slicers

To select filters easily for your pivot table. You can link the pivot table to a slicer. 
1. Select the pivot chart which you would like to create a slicer for and on the “PivotTable Analyze” tab, select “Insert Slicer”. 
2. Select which field you would like the slicer to work for, then hit “OK”
3. To use the slicer, just select variable you would like to filter the chart using, and the pivot chart will automatically filter using the slicer

If you have more than one pivot table which uses the same data source, you’ll be able to connect your slicers to work across all the pivot tables. **When creating the Pivot Tables, you will need to check the box that says "Add this data to the Data Model", otherwise this won't work.**
1. Select the slicer with the field you would like to use across more tables. On the “Slicer” tab, select “Report Connections”. 
2. Select the tables which you would like to connect. Then press “OK”, and this should connect all the tables to the slicer.


### 2.3 Pivot Charts

[Back to Top](#as-watson-edp-academy)

Sometime we might want to create a chart that needs to change depending on a variable. For example, by changing BUs. We can link a chart to a pivot table and slicer to change when a variable is changed. 
To create the chart: 
1. Select the pivot table you want to create into a chart and select the “PivotChart Analyze” tab, and select “PivotChart”. 
2. Select the type of chart you wish to use. You can edit these charts once you select “OK” using the “Format” tab

This should connect all existing slicers to chart (given the slicer is connected to the same table) if not, use the previous slide to create/connect a slicer


### 2.4 Drop Downs

[Back to Top](#as-watson-edp-academy)

A drop down is a very useful tool in reports when we want to filter through certain variables 
To create a drop down we follow these steps: 
1. Create the list of variables you would like to use in a column which isn’t used on a sheet in Excel
2. Click on the cell where you would like to create the drop down
3. Go to the “Data” tab and select “Data Validation”, then select “Data Validation…” 
4. Then under “Allow” select list. Then under “Source”, highlight the cells which you would like to use. Then select “OK”

> Note: to undo the drop down, follow the same steps, although at the “Allow” step, select number instead of list.


## 3.0 Exercises

[Back to Top](#as-watson-edp-academy)

### 3.1 Exercise 1 (Cereal Dataset)

Make a copy of the Cereal dataset, and answer the following questions (they are a copy of the ones found in the Questions tab in the spreadsheet). These are to get you started using formulas in excel, and aren't trying to trick you or overcomplicate anything.

1. What would be the total number of calories you would consume if you were to eat 1 bowl of every Kellogg’s manufactured cereal?

2. What amount of sugar does Great Grains Pecan contain?

3. What would be the total amount of potassium you would consume if you were to eat 1 bowl of every General Mills manufactured cereal which contained exactly 110 calories? 

4. Using the filter on the “Questions” page, make it so that the total number of calories you would consume if you were to eat 1 bowl of every cereal from the selected manufacturer. 

### 3.2 Exercise 2 (KPI Dataset)

[Back to Top](#as-watson-edp-academy)

#### Generating the dataset 
For this exercise, we want you to generate your own dataset! We want the following columns for our dataset, with examples of what the data should be like:

| BU_CODE | FISCAL_DAY_DESC | FISCAL_WK_IDNT | CHANNEL | SEG_NUM | GENDER | AGE | SALES | MEMBERS | ORDERS | ITEMS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MCZ | MONDAY | 202401 | ONLINE | LOYAL | Female | 26-35 | 4107.5 | 2 | 2 | 5  |
| MHU | WEDNESDAY | 202403 | STORE | NEW | Male | 56-65 | 2198 | 1 | 1 | 3  |

* The BUs should only be from Marionnaud Central Europe (MCE) which is MHU, MCZ, MSK and MRO.
* The data should only be from Fiscal January 2024
* It should only be member data, no non-member transactions
* It should use the RFM segments for `SEG_NUM`
* Channel is online for transactions from the Web stores, and Store for anything else

> Remember that MCE don't necessarily use Euros as their currency, so the sales amounts might seem a bit high but don't worry about this for now. If we were actually reporting on this data, then we would want to convert them to the same currency. 

Once you have this dataset, copy it into an excel file (it should be about 17,000 rows of data, so it will take a moment to select all of it).

If you are struggling to recreate the dataset, there is an example of code that generates it in the datasets folder, but only look at this if you are really stuck! 

#### Presenting the Dataset

Create a new blank excel and paste your sql query results into the new tab. We want to compare four KPIs (ACV, ATV, PPU and IPT) across four different charts by week and day, that can be filtered by BU, Channel, RFM Segment, Gender and Age. 

The filters should automatically change each chart at the same time (hint: slicers!). The charts should all be visible at the same time, and it should look pretty too.

> There are multiple ways of doing this, so don't worry too much if you don't do it the same way as the "answers" did, as long as you get the same results!