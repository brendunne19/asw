# other files
import src.utils as utils

# proprietary packages
import my_blob as blob

# global packages
import numpy as np
import pickle


class Predict:

    def __init__(self, MonthParams):

        self.MonthParams = MonthParams
        self.df = blob.download_dataframe_from_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_scaled_df.csv')
        self.metadata_df = blob.download_dataframe_from_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_metadata_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_cleaned_metadata_df.csv')
    

    def predict(self) -> None:

        """Load pre-trained model and predict."""

        with open(f'models/{self.MonthParams.model_label}.pkl','rb') as buff:
            model = pickle.load(buff)

        # Make a prediction on the test dataset
        y_prob = model.predict(X=self.df)
        y_pred = np.round(y_prob)

        self.metadata_df['high_skincare_flag'] = y_pred

        blob.upload_dataframe_to_blob(f'high-skincare-model/data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_model_predictions_df.csv', 
                              f'data/processed/{self.MonthParams.month_start}_to_{self.MonthParams.month_end}_model_predictions_df.csv',
                              self.metadata_df[['contact_key', 'high_skincare_flag']])