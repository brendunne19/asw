from conf.core import config as conf
import src.utils as utils
import src.dataset.dataset as data
import src.models.train as train_proc
import src.models.predict as predict_proc
import src.output.upload as upload_proc

from loguru import logger
logger.add('logs/file_{time}.log')

@logger.catch
def run_predict():

    logger.info(conf)

    MonthParams = utils.MonthParams(conf.specified_start_month, conf.specified_end_month)

    # getting data
    dataset = data.GenerateDataset(MonthParams)
    logger.info('run data sql proc')
    dataset.run_sql_prediction_proc(MonthParams)
    logger.info('get data')
    df = dataset.get_prediction_data(MonthParams)
    logger.info('data loading complete\n')

    # cleaning data
    logger.info('begin cleaning data')
    clean = train_proc.CleanData(MonthParams)
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

    # predict on data
    logger.info('load processed data')
    predict = predict_proc.Predict(MonthParams)
    logger.info('predict on data')
    predict.predict()
    logger.info('predictions completed\n')

    # upload to ADM
    logger.info('upload results to adm')
    upload = upload_proc.UploadResults()
    logger.info('create output table')
    upload.create_output_table(MonthParams)
    logger.info('upload results')
    upload.export_output_table(MonthParams)
    logger.info('upload complete')


if __name__ == "__main__":


    run_predict()