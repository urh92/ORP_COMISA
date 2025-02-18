import os
import numpy as np
import pandas as pd
from base.base_regression import BaseRegressor
from helper_functions import Helper
from config import ConfigLoader
from dataset import MorpheusDataset
from sklearn.linear_model import LogisticRegression
from scipy.stats import randint, uniform
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None


class MorpheusRegressor(BaseRegressor):
    def __init__(self, dataframe, y_label, predictors=None, co_variates=[], model_type='LogisticRegression',
                 y_dict=None, output_folder=None, drop_corr_cols=False, variable_type='All', drop_score_cols=False):
        super().__init__(dataframe, y_label, predictors, co_variates, model_type, y_dict, output_folder, drop_corr_cols, variable_type)
        self.drop_score_cols = drop_score_cols
        self.score_cols = self.get_score_columns()
        self.predictors = [p for p in self.predictors if p not in (*self.y_label, *self.co_variates, *self.remove_cols, *self.score_cols)]
        self.h = Helper()

    def get_score_columns(self):
        if self.drop_score_cols:
            score_names = [col for col in self.var_df.columns if col.endswith('Score')]
            filtered_df = self.var_df[self.var_df[score_names].eq(1).any(axis=1)]
            score_columns = filtered_df['Columns'].tolist()
        else:
            score_columns = []
        return score_columns

    def prepare_data(self, predictors):
        df = self.dataframe.copy()
        if self.model_type in ['LogisticRegression', 'MultinominalRegression']:
            df[self.y_label] = df[self.y_label].replace(self.y_dict)
        elif self.model_type == 'LinearRegression':
            df = self.h.clean_data(df, self.y_label, self.log_cols)
        if isinstance(predictors, list):
            for col in predictors:
                df = self.h.clean_data(df, col, self.log_cols)
        else:
            df = self.h.clean_data(df, predictors, self.log_cols)
        if self.co_variates:
            for co_var in self.co_variates:
                df = self.h.clean_data(df, co_var, self.log_cols)
        return df

    def get_summary_stats(self, df, col):
        n0, n1, mean0, std0, mean1, std1 = super().get_summary_stats(df, col)
        if self.model_type == 'LogisticRegression' and self.stats[col] == 'Mean':
            df0, df1 = df[df[self.y_label] == 0], df[df[self.y_label] == 1]
            if col.startswith('Midpoint'):
                mean0, std0 = self.h.calc_midpoint_mean(dataframe=df0, column=col + '_Original')
                mean1, std1 = self.h.calc_midpoint_mean(dataframe=df1, column=col + '_Original')
            else:
                mean0, mean1 = df0[col].mean(), df1[col].mean()
                std0, std1 = df0[col].std(), df1[col].std()
        elif self.model_type == 'LinearRegression' and self.stats[col] == 'Mean':
            if col.startswith('Midpoint'):
                mean0, std0 = self.h.calc_midpoint_mean(dataframe=df, column=col + '_Original')
        return n0, n1, mean0, std0, mean1, std1


if __name__ == '__main__':
    n_comparisons = 87
    config = ConfigLoader('config.json')
    dataset = MorpheusDataset(
        excel_path=os.path.join('C:/Code/projects/somno/cerebra', 'Data', 'Cerebra_Dataset_All5.csv'))
    data = dataset.data
    y_dict = {'Control': 0, 'Insomnia': 1, 'OSA': 2, 'COMISA': 3}
    predictors = ['TIB', 'TST', 'SOL', 'WASO', 'SE', 'Percentage_Stage1_2', 'Percentage_SWS', 'Percentage_REM',
                  'Latency_Stage2', 'Latency_SWS', 'Latency_REM', 'sleep', 'wake', 'nrem', 'rem', 'min_orp2',
                  'sleep_recovery', 'peak_arousal_orp1_x', 'peak_arousal_orp2_x', 'X000_025', 'X025_050', 'X050_075',
                  'X075_100', 'X100_125', 'X125_150', 'X150_175', 'X175_200', 'X200_225', 'X225_250']
    self = MorpheusRegressor(dataframe=data, y_label='Group2', predictors=predictors,
                             co_variates=['Gender', 'Age', 'BMI'],
                             model_type='MultinominalRegression', y_dict=y_dict, drop_score_cols=False,
                             variable_type='Objective')
    self.fit_models(n_comparisons=n_comparisons)
    for group in self.y_dict.keys():
        self.save_formatted_excel(group=group)
    self.h.collect_spreadsheets(y_labels=list(self.y_dict.keys()), y_head=self.y_label, model=self.model_type,
                                runs=[3, 3, 3, 3, 3, 3], mode='Objective')

    # import os
    # import numpy as np
    # import pandas as pd
    # from base.base_regression import BaseRegressor
    # from helper_functions import Helper
    # from config import ConfigLoader
    # from dataset import MorpheusDataset
    # from regression import MorpheusRegressor
    # from sklearn.linear_model import LogisticRegression
    # import warnings
    #
    # warnings.filterwarnings("ignore", category=FutureWarning)
    # pd.options.mode.chained_assignment = None
    #
    # config = ConfigLoader('config.json')
    # dataset = MorpheusDataset(excel_path=os.path.join('C:/Code/projects/somno/cerebra', 'Data', 'Cerebra_Dataset_All4.csv'))
    # h = Helper()
    # y_dict = {'Normal': np.nan, 'OSA_Mild': 1, 'Insomnia': 0, 'COMISA_Mild': 2, 'OSA_Severe': 1, 'COMISA_Severe': 2}
    # predictors = ['Age', 'BMI', 'PH2_Depression', 'PH2_Memory_Loss', 'PH3_Sleep_Hours', 'ESS', 'Muscoskeletal_Pain_Score',
    #               'PH3_Before_Bed_Sleep_Aids', 'PH2_Head_Ache', 'PH2_Asthma', 'PH2_Allergy', 'MH_High_Blood_Pressure',
    #               'MH_Tobacco_Habit', 'PH2_Arthritis', 'PH2_Anemia', 'MH_Caffeinated_Beverage', 'MH_Diabetes',
    #               'MH_Alcohol', 'PH2_Shiftworker', 'MH_Cancer', 'MH_Thyroid_Disease', 'PH2_Stroke_History', 'MH_Hist_Lung_Disease',
    #               'MH_Heart_Attack', 'MH_Stomach_Disease', 'MH_Intestinal_Disease',
    #               'sleep', 'wake', 'nrem', 'peak_arousal_orp1_x', 'peak_arousal_orp1_y', 'min_orp2', 'sleep_recovery',
    #               'X000_025', 'X025_050', 'X050_075', 'X075_100', 'X100_125', 'X125_150', 'X150_175', 'X175_200',
    #               'X200_225', 'X225_250', 'TIB', 'TST', 'SOL', 'WASO', 'SE', 'Percentage_Stage1_2',
    #               'Percentage_SWS', 'Percentage_REM', 'Latency_Stage2', 'Latency_SWS', 'Latency_REM']
    # self = MorpheusRegressor(dataframe=dataset.data, y_label='Group', predictors=predictors,
    #                          model_type='LogisticRegression', y_dict=y_dict, drop_score_cols=False, variable_type='All')
    # model = LogisticRegression(multi_class='multinomial', class_weight='balanced', max_iter=700)
    #
    # self.recursive_feature_elimination(model=model, standardize=True)
    # df_features = pd.read_csv(os.path.join(self.output_folder, 'RFE_Features.csv'))
    # self.predictors = df_features['Variables'].tolist()
    # y_true, y_pred, y_prob = self.evaluate_model_cv(model=model, standardize=True)
    # h.plot_roc_and_confusion(y_true, y_prob, label_order=['Insomnia', 'OSA', 'COMISA'])
