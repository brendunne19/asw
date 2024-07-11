# global imports
from loguru import logger

# local files
import src.models.predict_model as proc
import src.visualisation.visualise_profiles as visual_proc
import src.output.output_results as out
from conf.core import config as conf
from src.utils import *


@logger.catch
def predict_model() -> None:

    """Run monthly prediction process and generate profiles."""
    
    logger.add("logs/file_{time}.log")
    logger.info("run_predict_model.py initialised")
    logger.info(conf)

    # Set the start date based on whether we want to start from the current
    # month or from a specific month. Configured in the YAML file.
    if conf.current_month_flag == 1 and conf.run_type == 'MONTHLY':
        specified_month_idnt = int(orae.get_current_fiscal_mth())
        specified_month_name = get_mth_name(str(specified_month_idnt)) 
    
    elif conf.current_month_flag == 0 and conf.run_type == 'ONE-OFF':
        specified_month_idnt = conf.specified_month_idnt
        specified_month_name = conf.specified_month_name
    else:
        logger.info('ERROR: Run_type and current_month_flag config parameters are not aligned.\nPlease check these and try again. The Read-me file contains options for use.')
        return

    # selecting which model to use
    if conf.current_month_model_flag == 1:
        model_month_label = str(specified_month_name) + str(specified_month_idnt)[2:4]
    elif conf.current_month_model_flag == 0:
        model_month_label = conf.model_month_label
    else:
        logger.info('Error: current_month_model_flag incorrrectly set.')
        return

    logger.info("Starting for fiscal month: " + str(specified_month_idnt))

    # initialise the monthly parameters class
    MonthParams = proc.MonthParams(
        month_idnt = specified_month_idnt,
        month_name = specified_month_name,
        model_month_label = model_month_label     
    )
    
    
    # create data tables
    logger.info('Create data tables in ADM')
    proc.run_script('mrd_oo_mem_d', MonthParams)
    proc.run_script('lseg_mem_f', MonthParams)
    proc.run_script('lseg_prof_f', MonthParams)


    # run segmentation process
    logger.info('Fetch data tables from ADM')
    seg_proc = proc.ClassificationProcess(MonthParams)
    logger.info('build training features')
    seg_proc.build_features(MonthParams)
    logger.info('prep data for classification')
    seg_proc.prep_data_for_prediction(MonthParams)
    logger.info('predict on data')
    seg_proc.model_predict_and_upload(MonthParams)
    logger.info('completed Segmentation training')

    
    # visualise profiles
    logger.info('Initiate Visualise Profile')
    seg_vis = visual_proc.VisualiseProfile(MonthParams)
    logger.info('Aggregate profile data')
    seg_vis.aggregate_profile_data(MonthParams)
    logger.info('Combine raw datasets')
    seg_vis.combine_raw_datasets(MonthParams)
    logger.info('Calculate metrics')
    seg_vis.df_bu_f = seg_vis.calculate_metrics(MonthParams, group_list = ['bu_code'])
    logger.info(f'BU-level metrics: {seg_vis.df_bu_f}')
    seg_vis.df_clust_f = seg_vis.calculate_metrics(MonthParams)
    logger.info(f'Cluster-level metrics: {seg_vis.df_clust_f}')
    logger.info('\nCalculate column indexes')
    seg_vis.calculate_column_indexes(MonthParams)
    logger.info('Pivot cluster absolutes')
    seg_vis.pivot_cluster_indexes(MonthParams)
    logger.info('pivot and format abs and pivot cluster absolutes')
    seg_vis.pivot_and_format_abs(MonthParams)
    logger.info('Save heatmap')
    seg_vis.plot_heatmap(MonthParams)


    # output results to adm
    out_proc = out.OutputResults(MonthParams)
    logger.info('create output table')
    out_proc.create_output_table(MonthParams)
    logger.info('export output results')
    out_proc.export_output_table(MonthParams)
    logger.info('create siebel table')
    out_proc.create_siebel_table(MonthParams)
    logger.info('fill siebel table')
    out_proc.fill_siebel_table(MonthParams)
    
    logger.info("Job completed")


if __name__ == "__main__":


    predict_model()
