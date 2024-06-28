# mfr-high-skincare-model

## Running and Key Notes

You can train a new model, or predict using a pre-trained model by setting the months in the config file, and then running `run_train_model.py` or `run_predict_model.py` respectively.

## Parameters and File Structure

### Parameters

* **bu_code : str**
    * Do not change 

* **bu_key : int**
    * Do not change 

* **model_label : str**
    * The models are named after which months they were trained on, don't change this unless you have trained a new model to use.

* **run_type : str**
    * Currently not used, do not change

* **current_month_flag : int**
    * Currently not used, do not change

* **specified_start_month : int**
    * This is used to select either the training data starting month, and will be used in the model name, or to select members to be predicted on

* **specified_end_month : int**
    * This is used to select either the training data starting month, and will be used in the model name, or to select members to be predicted on

* **output_table_name : str**
    * This is the output table name in ADM. The results can also be found in the **data/processed** folder.

### File Structure

```
├───conf                <- Where parameters and creds are found
│   ├───creds           <- creds for accessing ADM
│   ├───core            <- script that reads config file
│   └───config.yml      <- parameters
├───data
│   ├───interim
│   ├───processed
│   └───raw
├───logs
│   └───visualisations
├───models              <- serialized models        
├───notebooks
└───src                 <- all code for model
    ├───dataset
    ├───models
    └───output
```

## Technical Details

### SQL procedures

There are two SQL procedures - one for training and one for predicting. They are almost identical, the only difference is that the training procedure has the `high_skincare_flag` and will look into the next year for the given months in the config folder. So, if you put in 202401 and 202412 as your start and end months, respectively, then it will use 202501 and 202512 for the `high_skincare_flag`.

### Model Coefficient Explanation

In the **logs/visualisations** folder, there is a model_coefficients chart. The numbers represent the average change in odds when the scaled feature changes by 1 unit. They are virtually meaningless to humans. I have tried hard to get them into meaningful numbers, which you can find in the notebooks relevant section, but it doesn't actually work. All they represent is how "important" a feature is, relative to the other features.

### Interpreting a Confusion Matrix

It consists of four parts, as seen below:

$$
\begin{bmatrix}
    \text{True Negatives} & \text{False Positives} \\
    \text{False Negatives} & \text{True Positives}
\end{bmatrix}
$$

True Negatives (TN) and True Positives (TP) are obviously what we want the most of, and the False Positives (FP) and False Negatives (FN) are what we want the least of. Thus, an ideal confusion matrix will have the top left and bottom right elements as the two highest counts, and the remaining two, the top right and bottom left as the two lowest counts. 

In our matrix above, we can see that the bottom left has a lot of members as FN, and so we want to reduce this. 


Next, we can try to understand **Precision**, **Recall** and the **F1 score** which are measures of accuracy of the model.

$$\text{Precision} = \frac{\text{TP}}{\text{TP}+\text{FP}}\quad \text{and} \quad \text{Recall} = \frac{\text{TP}}{\text{TP}+\text{FN}}$$

We can interpret Precision as the following: our model has a Precision of 0.51, so when it predicts a member as 'HIGH SKINCARE', it is correct 51% of the time. It can be seen by comparing the second column of the matrix.

We can interpret Recall as the following: our model has a Recall of 0.82, so it correctly identifies 82% of all 'HIGH SKINCARE' members. It can be seen by comparing the second row of the matrix.

### TODOS

**High Priority**

- In train.py, `drop_weird_enrol_date_members()`: automate it so that you don't have to manually exclude members with bad enrol dates, e.g. any after current date or before 1900

**Nice to Haves**

- In dataset.py, `run_sql_proc()`: if you get a table does not exist or table already exists error when running the sql proc, try deleting/creating the table and rerunning and if it happens again, log the error and exit. Function shells are there but do nothing currently
    - If you get a temp or tablespace error, try again in case the server is just a bit busy rn but if it fails again then throw the error and exit

- In train.py, `convert_dates_to_days()`: update to use datetime library instead of pd.datetime as will be deprecated in future releases
