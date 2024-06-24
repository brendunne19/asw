# AS Watson Excel Academy

![AS Watson and Databricks Logos](images/ASWxExcelLogo.png)

## Table of Contents

[1.0 Formulas](#10-simple-formulas)


## 1.0 Shortcuts and Formulas

[Back to Top](#as-watson-edp-academy)

#### Moving Around an Excel File

* Double clicking the box in the bottom right of the active cell applies the formula down the column until there is no more data. This is useful when there is a large amount of data – saves you scrolling for ages. Make sure to lock the required cells in the formula though!

* CTRL + arrow: Will move cursor to the end of the current object

* CTRL + A: selects all of the current object

* CTRL + SHIFT + L : Quickly adds filter drop down to a table

* F4: When referencing cells, you can use F4 to "lock" the cell values

* F2: If looking at a formula, this can be used to see what cells/columns the formula is referencing

#### ALT Shortcuts

ALT shortcuts don't rely on you pressing all the keys at once, so you can hit them in the right order and it will carry out the command.

* ALT + h + o + i: Changes all the column widths to fit all the filled cells in each highlighted column

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

* `LEFT/RIGHT(abcd, n)`: returns the first n digits from the left/right of abcd

* `INDEX(MATCH)`: can be used together to return a value from a grid, in a similar fashion to `VLOOKUP`

* `IFERROR`: returns one value if there is no error, returns another if there is, this is useful to make spreadsheets readable if dividing by zero

* `SUM`: sums a given range

* Using a \$ in a formula locks whatever the \$ is before, e.g. $A1:$B6 will lock A and B but not 1 and 6. To lock both use $A$1 etc. This is useful when needing repeated formulas in other columns. For example if you are always referring to a fixed cell for BU code, you can lock this for all formulas. There is also a shortcut for this with F4, as seen in the [shortcuts section].(#10-shortcuts-and-formulas)


## 2.0 Report Building Techniques:

### 2.1 Creating Charts

### 2.2 Pivot Tables

### 2.3 Pivot Charts

### 2.4 Drop Downs

### 2.5 Pasting types


## 3.0 Exercises
