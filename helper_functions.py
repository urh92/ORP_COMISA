from channel_names_morpheo import *
import numpy as np
import pandas as pd
from base.base_helper import BaseHelper
#import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

anxiety_dict = {'Not at all / None': 0, 'Slight / Few times': 1, 'Moderate / Sometimes': 2, 'Often': 3, 'Severe / Always': 4}
refreshed_dict = {'Not at all / None': 0, 'A little': 1, 'Quite a bit': 2, 'Extremely': 3}
sleep_quality_dict = {'Less rested': -1, 'Same': 0, 'More rested than usual': 1}
awake_feeling_dict = {'Worse': -1, 'Same': 0, 'Better': 1}
race_dict = {'American Indian': 'Native American', 'Pacific Islander': 'Native American',
             'Alaska Native': 'Native American', 'Native Hawaiian': 'Native American'}


class Helper(BaseHelper):
    def clean_data(self, dataframe, column, log_cols):
        if column == 'Gender':
            dataframe[column] = dataframe[column].replace({'Male': 1, 'Female': 0})
        elif column == 'BMI':
            dataframe = dataframe[dataframe[column] <= 80]
        elif column == 'Race':
            dataframe[column] = (dataframe[column] == 'White (Caucasian)').astype(int)
#            dataframe[column] = pd.Categorical(dataframe[column])
        elif column in ['LowSat', 'Minimum_SpO2']:
            dataframe = dataframe[(dataframe[column] >= 60) & (dataframe[column] <= 100)]
        elif column in ['SAO2_Per', 'TST_90', 'TST_80', 'TST_70']:
            dataframe = dataframe[dataframe[column] <= 100]
        elif column == 'TIB':
            dataframe = dataframe[dataframe[column] <= 600]
        elif column == 'WASO':
            dataframe = dataframe[dataframe[column] <= 500]
        elif column == 'Latency_REM':
            dataframe = dataframe[dataframe[column] <= 300]
            dataframe[column] = dataframe[column].abs()
        elif column == 'SEN':
            dataframe = dataframe[dataframe[column] <= 6000]
        elif column in ['Indices_AHI_Total', 'Indices_AHI_NREM', 'Indices_AHI_REM', 'RDI', 'RDI_NREM', 'RDI_REM',
                        'AI_NREM', 'AI_REM', 'Indices_AI_NREM', 'Indices_AI_REM', 'AI_Total', 'AI_Total2',
                        'AI_Spontaneous', 'AI_Respiratory', 'AI_PLMS', 'AI_Micro', 'AI_Awakenings', 'PLMS']:
            dataframe = dataframe[dataframe[column] <= 200]
        elif column in ['Durations_OA_Average_Duration', 'Durations_HI_Average_Duration', 'OA_HYP_Duration']:
            dataframe = dataframe[dataframe[column] >= 10]
        elif column in ['Baseline_SpO2', 'Mean_SpO2']:
            dataframe = dataframe[(dataframe[column] <= 100) & (dataframe[column] >= 80)]
        elif column == 'Mean_SpO2_90':
            dataframe = dataframe[(dataframe[column] <= 90) & (dataframe[column] >= 60)]
        elif column in ['PH3_Sleep_Hours', 'ESS']:
            dataframe = dataframe[dataframe[column] <= 24]
        elif column in ['PH3_Weekday_Nap_Hours', 'PH3_Weekend_Nap_Hours', 'PH3_Wakeup_Nooftimes']:
            dataframe = dataframe[dataframe[column] <= 10]
        elif column in ['PH3_Weekday_Nap_Last_Hours', 'PH3_Weekend_Nap_Last_Hours']:
            dataframe[column] = dataframe[column].replace({15: 0.25, 20: 0.25, 30: 0.5, 45: 0.75, 60: 1, 90: 1.5})
            dataframe = dataframe[dataframe[column] <= 8]
        elif column in ['PostSleep_Fall_Asleep_Hours', 'PostSleep_Slept_Hours']:
            dataframe = dataframe[dataframe[column] <= 8]
        elif column in ['PostSleep_Fall_Asleep_Minutes', 'PostSleep_Slept_Minutes']:
            dataframe = dataframe[dataframe[column] <= 60]
        elif column in ['PH3_Weekday_Bed_Time', 'PH3_Weekend_Bed_Time', 'PreSleep_Last_Night_Bed_Time']:
            dataframe = self.calc_time(dataframe, column, start_time=22)
            dataframe = dataframe[(dataframe[column] >= -1) & (dataframe[column] <= 1)]
        elif column in ['PH3_Weekday_Getup_Time', 'PH3_Weekend_Getup_Time', 'PreSleep_Last_Day_Getup_Time']:
            dataframe = self.calc_time(dataframe, column, start_time=7)
            dataframe = dataframe[(dataframe[column] >= -1) & (dataframe[column] <= 1)]
        elif column == 'PreSleep_Last_Meal_Time':
            dataframe = self.calc_time(dataframe, column, start_time=6)
            dataframe = dataframe[(dataframe[column] >= -1) & (dataframe[column] <= 1)]
        elif column in ['Midpoint_Weekday', 'Midpoint_Weekend']:
            dataframe[column + '_Original'] = dataframe[column]
            dataframe = self.calc_time(dataframe, column, start_time=3)
            dataframe = dataframe[(dataframe[column] >= -1) & (dataframe[column] <= 1)]
        elif column in ['PostSleep_Feeling_Refreshing', 'PostSleep_Feeling_Tired', 'PostSleep_Feeling_Sleepy',
                        'PostSleep_Feeling_Alert']:
            dataframe[column] = dataframe[column].replace(refreshed_dict)
        elif 'Not at all / None' in dataframe[column].unique().tolist():
            dataframe[column] = dataframe[column].replace(anxiety_dict)
        elif column == 'PostSleep_Awake_Feeling':
            dataframe[column] = dataframe[column].replace(awake_feeling_dict)
        elif column == 'PostSleep_Last_Night_Sleep_Quality':
            dataframe[column] = dataframe[column].replace(sleep_quality_dict)
        elif column in ['CPAP', 'BIPAP', 'Oxygen']:
            dataframe[column] = dataframe[column].replace({'Yes': 1, 'No': 0})
        elif column in ['EpReading', 'EpWatchingTV', 'EpSittingQuietlyInPublicPlace', 'EpCarPassenger', 'EpLyingDown',
                        'EpTalking', 'EpSittingQuietlyAfterLunch', 'EpInCar']:
            dataframe[column] = dataframe[column].replace(
                {'Would never doze': 0, 'Slight chance': 1, 'Moderate chance': 2, 'High chance of dozing': 3})
        else:
            dataframe[column] = pd.to_numeric(dataframe[column]).abs()
        if column in log_cols:
            dataframe.loc[:, column] = np.log(dataframe.loc[:, column] + 1)
        return dataframe

    def get_variable_stats_from_df(self, dataframe, column):
        n0, n1, mean0, mean1, std0, std1, beta, std_err, p_value = super().get_variable_stats_from_df(dataframe, column)
        if not column.startswith('Midpoint'):
            mean0, mean1, std0, std1 = float(mean0), float(mean1), float(std0), float(std1)
        return n0, n1, mean0, mean1, std0, std1, beta, std_err, p_value

    def compute_muskuloskeletal_score(self, dataframe, cols, label):
        dataframe[label] = dataframe[cols].any(axis=1).astype(int)
        dataframe = dataframe.drop(columns=cols)
        return dataframe

    def compute_score(self, dataframe, cols, label):
        score_dict = {'Not at all / None': 0, 'Slight / Few times': 1, 'Moderate / Sometimes': 2, 'Often': 3,
                      'Severe / Always': 4}
        df_temp = dataframe.copy()
        for col in cols:
            if 'Not at all / None' in df_temp[col].unique().tolist():
                df_temp[col] = df_temp[col].replace(score_dict)
            else:
                df_temp[col] = df_temp[col].replace(1, 3)
        dataframe[label] = df_temp[cols].sum(1)
        return dataframe

    def insomnia_score(self, dataframe, is_cols, fatigue_cols):
        is_dict = {'Not at all / None': 0, 'Slight / Few times': 1, 'Moderate / Sometimes': 2, 'Often': 3,
                   'Severe / Always': 4}
        dataframe_temp = dataframe.copy()
        dataframe_temp[is_cols] = dataframe_temp[is_cols].replace(is_dict)
        dataframe_temp[fatigue_cols] = dataframe_temp[fatigue_cols].replace(is_dict)
        dataframe['Score'] = dataframe_temp[is_cols].sum(1)
        dataframe['Score2'] = dataframe_temp[fatigue_cols].sum(1)
        dataframe['Insomnia'] = dataframe.apply(lambda row: 1 if (row['Score'] >= 10) and (row['Score2'] >= 9) else 0 if row['Score'] <= 2 else np.nan, axis=1)
#        dataframe['Insomnia'] = (dataframe_temp[is_cols] > 2).any(axis=1).astype(int)
        return dataframe

    def combine_oa_hyp(self, dataframe):
        dataframe['OA_HYP_Duration'] = (dataframe['Durations_HI_Average_Duration'] * dataframe['Numbers_HI_Total'] +
                                        dataframe['Durations_OA_Average_Duration'] * dataframe['Numbers_OA_Total']) / \
                                       (dataframe['Numbers_OA_Total'] + dataframe['Numbers_HI_Total'])
        return dataframe

    def compute_at(self, dataframe):
        df2 = dataframe.copy()
        df2 = df2[df2['BMI'] <= 80]
        df2['Age'] = df2['Age'].abs()
        df2 = df2[df2['LowSat'] >= 60]
        df2['F_HYP'] = df2['Numbers_HI_Total']/(df2['Numbers_OA_Total'] + df2['Numbers_CA_Total'] + df2['Numbers_MA_Total'] + df2['Numbers_HI_Total'])
        df2['Gender'] = df2['Gender'].replace({'Male': 1, 'Female': 0})
        df2['AT'] = 0.06 * df2['Age'] + 3.69 * df2['Gender'] - 0.03 * df2['BMI'] - 0.11 * df2['Indices_AHI_Total'] + 0.53 * df2['LowSat'] + 0.09 * df2['F_HYP']
        df2['AT_NREM'] = 0.07 * df2['Age'] + 3.78 * df2['Gender'] + 0.03 * df2['BMI'] - 0.11 * df2['Indices_AHI_Total'] + 0.58 * df2['LowSat'] + 0.1 * df2['F_HYP']
        df2['AT_REM'] = 0.06 * df2['Age'] + 3.93 * df2['Gender'] - 0.19 * df2['BMI'] - 0.17 * df2['Indices_AHI_Total'] + 0.49 * df2['LowSat'] + 0.05 * df2['F_HYP']
        df2 = df2[['ID', 'AT', 'AT_NREM', 'AT_REM']]
        dataframe = dataframe.merge(df2, how='left', left_on='ID', right_on='ID')
        return dataframe

    def compute_shiftwork(self, dataframe):
        conditions = [
                (dataframe['PH2_Shift_2nd'] + dataframe['PH2_Shift_3rd'] > 0),
                (dataframe['PH2_Shift_1st'] == 1) & (dataframe['PH2_Shift_2nd'] == 0) & (dataframe['PH2_Shift_3rd'] == 0),
                (dataframe['PH2_Shift_1st'] == 0) & (dataframe['PH2_Shift_2nd'] == 0) & (dataframe['PH2_Shift_3rd'] == 0)
            ]

        dataframe['PH2_Shiftworker'] = np.select(conditions, [1, 0, 0], default=np.nan)
        dataframe = dataframe.drop(columns=['PH2_Shift_1st', 'PH2_Shift_2nd', 'PH2_Shift_3rd'])
        return dataframe

    def calc_time(self, dataframe, col, start_time=0):
        dataframe[col] = pd.to_datetime(dataframe[col])
        dataframe['time_of_day'] = (dataframe[col] - dataframe[col].dt.normalize() - pd.Timedelta(hours=start_time)).dt.total_seconds()
        dataframe['cos_time'] = np.cos(2 * np.pi * dataframe['time_of_day'] / (24 * 60 * 60))
        dataframe['sin_time'] = np.sin(2 * np.pi * dataframe['time_of_day'] / (24 * 60 * 60))
        dataframe[col] = np.arctan2(dataframe['sin_time'], dataframe['cos_time'])
        dataframe = dataframe.drop(columns=['time_of_day', 'cos_time', 'sin_time'])
        return dataframe

    def calculate_midpoint(self, bedtime_str_series, get_up_time_str_series):
        bedtime = pd.to_datetime(bedtime_str_series, format='%H:%M:%S', errors='coerce')
        get_up_time = pd.to_datetime(get_up_time_str_series, format='%H:%M:%S', errors='coerce')
        overnight_mask = get_up_time < bedtime
        get_up_time[overnight_mask] += pd.Timedelta(days=1)
        duration = get_up_time - bedtime
        midpoint = bedtime + duration / 2
        return midpoint.dt.time

    def calc_midpoint_mean(self, dataframe, column):
        dataframe[column] = pd.to_datetime(dataframe[column], format='%H:%M:%S').dt.time
        dataframe['seconds'] = dataframe[column].apply(lambda x: x.hour * 3600 + x.minute * 60 + x.second)
        mean_seconds = dataframe['seconds'].mean()
        std_seconds = dataframe['seconds'].std()
        mean_time = pd.to_datetime(mean_seconds, unit='s').time()
        std_time = pd.to_datetime(std_seconds, unit='s').time()
        return mean_time, std_time

    def calculate_sleep_durations(self, bedtime_str_series, get_up_time_str_series):
        bedtime = pd.to_datetime(bedtime_str_series, format='%H:%M:%S', errors='coerce')
        get_up_time = pd.to_datetime(get_up_time_str_series, format='%H:%M:%S', errors='coerce')
        overnight_mask = get_up_time < bedtime
        get_up_time[overnight_mask] += pd.Timedelta(days=1)
        duration = get_up_time - bedtime
        hours = duration.dt.total_seconds() / 3600  # Convert timedelta to hours
        return hours

    def combine_time_columns(self, df, hours_col, minutes_col, new_col_name):
        df.loc[df[hours_col] > 8, :] = np.nan
        df.loc[df[minutes_col] > 60, :] = np.nan
        df[new_col_name] = (df[hours_col] * 60) + df[minutes_col]
        df = df.drop(columns=[hours_col, minutes_col])
        return df

    def convert_sleep_hours(self, s):
        hour_str = ['hrs', 'HOUR', 'HOURS', 'hours', 'Hour', 'Hours', 'HRS', 'Hrs', 'HR', 'h', 'H', 'hr', 'hour', 'hs']
        if pd.isna(s) or s == '?' or s == 'varies' or s == '4-5 minutes' or s == '-' or s == '5-10 min' or s == '5 min' or \
                s == '5 mins' or s == '5-10 mins' or s == '5 minutes' or s == 'varies due to work' or s == '2-3 minutes':
            return np.nan
        elif s.isdigit():
            return s
        elif self.is_float(s):
            return s
        elif s == '15 min' or s == '20 min' or s == '20 mins' or s == '20min' or s == '15 mins' or s == '10 - 15 minutes' or \
                s == '15 MINUTE' or s == '15 mins' or s == '20 minutes' or s == '10 min' or s == '15min' or \
                s == '15 minutes' or s == '15-20 min' or s == '10 mins' or s == '20mins' or s == '10-15 min' or \
                s == '10min' or s == '15mins' or s == '10-15 mins' or s == '10 minutes' or s == '20m' or \
                s == '15-20 mins' or s == '15m' or s == '15' or s == '15-20 minutes' or s == '15-20min' or s == '10mins' or \
                s == '15-30min' or s == '10-15min' or s == '15 min.' or s == '20 mins.' or \
                s == '20 min.' or s == '10-15 minutes' or s == '10-20 min' or s == '10-30 min' or s == '15-20mins' or \
                s == '10-20 mins' or s == '10-15mins' or s == '10' or s == '10m' or s == '15 mins.' or s == '20 m' or \
                s == '10-20min' or s == '15-20':
            return 0.25
        elif s == '30 min' or s == '30 mins' or s == '30min' or s == '30 minutes' or s == '30mins' or s == '30' or s == '30m' or \
                s == '20-30 min' or s == '30 mins.' or s == '30 min.' or s == '15-30 min' or s == '20-30 mins' or \
                s == '20' or s == '1/2 hr' or s == '30 m' or s == '20-30min' or s == '15-30 mins' or s == '30-40 min' or \
                s == '1/2 hour' or s == '30 MIN' or s == '20-30 minutes' or s == '30-40 mins' or s == '25 min' or \
                s == '20-30mins' or s == '30 MINS' or s == '30mins.' or s == '30 Minutes' or s == '30-40min' or \
                s == '20-60 min' or s == '15-30' or s == '15-30 minutes' or s == '30min.' or s == '30 Mins' or \
                s == '20-30' or s == '15-30mins' or s == '30MIN' or s == '30MINS' or s == '30minutes' or \
                s == '30-40 minutes' or s == '30-45 mins.' or s == '30 MINUTES' or s == '30-40mins' or s == '30-40' or \
                s == '30 MIN.' or s == '30mns' or s == '30M':
            return 0.5
        elif s == '45 min' or s == '45 mins' or s == '45min' or s == '30-60 min' or s == '30-45 min' or \
                s == '45 minutes' or s == '30-60min' or s == '30-60 mins' or s == '45mins' or s == '30-45 mins' or \
                s == '40 min' or s == '30-45min' or s == '45m' or s == '45' or s == '30-60 minutes' or s == '40 mins' or \
                s == '30-45 minutes' or s == '30-60mins' or s == '30min-1hr' or s == '40min' or s == '30 min to 1 hr' or \
                s == '45 mins.' or s == '30-45mins' or s == '30-60m' or s == '45 min.' or s == '30-60' or \
                s == '40 minutes' or s == '30-45' or s == '30-1hr' or s == '30 min-1 hr' or s == '30-1 hr' or \
                s == '30-45m' or s == '30 mins to 1 hr' or s == '30 min - 1 hr' or s == '30mins-1hr' or s == '30 min-1hr' or \
                s == '30 mins - 1 hr' or s == '30 min- 1 hr' or s == '30m-1h' or s == '30 to 45 min' or \
                s == '30 - 60 min' or s == '30 to 60 min.' or s == '30 - 60 minutes' or s == '30 mins. to 1 h' or \
                s == '30min to 1hr' or s == '30min-1 hr' or s == '30 to 60 mins' or s == '30 to 45 minute' or s == '30-60 mins.':
            return 0.75
        elif s == '60 min' or s == '60min' or s == '60 mins' or s == '60 minutes' or s == '60' or s == '60m' or \
                s == '60mins' or s == '45-60 min' or s == '0-2 TIMES' or s == '30-90 min' or s == 'one hour' or \
                s == '30-90min' or s == '30-90 mins':
            return 1
        elif s == '90 min' or s == '1.5 hours' or s == '1 1/2 hrs' or s == '90 mins' or s == '1 1/2 hours' or \
                s == '1.5hrs' or s == '90min' or s == '1-2 hr' or s == '1-2 hrs.' or s == '1-2h' or \
                s == '90 minutes' or s == '60-90 min' or s == '1 1/2 hr' or s == '1-1.5 hrs' or s == '90mins' or \
                s == '1-2 h' or s == '1-2hours' or s == '1.5h' or s == '90m' or s == '1-2 HRS' or s == '1 1/2hrs' or \
                s == '1 - 2 hrs.' or s == '1 or 2 hours' or s == '1 hr 30 min' or s == '1-1.5hrs' or s == '90' or \
                s == '1-1.5 hours' or s == '1 - 2 hours' or s == '60-90 mins' or s == '1 or 2 hrs' or s == '60-90min' or \
                s == '1-2hr' or s == '1 to 2 hours' or s == '1 to 2 hrs' or s == '1-2 times' or s == '1-2x' or \
                s == '1-2 hrs' or s == '1-2 hours' or s == '1-2hrs' or s == '90 min.' or s == '1 - 2 hrs' or \
                s == '30min-2hrs' or s == '30-120 min' or s == '30 min - 2 hrs':
            return 1.5
        elif s == '1-3 hrs' or s == '1-3 hours' or s == '1-3hrs' or s == '1.5-2 hrs' or s == '1.5-2 hours' or s == '2x':
            return 2
        elif s == '2-3 hrs.' or s == '2-3 hr' or s == '2 1/2 hrs' or s == '2-3h' or s == '1-4 hours' or s == '2 to 3 hrs' or \
                s == '21/2 hours':
            return 2.5
        elif s == '2-3 times' or s == '2-3x' or s == '2--3 HOURS' or s == '2-3 hrs' or s == '2-3 hours' or s == '2-3hrs' or \
                s == '2-4 hrs' or s == '2-4 hours' or s == '2-4hrs' or s == '1-4 hrs' or s == '1 1/2 - 5 hrs' or \
                s == '3,4 or 5' or s == '3xs' or s == '3time' or s == '3x' or s == '2-4 intervals' or s == '3 x':
            return 3
        elif s == '3-4 hrs' or s == '3-4 hours' or s == '3-4hrs' or s == '3or 4 hr' or s == 'between 2-5 hrs each night':
            return 3.5
        elif s == '4 -- 5 hours' or s == '4-41/2hrs' or s == '4-41/2 hours' or s == '4-5 hrs' or s == '4.5hrs' or \
                s == '4.5 hrs' or s == '4 to 5':
            return 4.5
        elif s == '5-hr' or s == '4-6x' or s == '4 to 6' or s == 'maybe 5h' or s == 'varies 5 hrs?' or \
                s == 'varies 3-4/6/8' or s == 'About 5 hrs.' or s == '5/hours' or s == '5 not constant':
            return 5
        elif s == '51/2`' or s == '5-6?' or s == '5 hours, occasionally 7 - 8' or s == '5 - 6 Times' or \
                s == '5 1/2 HRS' or s == '5 to 6' or s == '5/6hrs' or s == '5.5 hrs':
            return 5.5
        elif s == '6-61/2 hrs.' or s == '6-7X' or s == '6--7 HOURS' or s == '6-7 times' or s == '6-6 1/2' or \
                s == '6-7 now' or s == '6--7 hours' or s == '6.5 hrs' or s == '6.5 hours' or s == '6-7 average' or \
                s == '6.5hrs' or s == '6.5hr':
            return 6.5
        elif s == '5 1/2-6 hours' or s == '5-6  1/2hrs.' or s == '4-8 interrupted' or s == '- 6 hr':
            return 6
        elif s == '6 1/2-7hrs' or s == '5-8 ?' or s == '7 - ?' or s == '6 1/2 - 7 1/2 hrs' or \
                s == '7 wkdys 11-12wknd' or s == '6 to 8' or s == '6-7  /  9-10 wkends' or s == '6.85 hrs' or s == '6,7 or 8hrs':
            return 7
        elif s == '-4' or s == '10:30-2am then wake frequently' or s == '10-30 - 2 am the wake freq.' or \
                s == '3-5 times' or s == '3.5 to 4 hrs' or s == '3-5times' or s == '4x':
            return 4
        elif s == 'varies 2-3 or 8+' or s == '5 1/2-6 1/2 hours':
            return 6
        elif s == '7 plus' or s == '7-8 total' or s == '7-8 rarely more sometimes much less' or s == '7.5 hrs' or \
                s == '7.5 hr' or s == '7 to 8' or s == '7+8' or s == '7 & half hours' or s == '7.5 hrs.' or \
                s == '7--8 hr' or s == '7 ro 8 hrs':
            return 7.5
        elif s == '8-1/2hrs.' or s == '7-8 1/2' or s == '71/2 - 8 hrs' or s == '6--9' or s == '4-12  / varies greatly' or \
                s == '7-8`' or s == '8 times' or s == '7+' or s == '8 +/- hr' or s == '7 1/2-8' or s == '7 1/2 - 8' or s == '7 1/2-8 hrs':
            return 8
        elif s == '8.5 hrs' or s == '8.5 hours' or s == '8.5hrs' or s == '8.5 hr' or s == '8 to 9':
            return 8.5
        elif s == '8+' or s == '8 +' or s == '8+ hours':
            return 9
        elif s == '9.5 hours' or s == '9+' or s == '9.5hrs':
            return 9.5
        elif s == '10 - 12 fitful':
            return 11
        elif s == '11or 12':
            return 11.5
        elif s == '12+':
            return 13
        else:
            hour = next((h for h in hour_str if h in s), None)
            if '-' in s:
                s_split = s.split('-')
                if hour:
                    idx = s.find(hour)
                    if idx > 0 and s[idx-1] == ' ':
                        s_split2 = s_split[1].split(hour)
                        try:
                            s = (float(s_split[0]) + float(s_split2[0])) / 2
                        except:
                            return np.nan
                    else:
                        s_split2 = s_split[1].split(hour.strip())
                        try:
                            s = (float(s_split[0]) + float(s_split2[0])) / 2
                        except:
                            return np.nan
                    return s
                else:
                    try:
                        s = (float(s_split[0]) + float(s_split[1])) / 2
                        return s
                    except ValueError:
                        return np.nan
            elif hour:
                s_split = s.split(hour[0])
                if 'or' in s_split[0]:
                    s_split = s_split[0].split(' or')
                elif 'to' in s_split[0]:
                    s_split = s_split[0].split(' to')
                elif 'TO' in s_split[0]:
                    s_split = s_split[0].split(' TO')
                elif 'and' in s_split[0]:
                    s_split = s_split[0].split(' and')
                elif '1/2' in s_split[0]:
                    s_split = s_split[0].split(' 1/2')
                if s_split[0].isdigit():
                    return s_split[0]
                elif s_split[0].strip().isdigit():
                    return s_split[0].strip()
                else:
                    return np.nan
            elif 'or' in s:
                s_split = s.split(' or')
                if s_split[0].isdigit():
                    return s_split[0]
                else:
                    return np.nan
            elif 'AND' in s:
                s_split = s.split('AND')
                if s_split[0].isdigit():
                    return s_split[0]
                else:
                    return np.nan
            elif 'to' in s:
                s_split = s.split('to')
                if s_split[0].isdigit():
                    return s_split[0]
                else:
                    return np.nan
            else:
                return np.nan

    def convert_n_naps(self, s):
        if s.isdigit():
            return s
        elif s == '0 times' or s == '0x' or s == '0 x' or s == 'rarely':
            return 0
        elif s == '0-1' or s == '2/wk' or s == '1/wk' or s == '2/week' or s == '1-2/wk' or s == '2-3/wk' or \
                s == '2 a week' or s == '2 week' or s == '2 per wk' or s == '3/week' or s == '2or3' or s == '1-2 week' or \
                s == '1-2/week' or s == '0-1' or s == '0-1 times' or s == '0-1x' or s == '0-1 time' or s == '0 - 1' or \
                s == 'maybe 1' or s == '1 X':
            return 0.5
        elif s == '1 max.' or s == '0-2x' or s == '1 all day' or s == 'one' or s == '0-2' or s == '1 sometimes' or \
                s == '1x' or s == 'maybe 1' or s == 'sometimes 1' or s == 'once' or s == '&lt;1' or s == '3/wk' or \
                s == 'everyday' or s == '1`' or s == 'Once' or s == '1 a day' or s == '1 per day' or s == 'every day' or \
                s == '&gt;1' or s == 'at least 1' or s == '1 time' or s == '1?' or s == '1 times' or s == '1 x' or \
                s == '1time' or s == '1 Time' or s == '1X' or s == '1times' or s == 'x1' or s == '&lt;1' or \
                s == '0-2 times' or s == 'Once' or s == '1 TIME':
            return 1
        elif s == '1 or 2' or s == '1 to 2' or s == '1or2' or s == '1or 2' or s == '1 or more' or s == '0-3' or \
                s == '1-2x' or s == '1 or2' or s == '1 OR 2' or s == '1-2 times' or s == '1-2 x' or s == '1 or 2 times' or \
                s == '1-2times' or s == '1 - 2 times' or s == '1- 2 times' or s == '1 to 2 times' or s == '1-2X' or \
                s == '1-2xs' or s == '1 or 2x' or s == '1-2 TIMES' or s == '1 - 2 Times':
            return 1.5
        elif s == '2x' or s == '1+' or s == 'twice' or s == '2 times' or s == '2times' or s == '2 x' or s == '1-3 times' or \
                s == "2 x's" or s == '2X' or s == '2 Times' or s == '2xs' or s == '1-3x' or s == 'x2' or s == '2 TIMES' or \
                s == '2t' or s == 'twice' or s == '2 time':
            return 2
        elif s == '2 or 3' or s == '2 to 3' or s == '2 or more' or s == '2or 3' or s == '2-3 times' or s == '2-3x' or \
                s == '2-3 x' or s == '2-3times' or s == '2 or 3 times' or s == '2 to 3 times' or s == '2- 3 times' or \
                s == '2 - 3 times' or s == '2-3X' or s == '2 or more' or s == "2 to 3 x's" or s == '2 - 3 Times' or \
                s == '1-4 times' or s == '2-3 TIMES' or s == '2 or 3x' or s == '2/3 times':
            return 2.5
        elif s == '2+' or s == '3 times' or s == '3x' or s == '3 x' or s == '3times' or s == '2-4 times' or s == "3 x's" or \
                s == '2-4x' or s == '3xs' or s == '3 Times' or s == 'x3' or s == '3 TIMES' or s == '2-3xs' or s == '2-4 x':
            return 3
        elif s == '3 or 4' or s == '3 to 4' or s == '3x' or s == '3-4 times' or s == '3-4x' or s == '3-4 x' or \
                s == '3 or 4 times' or s == '3-4times' or s == '3X' or s == '3 to 4 times' or s == '3 or more' or \
                s == '3- 4 times' or s == '2-5 times' or s == '3 - 4 times' or s == '3/4 times' or s == '3-4X' or \
                s == "3 to 4 x's" or s == '3-4xs' or s == '2-5x':
            return 3.5
        elif s == '3+' or s == '4 times' or s == '4x' or s == '3-5 times' or s == '4times' or s == '4 x' or s == '3-5x' or \
                s == "4 x's" or s == '3-5 x' or s == '4X' or s == 'x4' or s == '3 or 4x' or s == '3 to 5' or s == '4xs':
            return 4
        elif s == '4 or 5' or s == '4 to 5' or s == '4-5 times' or s == '4-5x' or s == '4-5 x' or s == '4 or 5 times' or \
                s == '3-6 times' or s == '4-5times' or s == '4 or more' or s == '4 to 5 times' or s == '4 Times':
            return 4.5
        elif s == '5 times' or s == '5x' or s == '4-6 times' or s == '5 x' or s == '4+' or s == '4-6x' or s == '5times' or \
                s == '5 min' or s == "5 x's":
            return 5
        elif s == '5-6 times' or s == '5-6x' or s == '5 or 6' or s == '5-6 x' or s == '5 or more' or s == '5 to 6':
            return 5.5
        elif s == '5+' or s == '6 times' or s == '6x' or s == '5-7 times' or s == '6 x' or s == '6times':
            return 6
        elif s == '6-7 times':
            return 6.5
        elif s == '7 times' or s == '6-8 times' or s == '7x' or s == '6+' or s == '6-8x':
            return 7
        elif s == '7-8 times' or s == '5-10 times':
            return 7.5
        elif s == '8 times' or s == '8x':
            return 8
        elif s == '8-10 times':
            return 9
        elif s == '10 times' or s == '10x' or s == '10 min' or s == '10+':
            return 10
        else:
            return np.nan

    def convert_n_beverages(self, s):
        if s.isdigit():
            return s
        elif s in ['1 oz', '1oz', '1.5 oz', '1 1/2 oz', '2 sips', '2 ounces', '1.5oz', 'sip', '1 oz.', '1/2 oz', '1 ounce']:
            return 0.1
        elif s in ['2 oz', '2oz', '3 oz', '3oz', '2 oz.', '3 oz.', '1/4 glass', '2-3oz', '1/4 cup', '2 oz']:
            return 0.25
        elif s in ['1/2 glass', '4oz', '4 oz', 'small glass', '5 oz', '1 small glass', '1/2 cup', '5oz', 'half glass',
                   '4 oz.', '1/2 bottle', '1/2 can', '1/2', '1/2glass', '1/2 pint', '1/2 Glass', '1/2 beer', '1.5 cups',
                   'small cup', 'half cup', '1/2cup', 'small', '1 small cup', '1 soda', '1/cup', '.5 cup', '1/2 c',
                   'half a cup', 'half glass']:
            return 0.5
        elif s in ['6oz', '6 oz', '8oz', '8 oz', '6 oz.', '8 oz.', '7 oz', '8 ounces', '8oz.', '6 oz.', '3/4 cup',
                   '8 ozs']:
            return 0.75
        elif s in ['1 glass', '12 oz', '12oz', '1 can', '1 drink', '1 bottle', '1 cup', '1 beer', '1glass', 'one',
                   '1 shot', '1 Glass', 'glass', '12 oz.', 'one glass', '1 GLASS', '1 glass wine', '1 each', '1cup',
                   '1 Beer', '10 oz', '10oz', '1can', '1 glass of wine', '1 pint', '2 small glasses', '1 Bottle',
                   '12oz.', '1 12oz', 'One', 'one beer', '1drink', '12 OZ', '12 ounces', '12 ozs', '1 c', '1 12 oz',
                   'shot', '1-12oz', '1 Drink', '10 oz.', '1c', '1 Cup', '1 cup each', '1 CUP', 'one cup', 'glass',
                   '1glass', '1 mug', '1 cup each time', 'can', '12 oz can', '1 cup coffee', '1 glass each',
                   '1 of each', '12 OZ', '1 CAN', '1 cups', '12 ozs.', '12oz can', '1 Can', '1 cup.', 'a cup',
                   'one can', '1cp', '12 oz each', '12OZ', '1- cup', 'medium', '14 oz', '1 cup/1 glass',
                   '1 cup of each', '1CUP', '14oz', '1/1']:
            return 1
        elif s in ['16oz', '16 oz', '1.5 glasses', '1 1/2 glasses', '1.5', '16 oz.', '1 1/2 glass', '1 1/2',
                   '1.5 glass', '1 1/2 cups', '1 large cup', '16 ounces', '16oz.', '1 1/2 cup', 'large', '16 ozs',
                   '1.5cups', '18 oz', '16OZ', '18oz', '16 OZ', '1-2 cups', '16 ozs.']:
            return 1.5
        elif s in ['20 oz', '20oz', '20 oz.', '20 ounces', '20oz.', '20 ozs']:
            return 1.75
        elif s in ['2 glasses', '2 drinks', '2 cans', '2 beers', '2 cups', '24 oz', '24oz', '2 shots', '2 bottles',
                   '2glasses', '2 Glasses', '24 oz.', '2cups', '2cans', '2 GLASSES', '2 glass', '2-12oz', '2 Beers',
                   '2 12oz', '2 beer', '2 glasses wine', '2 gl', '2 c', '2c', '2 Cups', '2 CUPS', '2 cup', '2 mugs',
                   '1 cup, 1 glass', '2 cups coffee', '2 cups.', '2 cups total', '1 cup, 1 can', '2- cups', '2cps',
                   '24 ounces', '2 cups each', '2 large cups', '2 cps']:
            return 2
        elif s in ['2-3', '32oz', '32 oz', '2-3 cups', '2.5 cups', '30 oz', '2 1/2 cups', '32 oz.', '30oz']:
            return 2.5
        elif s in ['3 glasses', '3 beers', '3 cans', '3 drinks', '3 cups', '3 bottles', '3 shots', '36oz', '3cups',
                   '3 c', '1 liter', '3 Cups', '3c', '36 oz', '3 CUPS', '3 cups total', '2 cups, 1 glass',
                   '2 cups, 1 can']:
            return 3
        elif s in ['3-4', '40 oz', '3-4 cups', '40oz', '44oz']:
            return 3.5
        elif s in ['4 cans', '4 beers', '4 glasses', '4 cups', '4 drinks', '4cups', '1 pot', '48 oz', '48oz', '4 c',
                   '4 cups total', '4 Cups']:
            return 4
        elif s == '4-5 cups':
            return 4.5
        elif s in ['5 beers', '5 cans', '5 cups', '60 oz', '60oz']:
            return 5
        elif s in ['6 pack', '6 beers', '6 cans', '6 cups', '2 liters']:
            return 6
        elif s == '8 cups':
            return 8
        elif s == '10 cups':
            return 10
        else:
            return np.nan

    def get_recording_info(self, f):
        start_time = f.getStartdatetime()
        duration = f.getFileDuration()
        fs = f.getSampleFrequencies()
        signal_labels = f.getSignalLabels()
        units = [f.getPhysicalDimension(i) for i in range(len(fs))]
        physical_min = [f.getPhysicalMinimum(i) for i in range(len(fs))]
        physical_max = [f.getPhysicalMaximum(i) for i in range(len(fs))]
        digital_min = [f.getDigitalMinimum(i) for i in range(len(fs))]
        digital_max = [f.getDigitalMaximum(i) for i in range(len(fs))]
        transducer = [f.transducer(i) for i in range(len(fs))]
        prefilter = [f.prefilter(i) for i in range(len(fs))]
        startdatetime = f.getStartdatetime()
        return start_time, duration, fs, signal_labels, units, physical_min, physical_max, digital_min, digital_max, transducer, prefilter, startdatetime

    def get_channel_labels(self, f, channel):
        signal_labels = f.getSignalLabels()
        channel_labels = channel_alias[channel] + unref_channel_alias[channel] + ref_channel_alias[channel]
        channel_labels = list(dict.fromkeys(channel_labels))
        labels_in_file = sorted([c for c in channel_labels if c in signal_labels])
        if len(labels_in_file) == 0:
            labels_in_file = [np.nan]
            idx = np.nan
        else:
            idx = signal_labels.index(labels_in_file[0])
        return labels_in_file, idx

    # def plot_roc__all_variables(self, y_true, y_prob, y_pred=None):
    #     if y_prob.ndim == 2:
    #         y_prob = y_prob[:, 1]
    #     fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    #     roc_auc = roc_auc_score(y_true, y_prob)
    #
    #     youden_index = tpr - fpr
    #     best_threshold = thresholds[np.argmax(youden_index)]
    #
    #     if y_pred is None:
    #         y_pred = (y_prob >= best_threshold).astype(int)
    #
    #     plt.figure(figsize=(15, 5))
    #
    #     # ROC Curve
    #     plt.subplot(1, 2, 1)
    #     plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    #     plt.plot([0, 1], [0, 1], color='grey', lw=2, linestyle='--')
    #     plt.xlim([0.0, 1.0])
    #     plt.ylim([0.0, 1.05])
    #
    #     # Increase fontsize by 2 on ROC Curve
    #     plt.xlabel('False Positive Rate', fontsize=14)
    #     plt.ylabel('True Positive Rate', fontsize=14)
    #     plt.legend(loc='lower right', fontsize=14)
    #
    #     # Confusion Matrix
    #     cm = confusion_matrix(y_true, y_pred)
    #     cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    #
    #     plt.subplot(1, 2, 2)
    #     plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    #     plt.colorbar()
    #
    #     # Increase fontsize by 2 on Confusion Matrix labels
    #     tick_marks = np.arange(2)
    #     plt.xticks(tick_marks, ['OSA/Insomnia', 'COMISA'], fontsize=14)
    #     plt.yticks(tick_marks, ['OSA/Insomnia', 'COMISA'], fontsize=14)
    #
    #     # Increase fontsize of the text inside Confusion Matrix
    #     thresh = cm.max() / 2.
    #     for i, j in np.ndindex(cm.shape):
    #         plt.text(j, i, f'{cm_normalized[i, j] * 100:.1f}%\n({cm[i, j]})',
    #                  horizontalalignment="center",
    #                  fontsize=12,  # Increase text fontsize
    #                  color="white" if cm[i, j] > thresh else "black")
    #
    #     plt.ylabel('True label', fontsize=14)
    #     plt.xlabel('Predicted label', fontsize=14)
    #     plt.tight_layout()
    #     plt.show()
