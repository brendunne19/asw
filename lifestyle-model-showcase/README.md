# predict-lifestyle-model

> *Note that some folders have been removed, `data`, `models` and `notebooks`, in order for me to share this publicly but are shown below in the folder structures.*

## Running and Key Notes

The model is scheduled to train on MFR data and is used to predict on this BU every month with **run_predict_model.py**. When this happens, the log files are updated and it will also create the profiling results in the [visualisation folder](#file-structure).

### Things to note:

* N/A

## Parameters and File Structure

### config.yml 

> *To see the location of the config file, go to [File Structure](#file-structure)*

**Parameters:** 
* **bu_code : str**
    * Do not change 

* **bu_key : int**
    * Do not change 

* **model_label : str**
    * Multiple options available, see the `mce-mit-training/models` folder in to view all options 
    * MIT should default to `'equal_model'` (as they don't want one segment to be too small) whilst the rest in MCE should default to `'upsample5_model'`

* **model_month_label : str**
    * Multiple options available, see the `mce-mit-training/models` folder in to view all options, and is used in conjunction with **current_month_model_flag**, to choose whether to use the current month training to predict, or a previous one
    * Should default to `'MAYyy'`, where `'yy'` is the current year

* **current_month_model_flag : int**
    * Used in conjunction with **model_month_label**, and can be set to `0` when wanting to select which month of training data to use, or can be set to `1` to select the current month's training data

* **run_type : str**
    * Used in conjunction with **current_month_flag** and can be set to either: 
        * `'ONE-OFF'`: Used when user wants to specify which dates to run for
        * `'MONTHLY'`: Used for regular monthly updates and runs for current fiscal month

* **current_month_flag : int** 
    * Used in conjunction with **run_type** and can be set to either:
        * `0`: Used when user wants to run it one-off for a specified fiscal month
        * `1`: Used for regular monthly updates and runs for the current fiscal month

* **specified_month_idnt : int**
    * In `yyyymm` format, will run for this given month

* **specified_month_name : str**
    * In `'MMM'` format, will run for this given month

* **period_length : int**
    * Number of months to collect data on members for, the default should be `23` to use the last two years of data for prediction

### File structure

```
├───conf                <- parameters for training  
├───data
│   ├───interim         <- Intermediate data that has been transformed
│   ├───processed       <- The final data sets for modeling
│   └───raw             <- The original data (tables in ADM)
├───logs
├───models              <- Trained and serialized models - not used, use ones from mce-mit-training
├───notebooks           <- Exploratory Jupyter notebooks and previous running
└───src                 <- Source code for training model
    ├───data            <- Scripts to generate data
    │   ├───populated_sql
    │   └───sql_templates
    ├───outputs         <- Scripts to upload results to ADM
    ├───models          <- Script to create features and train model
    └───visualisation   <- Results oriented visualisations
        └───profiling-outputs

```

## Technical Details

This is a simplified overview of how the code works and is set up to run.

### run_predict_model.py

This is the master running file for predicting with the model. It references a few different files of which contain the bulk of the code, thus it doesn't contain much itself. It should almost read in plain english what is happening and in what order things happen.

There are a few key imports near the beginning of the file:

```
import src.models.predict_model as proc
import src.models.visualise_profiles as visual_proc
from conf.core import config as conf
from src.utils import *
```

`proc` and `visual_proc` are where the bulk of the code lies, and is where the parameter Class is found,  where the Class for predicting with the model is found, and where the visualisation Class is found. 

`conf` is used to read the parameters from the config file, and is also called in the parameter class in `proc` to help.

`src.utils` is where functions that may be used across multiple files can be found, such as executing SQL. 