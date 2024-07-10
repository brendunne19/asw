from conf.core import config as conf
import src.utils as utils
import src.dataset.dataset as data
import src.models.train as train_proc

from loguru import logger
logger.add('logs/training_file_{time}.log')

@logger.catch
def run_predict():

    logger.info(conf)

    MonthParams = utils.MonthParams(conf.specified_start_month, conf.specified_end_month)

        
    # getting data
    dataset = data.GenerateDataset(MonthParams)
    logger.info('run data sql proc')
    dataset.run_sql_proc(MonthParams)
    logger.info('get data')
    df = dataset.get_training_data(MonthParams)
    logger.info('data loading complete\n')

    # cleaning data
    logger.info('begin cleaning data')
    clean = train_proc.CleanData(MonthParams)
    logger.info('check member split and save graph')
    clean.check_member_split(df)
    logger.info('add extra features')
    df = clean.add_more_features(df)
    logger.info('check null columns, and replace with zeroes')
    df = clean.check_nulls_and_replace(df)
    logger.info('store metadata')
    clean.store_metadata(df)
    logger.info('remove skew')
    df = clean.remove_skew(df)
    logger.info('drop erroneous date members')
    df, metadata_df = clean.drop_erroneous_date_members(df)
    logger.info('drop weird enrol date members')
    df = clean.drop_weird_enrol_date_members(df, metadata_df)
    logger.info('convert dates to days')
    df = clean.convert_dates_to_days(df)
    logger.info('creating flag features')
    df = clean.creating_flag_features(df) 
    logger.info('scale data')
    df = clean.scale_data(df) 
    logger.info('data cleansing complete\n') 

    # training model 
    logger.info('load in scaled data')
    train = train_proc.TrainModel(MonthParams)
    logger.info('split data')
    train.split_data()
    logger.info('upsample data with SMOTE')
    train.upsample()
    logger.info('train model')
    train.train_model()
    logger.info('visualise coefficients')
    train.visualise_model_coefficients()
    logger.info('visualise confusion matrix')
    train.visualise_confusion_matrix()
    logger.info('training complete')


if __name__ == "__main__":


    run_predict()