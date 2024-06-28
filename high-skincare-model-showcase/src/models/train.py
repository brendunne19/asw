# other files
import src.utils as utils

# proprietary packages
import my_blob as blob

# global packages
from loguru import logger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import pickle
from scipy.stats import skew
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report 


class CleanData:

    def __init__(self, MonthParams):

        self.MonthParams = MonthParams


    def check_member_split(self, df) -> None:

        """Check and visualise the member split between high and low skincare members."""

        # showing the low vs high skincare member split
        high_member_count = df.groupby('high_skincare_flag')['high_skincare_flag'].count()[1]
        low_member_count = df.groupby('high_skincare_flag')['high_skincare_flag'].count()[0]
        total_members = high_member_count + low_member_count

        # Data
        x_label = (f"Member Count (%) of {format(total_members, '0,')} total members")
        weight_counts = {
            "High Skincare Members": np.array([high_member_count * 100/total_members]),
            "Low Skincare Members": np.array([low_member_count * 100/total_members]),
        }

        fig, ax = plt.subplots(figsize=(5,5))
        bottom = np.zeros(1)

        for boolean, weight_count in weight_counts.items():
            p = ax.bar(x_label, weight_count, label=boolean, bottom=bottom)
            bottom += weight_count

        ax.legend(loc="upper right")
        ax.text(0,6, str(round((high_member_count * 100/total_members), 0)) + '%', ha='center', color='white', size=15, fontweight='bold')
        ax.text(0,55, str(round((low_member_count * 100/total_members), 0)) + '%', ha='center', color='white', size=15, fontweight='bold')
        plt.rc('font', size = 12)
        plt.rc('xtick', labelsize = 12)
        plt.rc('ytick', labelsize = 12)
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_member_split')


    def add_more_features(self, df) -> pd.DataFrame:

        df['sales_change_12_months'] = df['ty_sales'] - df['ly_sales']
        df['skincare_sales_change_12_months'] = df['skincare_sales'] - df['previous_yr_skincare_sales']  

        return df
    
    
    def check_nulls_and_replace(self, df) -> pd.DataFrame:

        null_prcs = 100 * df.isnull().sum().sort_values(ascending=False) / len(df)
        non_zero_null_prcs = null_prcs[null_prcs > 0]

        fig, ax = plt.subplots(1, 1, figsize=[10, 10])
        sns.barplot(x=non_zero_null_prcs, y=non_zero_null_prcs.index, ax=ax)
        ax.set_xlabel('Percentage null')
        ax.set_title('Columns with >0 null values')
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_null_columns')

        df.replace(np.nan, 0, inplace=True)

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_df.csv', 
                              f'data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_df.csv',
                              df)

        return df
    

    def store_metadata(self, df) -> None:

        metadata_df = pd.DataFrame(df.pop('contact_key'))
        metadata_df['email_flag'] = df.pop('email_flag')
        metadata_df['sms_flag'] = df.pop('sms_flag')
        metadata_df['dm_flag'] = df.pop('dm_flag')

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_metadata_df.csv', 
                              f'data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_metadata_df.csv',
                              metadata_df)
        

    def remove_skew(self, df) -> pd.DataFrame:

        # Find numeric values
        numeric_cols = df.columns[(df.dtypes == 'int64') | (df.dtypes == 'float64')].tolist()

        # Don't consider binary variables
        for col in numeric_cols:
            if (df[col].min() == 0) and (df[col].max() == 1):
                numeric_cols.remove(col)

        # Calculate skew and store in a dataframe
        skews = pd.DataFrame({
            'column': numeric_cols, 
            'skew': skew(df[numeric_cols])
        }).sort_values(by='skew')

        for i, row in skews.iterrows():
            
            # Calculate the skew if log transformed. If it is an improvement, apply it to the main merged dataframe
            n_zeros = sum(df[row['column']] == 0)
            n_neg = sum(df[row['column']] < 0)
            
            if n_zeros == 0 and n_neg == 0:
                skews.loc[i, 'skew_if_logged'] = skew(np.log(df[row['column']]))
                skews.loc[i, 'skew_change'] = abs(skews.loc[i, 'skew_if_logged']) - abs(skews.loc[i, 'skew'])
                if skews.loc[i, 'skew_change'] < 0:
                    df[row['column']] = np.log(df[row['column']])
                                                    
            elif n_zeros > 1 and n_neg == 0:
                skews.loc[i, 'skew_if_logged'] = skew(np.log1p(df[row['column']]))
                skews.loc[i, 'skew_change'] = abs(skews.loc[i, 'skew_if_logged']) - abs(skews.loc[i, 'skew'])
                if skews.loc[i, 'skew_change'] < 0:
                    df[row['column']] = np.log1p(df[row['column']])
                                                    
            else:
                skews.loc[i, 'skew_if_logged'] = skew(np.log1p(df[row['column']] + abs(min(df[row['column']]))))
                skews.loc[i, 'skew_change'] = abs(skews.loc[i, 'skew_if_logged']) - abs(skews.loc[i, 'skew'])
                if skews.loc[i, 'skew_change'] < 0:
                    df[row['column']] = np.log1p(df[row['column']] + abs(min(df[row['column']])))                                             
                
        fig, (ax, ax1) = plt.subplots(1, 2, figsize=[10, 7])
        sns.barplot(x='skew', y='column', data=skews, ax=ax)
        sns.barplot(x='skew_if_logged', y='column', data=skews, ax=ax1)
        plt.tight_layout()
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_skewed_columns')

        return df


    def drop_erroneous_date_members(self, df) -> tuple[pd.DataFrame, pd.DataFrame]:

        """Drop any members with 0 as their last_purchase_date, last_skincare_purchase_date or first_purchase_dt
        as not sure how they even got into the dataset in the first place"""

        metadata_df = blob.download_dataframe_from_blob(f'high-skincare-model/data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_metadata_df.csv', 
                              f'data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_metadata_df.csv')

        num_rows_dropped = 0
        total_rows = len(df.index)

        num_rows_dropped += len(df[df['last_purchase_date'].apply(lambda x: isinstance(x, int))].index)
        metadata_df.drop(index=df[df['last_purchase_date'].apply(lambda x: isinstance(x, int))].index, inplace=True)
        df.drop(index=df[df['last_purchase_date'].apply(lambda x: isinstance(x, int))].index, inplace=True)

        num_rows_dropped += len(df[df['last_skincare_purchase_date'].apply(lambda x: isinstance(x, int))].index)
        metadata_df.drop(index=df[df['last_skincare_purchase_date'].apply(lambda x: isinstance(x, int))].index, inplace=True)
        df.drop(index=df[df['last_skincare_purchase_date'].apply(lambda x: isinstance(x, int))].index, inplace=True)

        num_rows_dropped += len(df[df['first_purchase_dt'].apply(lambda x: isinstance(x, int))].index)
        metadata_df.drop(index=df[df['first_purchase_dt'].apply(lambda x: isinstance(x, int))].index, inplace=True)
        df.drop(index=df[df['first_purchase_dt'].apply(lambda x: isinstance(x, int))].index, inplace=True)

        logger.info(f'{round(100 * num_rows_dropped / total_rows, 0)}% rows dropped')

        return df, metadata_df
    

    def drop_weird_enrol_date_members(self, df, metadata_df) -> tuple[pd.DataFrame, pd.DataFrame]:

        """Dropping members with messed up enrol dates. Needs update from TODOS in README."""

        metadata_df.drop(index=df[df['enrol_dt'] == datetime.datetime.strptime('3000-01-15 00:00:00', '%Y-%m-%d %H:%M:%S')].index, inplace=True)
        metadata_df.drop(index=df[df['enrol_dt'].apply(lambda x: isinstance(x, int))].index, inplace=True)
        metadata_df.drop(index=df[df['enrol_dt'] == datetime.datetime.strptime('4200-11-28 00:00:00', '%Y-%m-%d %H:%M:%S')].index, inplace=True)

        df.drop(index=df[df['enrol_dt'] == datetime.datetime.strptime('3000-01-15 00:00:00', '%Y-%m-%d %H:%M:%S')].index, inplace=True)
        df.drop(index=df[df['enrol_dt'].apply(lambda x: isinstance(x, int))].index, inplace=True)
        df.drop(index=df[df['enrol_dt'] == datetime.datetime.strptime('4200-11-28 00:00:00', '%Y-%m-%d %H:%M:%S')].index, inplace=True)

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_metadata_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_metadata_df.csv',
                              metadata_df)

        return df
    

    def convert_dates_to_days(self, df) -> pd.DataFrame:

        """Turning the date of purchase columns into number of days since purchase from today AND for enrol_dt. Needs update from TODOS in README"""

        df['last_purchase_date'] = (pd.datetime.now() - pd.to_datetime(df['last_purchase_date'], infer_datetime_format=True)).dt.days
        df['last_skincare_purchase_date'] = (pd.datetime.now() - pd.to_datetime(df['last_skincare_purchase_date'], infer_datetime_format=True)).dt.days
        df['first_purchase_dt'] = (pd.datetime.now() - pd.to_datetime(df['first_purchase_dt'], infer_datetime_format=True)).dt.days
        df['enrol_dt'] = (pd.datetime.now() - pd.to_datetime(df['enrol_dt'], infer_datetime_format=True)).dt.days

        # if there is only one transaction, then days_between_trxs is 0, but that is the opposite behaviour of what we want,
        # as the lower the days between a transaction, the more a member visits the store so we set it to the max length of the period
        df['days_between_trxs'].replace(to_replace=0, value = 365, inplace=True)

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_dates_df.csv', 
                              f'data/interim/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_dates_df.csv',
                              df)
        
        return df
    

    def creating_flag_features(self, df) -> pd.DataFrame:

        """Convert any categorical or ordinal features into flags (Gender, Age and RFM)."""

        df = pd.get_dummies(data = df, columns=['gender_name'])

        df.drop(['birth_dt'], axis=1, inplace=True)

        # Define the mappings
        rfm_map = {
            'GONE AWAY': 0,
            'LAPSED': 1,
            'INACTIVE': 2,
            'NEW': 3,
            'ONE-OFFS': 4,
            'REGULAR': 5,
            'LOYAL': 6,
            'VIP': 7
        }

        age_map = {
            'Unspecified': 0,
            'Under 20': 1,
            '21-25': 2,
            '26-35': 3, 
            '36-45': 4,
            '46-55': 5, 
            '56-65': 6, 
            '65+': 7  
        }

        # Apply the mappings
        df['rfm_segment'] = df['seg_num'].map(rfm_map) 
        df['age_band'] = df['age'].map(age_map)

        # dropping old columns
        df.drop(['age', 'seg_num'], axis=1, inplace=True)

        return df


    def scale_data(self, df) -> pd.DataFrame:

        """Normalise all columns apart from target column."""

        scaler = StandardScaler()

        columns_to_scale = ['ty_sales', 'ty_units', 'ty_visits', 'ly_sales',
            'ly_units', 'ly_visits', 'days_between_trxs', 'last_purchase_date',
            'last_skincare_purchase_date', 'enrol_dt', 'first_purchase_dt',
            'skincare_sales', 'skincare_units', 'previous_yr_skincare_sales',
            'make_up_sales', 'make_up_units', 'fragrance_sales', 'fragrance_units',
            'gift_sets_sales', 'gift_sets_units', 'suncare_sales', 'suncare_units',
            'other_sales', 'other_units', 'accessories_sales', 'accessories_units',
            'clarins_sales', 'sisley_sales', 'lancome_sales', 'qiriness_sales',
            'lauder_sales', 'chanel_sales', 'guerlain_sales', 'ioma_sales',
            'filorga_sales', 'shiseido_sales', 'sales_change_12_months',
            'skincare_sales_change_12_months', 'gender_name_F', 'gender_name_M',
            'gender_name_Unspecified', 'rfm_segment', 'age_band']

        scale_df = df.copy()
        scale_df[columns_to_scale] = scaler.fit_transform(scale_df[columns_to_scale])	

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv',
                              scale_df)



class TrainModel:

    def __init__(self, MonthParams):

        self.MonthParams = MonthParams
        self.df = blob.download_dataframe_from_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv')

    
    def split_data(self) -> None:

        """Split data into train and test sets."""

        y = self.df.pop('high_skincare_flag')
        X = self.df

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    
    def upsample(self) -> None:
        
        """Use SMOTE to upsample training sets to balance the low and high members.
        Save figure that checks if split is equal."""

        su = SMOTE(random_state=42)
        self.X_train_su, self.y_train_su = su.fit_resample(self.X_train, self.y_train)

        high_member_count = self.y_train_su.value_counts()[1]
        low_member_count = self.y_train_su.value_counts()[0]
        total_members = high_member_count + low_member_count

        x_label = (f"Member Count (%) of {format(total_members, '0,')} total members")
        weight_counts = {
            "High Skincare Members": np.array([high_member_count * 100/total_members]),
            "Low Skincare Members": np.array([low_member_count * 100/total_members]),
        }

        fig, ax = plt.subplots(figsize=(5,5))
        bottom = np.zeros(1)

        for boolean, weight_count in weight_counts.items():
            p = ax.bar(x_label, weight_count, label=boolean, bottom=bottom)
            bottom += weight_count

        ax.legend(loc="upper right")
        ax.text(0,6, str(round((high_member_count * 100/total_members), 0)) + '%', ha='center', color='white', size=15, fontweight='bold')
        ax.text(0,55, str(round((low_member_count * 100/total_members), 0)) + '%', ha='center', color='white', size=15, fontweight='bold')
        plt.rc('font', size = 12)
        plt.rc('xtick', labelsize = 12)
        plt.rc('ytick', labelsize = 12)
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_upsampled_member_split')

    
    def train_model(self) -> None:

        """Train and save Logistic Regression Model and the model predictions."""

        model = LogisticRegression(max_iter=200)

        model.fit(X=self.X_train_su, y=self.y_train_su)

        pickle.dump(model, open(f'models/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_model.pkl','wb'))

        y_prob = model.predict(X=self.X_test)
        self.y_pred = np.round(y_prob)

        # save model coefficients to plot later
        self.model_coefficients = model.coef_


    def visualise_model_coefficients(self) -> None:

        """Save a representation of the model coefficients. Hard to understand what they mean in the real world,
        but gives an indication as to which coefficients are important. Further explanation in README."""

        coefficients_df = pd.DataFrame({'Feature': self.X_train_su.columns, 'Coefficient': np.exp(self.model_coefficients[0])})
        coefficients_df['Coefficient magnitude'] = coefficients_df['Coefficient'].abs()
        top_10 = coefficients_df.sort_values(by='Coefficient magnitude', ascending=False)[:25]

        fig, ax = plt.subplots(1, 1, figsize=[6, 7])
        sns.barplot(x=top_10['Coefficient magnitude'], y=top_10['Feature'])
        ax.set_title('Top 15 most important features')
        ax.set_xlabel('Average change in odds when scaled feature increases by one unit', size=10)
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_model_coefficients')


    def visualise_confusion_matrix(self) -> None:

        """Save the confusion matrix, and log the other model scores."""

        # Accuracy, precision & recall 
        accuracy = accuracy_score(self.y_test, self.y_pred)
        logger.info('Accuracy = {:.2f}\n'.format(accuracy))
        logger.info('Classification report:\n')
        logger.info(classification_report(self.y_test, self.y_pred))

        # Visualise the confusion matrix, normalised for classification frequency
        conf_matrix = confusion_matrix(self.y_test, self.y_pred)
        row_sums = conf_matrix.sum(axis=1, keepdims=True)
        norm_conf_matrix = conf_matrix / row_sums

        fig, ax = plt.subplots(1, 1, figsize=[7,5])
        conf_plot = ax.matshow(norm_conf_matrix, cmap=plt.cm.gray)
        ax.set_xlabel('Predicted class')
        ax.set_ylabel('Actual class')
        ax.set_title('Confusion matrix')
        plt.colorbar(ax=ax, mappable=conf_plot)

        # Add actual counts to plot
        for (i, j), z in np.ndenumerate(conf_matrix):
            ax.text(j, i, '{:0.0f}'.format(z), ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))

        plt.tight_layout()
        plt.savefig(f'logs/visualisations/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_confusion_matrix')