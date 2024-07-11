# proprietary imports
import my_oracle as ora
import my_blob as blob

# global imports
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
from datetime import timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from loguru import logger

class VisualiseProfile:

    """Class for visualising results from prediction with member profiles."""

    def __init__(self, MonthParams) -> None:
        
        logger.info('-----------------------------------------')
        logger.info('VISUALISE PROFILE INITIATED')
        logger.info('-----------------------------------------')

        self.MonthParams = MonthParams

        logger.info('Collecting profile data')

        self.df = ora.get_oracle_data('CRMBMAP', f"SELECT * FROM {MonthParams.bu_code}_LSEG_PROF_F_{MonthParams.month_label}")

        # Upload raw profile data
        blob.upload_dataframe_to_blob(f'lifestyle-model/data/raw/{MonthParams.bu_code}/{MonthParams.bu_code}_lseg_prof_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv', 
                              f'data/raw/{MonthParams.bu_code}_lseg_prof_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                             self.df)
        
        # download prediction data for members
        self.df_preds = blob.download_dataframe_from_blob(f'lifestyle-model/data/processed/{MonthParams.bu_code}/{MonthParams.bu_code}_lseg_pred_d_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                       f'data/processed/{MonthParams.bu_code}_lseg_pred_d_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv')
        
        # Check total counts
        df_t = self.df_preds.groupby(['pred']).nunique().reset_index()
        total = self.df_preds.contact_key.nunique()
        df_t['pct'] = df_t['contact_key'] / total
        
        logger.info(f'Number of unique contact keys: {total}\nLength of prediction table: {len(self.df_preds)} (Should be the same as above)')
        logger.info(f'Total Counts per Segment:\n{df_t}')

        # start calculating profile
        self.df_seg = self.df_preds.copy().rename(columns = {'pred': 'seg_num'})

    
    def aggregate_profile_data(self, MonthParams) -> None:

        df = self.df.copy()
        df_preds = self.df_seg[['contact_key']]

        # Restrict members for efficiency
        df = pd.merge(df_preds[['contact_key']], df, on = ['contact_key'], how = 'inner')

        # Create brand type columns
        df['a_brand_sales'] = np.where(df['brand_type_name'] == 'A Brand', df['tot_sales'], 0)
        df['excl_brand_sales'] = np.where(df['brand_type_name'] == 'Exclusive Brand', df['tot_sales'], 0)
        df['pl_brand_sales'] = np.where(df['brand_type_name'] == 'Private Label', df['tot_sales'], 0)
        
        # Create online or offline columns
        df['offline_sales'] = np.where(df['web_store_flag'] == 0, df['tot_sales'], 0)
        df['online_sales'] = np.where(df['web_store_flag'] == 1, df['tot_sales'], 0)

        # Create category columns
        df['accessories_sales'] = np.where(df['product_hier_2_l3_name'] == 'ACCESSORIES', df['tot_sales'], 0)
        df['fragrances_women_sales'] = np.where(df['product_hier_2_l3_name'] == 'FRAGRANCES WOMEN', df['tot_sales'], 0)
        df['fragrances_men_sales'] = np.where(df['product_hier_2_l3_name'] == 'FRAGRANCES MEN', df['tot_sales'], 0)
        df['fragrances_children_sales'] = np.where(df['product_hier_2_l3_name'] == 'FRAGRANCES CHILDREN', df['tot_sales'], 0)
        df['fragrances_unisex_sales'] = np.where(df['product_hier_2_l3_name'] == 'FRAGRANCES UNISEX', df['tot_sales'], 0)
        df['gift_sets_selective_sales'] = np.where(df['product_hier_2_l3_name'] == 'GIFT SETS SELECTIVE', df['tot_sales'], 0)
        df['make_up_eyes_sales'] = np.where(df['product_hier_2_l3_name'] == 'MAKE-UP EYES', df['tot_sales'], 0)
        df['make_up_face_sales'] = np.where(df['product_hier_2_l3_name'] == 'MAKE-UP FACE', df['tot_sales'], 0)
        df['make_up_lips_sales'] = np.where(df['product_hier_2_l3_name'] == 'MAKE-UP LIPS', df['tot_sales'], 0)
        df['make_up_nails_sales'] = np.where(df['product_hier_2_l3_name'] == 'MAKE-UP NAILS', df['tot_sales'], 0)
        df['make_up_others_sales'] = np.where(df['product_hier_2_l3_name'] == 'MAKE-UP OTHERS', df['tot_sales'], 0)
        df['other_sales'] = np.where(df['product_hier_2_l3_name'] == 'OTHER', df['tot_sales'], 0)
        df['parapharmacy_sales'] = np.where(df['product_hier_2_l3_name'] == 'PARAPHARMACY', df['tot_sales'], 0)
        df['skincare_women_sales'] = np.where(df['product_hier_2_l3_name'] == 'SKINCARE WOMEN', df['tot_sales'], 0)
        df['skincare_men_sales'] = np.where(df['product_hier_2_l3_name'] == 'SKINCARE MEN', df['tot_sales'], 0)
        df['skincare_children_sales'] = np.where(df['product_hier_2_l3_name'] == 'SKINCARE CHILDREN', df['tot_sales'], 0)
        df['skincare_unisex_sales'] = np.where(df['product_hier_2_l3_name'] == 'SKINCARE UNISEX', df['tot_sales'], 0)
        df['suncare_selective_sales'] = np.where(df['product_hier_2_l3_name'] == 'SUNCARE SELECTIVE', df['tot_sales'], 0)

        # Aggregate to member level
        df = df.groupby(['contact_key']).agg({
            'tot_sales': 'sum',
            'tot_items': 'sum',
            'tot_discount': 'sum',
            'order_num': 'nunique',
            'birth_dt': 'min',
            'gender_name': 'min',
            'seg_num': 'min',
            'a_brand_sales': 'sum',
            'excl_brand_sales': 'sum',
            'pl_brand_sales': 'sum',
            'offline_sales': 'sum',
            'online_sales': 'sum',
            'accessories_sales': 'sum',
            'fragrances_women_sales': 'sum',
            'fragrances_men_sales': 'sum',
            'fragrances_children_sales': 'sum',
            'fragrances_unisex_sales': 'sum',
            'gift_sets_selective_sales': 'sum',
            'make_up_eyes_sales': 'sum',
            'make_up_face_sales': 'sum',
            'make_up_lips_sales': 'sum',
            'make_up_nails_sales': 'sum',
            'make_up_others_sales': 'sum',
            'other_sales': 'sum',
            'parapharmacy_sales': 'sum',
            'skincare_women_sales': 'sum',
            'skincare_men_sales': 'sum',
            'skincare_children_sales': 'sum',
            'skincare_unisex_sales': 'sum',
            'suncare_selective_sales': 'sum'
        }).reset_index()

        # remove any members with unrealistic birth_dt
        df = df[df['birth_dt'] < pd.to_datetime(MonthParams.age_max_date)] 
        df = df[df['birth_dt'] > pd.to_datetime('01-JAN-1900')]

        # Calculate age
        df['age'] = (pd.to_datetime(MonthParams.age_max_date) - pd.to_datetime(df['birth_dt'])) / timedelta(days=365)
        df['16_to_20_yrs'] = np.where(df['age'] < 21, 1, 0)
        df['21_to_25_yrs'] = np.where((df['age'] >= 21) & (df['age'] < 26), 1, 0)
        df['26_to_35_yrs'] = np.where((df['age'] >= 26) & (df['age'] < 36), 1, 0)
        df['36_to_45_yrs'] = np.where((df['age'] >= 36) & (df['age'] < 46), 1, 0)
        df['46_to_55_yrs'] = np.where((df['age'] >= 46) & (df['age'] < 56), 1, 0)
        df['56_to_66_yrs'] = np.where((df['age'] >= 56) & (df['age'] < 66), 1, 0)
        df['66+_yrs'] = np.where(df['age'] >= 66, 1, 0)

        # Split out gender
        df['female'] = np.where(df['gender_name'] == 'F', 1, 0)
        df['male'] = np.where(df['gender_name'] == 'M', 1, 0)
        df['unspecified'] = np.where(df['gender_name'] == 'Unspecified', 1, 0)

        # Split out rfm
        df['vip'] = np.where(df['seg_num'] == 'VIP', 1, 0)
        df['loyal'] = np.where(df['seg_num'] == 'LOYAL', 1, 0)
        df['regular'] = np.where(df['seg_num'] == 'REGULAR', 1, 0)
        df['one_offs'] = np.where(df['seg_num'] == 'ONE-OFFS', 1, 0)
        df['new'] = np.where(df['seg_num'] == 'NEW', 1, 0)
        df['lapsed'] = np.where(df['seg_num'] == 'LAPSED', 1, 0)
        df['inactive'] = np.where(df['seg_num'] == 'INACTIVE', 1, 0)
        df['gone_away'] = np.where(df['seg_num'] == 'GONE AWAY', 1, 0)

        self.df_prof_f = df

        blob.upload_dataframe_to_blob(f'lifestyle-model/data/interim/{MonthParams.bu_code}/{MonthParams.bu_code}_df_prof_f_{MonthParams.month_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      f'data/interim/{MonthParams.bu_code}_df_prof_f_{MonthParams.month_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      df)

    
    def combine_raw_datasets(self, MonthParams) -> None:

        """Create a master dataset to use."""

        df_abs_f = self.df_seg[['contact_key', 'seg_num']].copy()
        df_abs_f.rename(columns = {'seg_num': 'cluster'}, inplace = True)
        df_abs_f = pd.merge(df_abs_f, self.df_prof_f, on = ['contact_key'], how = 'inner')
        df_abs_f.rename(columns = {'order_num': 'tot_trxs'}, inplace = True)
        # Add bu column so we can aggregate to bu total as well
        df_abs_f['bu_code'] = MonthParams.bu_code

        self.df_abs_f = df_abs_f

        blob.upload_dataframe_to_blob(f'lifestyle-model/data/interim/{MonthParams.bu_code}/{MonthParams.bu_code}_df_abs_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      f'data/interim/{MonthParams.bu_code}_df_abs_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      df_abs_f)

    
    def calculate_metrics(self, MonthParams, group_list = ['bu_code', 'cluster']) -> pd.DataFrame:

        """Summarise to a specified level (default is cluster as used later on) some key metrics. 
        Returns the df to be logged as can be used for checking."""

        df = self.df_abs_f.copy()
        df['members'] = 1

        ## Define O+O features at member level before aggregation
        # O+O: offline_sales & online_sales both > 0
        # Pure Offline: offline_sales > 0 and online_sales = 0
        # Pure Online: offline_sales = 0 and online_sales > 0
        df['o+o_sales'] = np.where((df['offline_sales'] > 0) & (df['online_sales'] > 0), df['tot_sales'], 0)
        df['pure_offline_sales'] = np.where((df['offline_sales'] > 0) & (df['online_sales'] == 0), df['tot_sales'], 0)
        df['pure_online_sales'] = np.where((df['offline_sales'] == 0) & (df['online_sales'] > 0), df['tot_sales'], 0)

        col_list = list(df.columns)
        for col in ['contact_key', 'cluster', 'bu_code', 'offline_sales', 'online_sales', 'birth_dt']:
            col_list.remove(col)
        df = df.groupby(group_list)[col_list].sum().reset_index()

        ## Main KPIs
        df['acv'] = df['tot_sales'] / df['members']
        df['atv'] = df['tot_sales'] / df['tot_trxs']
        df['atf'] = df['tot_trxs'] / df['members']
        df['ipt'] = df['tot_items'] / df['tot_trxs']
        df['ppu'] = df['tot_sales'] / df['tot_items']
        df['pct_discount'] = df['tot_discount'] / df['tot_sales']

        main_kpi_cols = ['tot_sales', 'members', 'acv', 'atv', 'atf', 'ipt', 'ppu', 'pct_discount']

        ## Age
        age_cols = ['16_to_20_yrs', '21_to_25_yrs', '26_to_35_yrs', '36_to_45_yrs', '46_to_55_yrs', '56_to_66_yrs', '66+_yrs']
        df['abs_age_members'] = df[age_cols].sum(axis=1)
        for i in age_cols:
            df[i+'_share'] = df[i] / df['abs_age_members']
        age_cols = [i+'_share' for i in age_cols]  # update col names

        ## RFM
        rfm_cols = ['vip', 'loyal', 'regular', 'one_offs', 'new', 'lapsed', 'inactive', 'gone_away']
        df['abs_rfm_members'] = df[rfm_cols].sum(axis=1)
        for i in rfm_cols:
            df[i+'_share'] = df[i] / df['abs_rfm_members']
        rfm_cols = [i+'_share' for i in rfm_cols]  # update col names

        ## Gender
        gender_cols = ['female', 'male', 'unspecified']
        df['abs_gender_members'] = df[gender_cols].sum(axis=1)
        for i in gender_cols:
            df[i+'_share'] = df[i] / df['abs_gender_members']
        gender_cols = [i+'_share' for i in gender_cols]  # update col names

        ## Category sales share
        cat_cols = ['accessories_sales', 'fragrances_women_sales', 'fragrances_men_sales', 'fragrances_children_sales', 'fragrances_unisex_sales',
                        'gift_sets_selective_sales', 'make_up_eyes_sales', 
                        'make_up_face_sales', 'make_up_lips_sales', 'make_up_nails_sales', 'make_up_others_sales', 
                        'other_sales', 'parapharmacy_sales',
                        'skincare_women_sales', 'skincare_men_sales', 'skincare_children_sales', 'skincare_unisex_sales', 'suncare_selective_sales']

        df['abs_cat_sales'] = df[cat_cols].sum(axis=1)
        for i in cat_cols:
            df[i+'_share'] = df[i] / df['abs_cat_sales']
        cat_cols = [i+'_share' for i in cat_cols]  # update col names

        ## Brand type share
        brand_type_cols = ['a_brand_sales', 'excl_brand_sales', 'pl_brand_sales']
        for i in brand_type_cols:
            df[i+'_share'] = df[i] / df['tot_sales']
        brand_type_cols = [i+'_share' for i in brand_type_cols]  # update col names

        ## O+O share
        opo_cols = ['o+o_sales', 'pure_offline_sales', 'pure_online_sales']
        for i in opo_cols:
            df[i+'_share'] = df[i] / df['tot_sales']
        opo_cols = [i+'_share' for i in opo_cols]  # update col names


        ## Collate final col list, dropping any unneeded ones
        final_cols = group_list + main_kpi_cols + age_cols + rfm_cols + gender_cols + cat_cols + brand_type_cols + opo_cols

        df = df[final_cols]

        return df
    
    
    def calculate_column_indexes(self, MonthParams) -> None:

        """List the columns to calculate indexes on."""

        columns_to_index = list(self.df_clust_f.columns)
        for col in ['bu_code', 'cluster', 'tot_sales', 'members', 'a_brand_sales_share', 'excl_brand_sales_share', 'inactive_share', 
                    'gone_away_share', 'parapharmacy_sales_share', 'skincare_unisex_sales_share']:
            columns_to_index.remove(col)

        self.columns_to_index = columns_to_index

        logger.info(f'Columns to index: {columns_to_index}')

    
    def pivot_cluster_indexes(self, MonthParams):

        """Description."""

        # define objects to use 
        df_clust_f = self.df_clust_f
        df_bu_f = self.df_bu_f
        self.df_clust_d = self.df_abs_f[['contact_key', 'cluster']].copy()
        df_clust_d = self.df_clust_d.copy()     
        features = self.columns_to_index

        df_idx_f = df_clust_f.merge(df_bu_f.rename(columns = dict(zip(df_bu_f.columns[1:], df_bu_f.columns[1:]+"_bu")))
            , on = ['bu_code'], how = 'left'
        )

        for feature in features:
            df_idx_f[feature+'_index'] = (df_idx_f[feature] / df_idx_f[feature+'_bu']) * 100

        df_idx_piv_f = df_idx_f[['cluster'] + [i+'_index' for i in features]].set_index('cluster').transpose()

        my_list = map(str, df_idx_piv_f.columns)
        num_members = df_clust_d['cluster'].value_counts().sort_index().values
        share_members = [str("{0:.0%}".format(i)) for i in num_members/sum(num_members)]

        my_list = ['Seg: '+ s + ' |' for s in my_list]
        new_columns = []
        for pos, count, share in zip(list(df_clust_f['cluster'].unique()-1), num_members, share_members):
            new_columns.append(my_list[pos] + ' Members: '+str(count)+" ("+share+")")

        df_idx_piv_f.columns = new_columns

        self.df_idx_piv_f = df_idx_piv_f

        blob.upload_dataframe_to_blob(f'lifestyle-model/data/processed/{MonthParams.bu_code}/{MonthParams.bu_code}_df_idx_piv_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      f'data/processed/{MonthParams.bu_code}_df_idx_piv_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      df_idx_piv_f)

    
    def pivot_and_format_abs(self, MonthParams):

        df = self.df_clust_f
        df_clust_d = self.df_clust_d.copy()     
        features = self.columns_to_index

        df[features] = df[features].apply(lambda x: round(x, 2)).astype(str)

        for feature in features:
            df[feature+'_abs'] = df[feature]
        
        df_abs_piv_f = df[['cluster'] + [i + '_abs' for i in features]].set_index('cluster').transpose()

        my_list = map(str, df_abs_piv_f.columns)
        num_members = df_clust_d['cluster'].value_counts().sort_index().values
        share_members = [str("{0:.0%}".format(i)) for i in num_members/sum(num_members)]

        my_list = ['Seg: '+ s + ' |' for s in my_list]
        new_columns = []
        for pos, count, share in zip(list(np.sort(df_clust_d['cluster'].unique()-1, axis=0)), num_members, share_members):
            new_columns.append(my_list[pos] + ' Members: '+str(count)+" ("+share + ")")
        
        df_abs_piv_f.columns = new_columns

        self.df_abs_piv_f = df_abs_piv_f

        blob.upload_dataframe_to_blob(f'lifestyle-model/data/processed/{MonthParams.bu_code}/{MonthParams.bu_code}_df_abs_piv_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      f'data/processed/{MonthParams.bu_code}_df_abs_piv_f_{MonthParams.month_label}_{MonthParams.model_label}_trained_on_{MonthParams.model_month_label}_for_{MonthParams.period_length}_months.csv',
                                      df_abs_piv_f)

    
    def plot_heatmap(self, MonthParams, index_flag = True):

        if index_flag == True:
            df = self.df_idx_piv_f.copy()
            df.fillna(value=-1, inplace=True)
            # Optional: add nice name dict for feature names here

            fig, ax = plt.subplots(1, 1, figsize=[20, 15])
            cmap = sns.diverging_palette(10, 133, as_cmap=True)
            g = sns.heatmap(data=df[df.columns].astype(int), square=False, cmap=cmap, center=100, vmax=130, vmin=70,
                linewidths=.8, cbar=True, ax=ax, annot=True, fmt='.0f', xticklabels=True, yticklabels=True)
            ax.set_ylabel('metric')
            ax.set_xticklabels(g.get_xticklabels(), rotation=30)
            plt.savefig(f'src/visualisation/profiling-outputs/heatmap-{MonthParams.bu_code}-{MonthParams.month_label}-{MonthParams.model_label}-{MonthParams.period_length}-month.jpg')
        
        elif index_flag == False:
            df = self.df_idx_piv_f.copy()
            df.reset_index(inplace=True)
            metrics = df['index'].values.copy()
            # Optional: add nice name dict for feature names here
            df.set_index('index', inplace=True)

            df_abs = self.df_abs_piv_f.copy()
            df_abs.reset_index(inplace=True)
            df_abs['index'] = df_abs['index'].str.replace("_abs", "_index")
            df_abs = df_abs[df_abs['index'].isin(metrics)]        

            fig, ax = plt.subplots(1, 1, figsize=[20, 15])
            cmap = sns.diverging_palette(10, 133, as_cmap=True)
            g = sns.heatmap(data=df[df.columns].astype(int), square=False, cmap=cmap, center=100, vmax=130, vmin=70,
                linewidths=.8, cbar=True, ax=ax, annot=df_abs, fmt = '', xticklabels=True, yticklabels=True)
            ax.set_yabel('metric')
            ax.set_xticklabels(g.get_xticklabels(), rotation=30)
            plt.savefig(f'src/visualisation/profiling-outputs/heatmap-{MonthParams.bu_code}-{MonthParams.month_label}-{MonthParams.model_label}-{MonthParams.period_length}-month.jpg')
