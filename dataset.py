from helper_functions import Helper
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)  # Ignore FutureWarnings

class MorpheusDataset:
    def __init__(self, excel_path, psg_criterion=False):
        self.excel_path = excel_path
        self.psg_criterion = psg_criterion

        self.h = Helper()
        self.var_df = pd.read_csv(os.path.join(os.getcwd(), 'Data', 'Group_Variable_Info.csv'))
        self.insomnia_cols = self.get_columns(score_label='Insomnia_Score')
        self.fatigue_cols = self.get_columns(score_label='Fatigue_Score')
        self.allergy_cols = self.get_columns(score_label='Allergy_Score')
        self.muskuloskeletal_cols = self.get_columns(score_label='Muskuloskeletal_Pain_Score')
        self.reflux_cols = self.get_columns(score_label='Reflux_Score')
        self.cardiopulmonary_cols = self.get_columns(score_label='Cardiopulmonary_Score')
        self.other_cols = self.get_columns(score_label='Other_Score')
        self.apnea_cols = self.get_columns(score_label='Apnea_Cols')

        self.data = self.load_data()

    def get_columns(self, score_label):
        score_columns = self.var_df[self.var_df[score_label] == 1]['Columns'].tolist()
        return score_columns

    def load_data(self):
        df_meta = pd.read_csv(os.path.join(self.excel_path), low_memory=False)
        if self.psg_criterion:
            df_meta = df_meta[df_meta['StudyType'] == 'Baseline PSG']
            df_meta = df_meta[df_meta['TST'] >= 60]

        df_meta = self.h.insomnia_score(dataframe=df_meta, is_cols=self.insomnia_cols, fatigue_cols=self.fatigue_cols)
        df_meta = self.h.compute_score(dataframe=df_meta, cols=self.allergy_cols, label='Allergy_Score')
#        df_meta = self.h.compute_score(dataframe=df_meta, cols=self.muskuloskeletal_cols, label='Muscoskeletal_Pain_Score')
        df_meta = self.h.compute_muskuloskeletal_score(dataframe=df_meta, cols=self.muskuloskeletal_cols, label='Muscoskeletal_Pain_Score')
        df_meta = self.h.compute_score(dataframe=df_meta, cols=self.reflux_cols, label='Reflux_Score')
        df_meta = self.h.compute_score(dataframe=df_meta, cols=self.cardiopulmonary_cols, label='Cardiopulmonary_Score')
        df_meta = self.h.compute_score(dataframe=df_meta, cols=self.other_cols, label='Other_Score')

        df_meta['PH3_Sleep_Hours'] = df_meta['PH3_Sleep_Hours'].apply(self.h.convert_sleep_hours).astype(float)
        df_meta['PH3_Weekday_Nap_Last_Hours'] = df_meta['PH3_Weekday_Nap_Last_Hours'].apply(self.h.convert_sleep_hours).astype(float)
        df_meta['PH3_Weekend_Nap_Last_Hours'] = df_meta['PH3_Weekend_Nap_Last_Hours'].apply(self.h.convert_sleep_hours).astype(float)
        df_meta['Percentage_Stage1_2'] = df_meta['Percentage_Stage1'] + df_meta['Percentage_Stage2']
        df_meta['Duration_Stage1_2'] = df_meta['Duration_Stage1'] + df_meta['Duration_Stage2']
        df_meta['PH3_Weekday_Nap_Hours'] = df_meta['PH3_Weekday_Nap_Hours'].astype(str).apply(self.h.convert_n_naps).astype(float)
        df_meta['PH3_Weekend_Nap_Hours'] = df_meta['PH3_Weekend_Nap_Hours'].astype(str).apply(self.h.convert_n_naps).astype(float)
        df_meta['PH3_Wakeup_Nooftimes'] = df_meta['PH3_Wakeup_Nooftimes'].astype(str).apply(self.h.convert_n_naps).astype(float)
#        df_meta['PostSleep_Wakeup_Comments'] = df_meta['PostSleep_Wakeup_Comments'].astype(str).apply(self.h.convert_n_naps).astype(float)
        df_meta['Midpoint_Weekday'] = self.h.calculate_midpoint(df_meta['PH3_Weekday_Bed_Time'], df_meta['PH3_Weekday_Getup_Time']).astype(str)
        df_meta['Midpoint_Weekend'] = self.h.calculate_midpoint(df_meta['PH3_Weekend_Bed_Time'], df_meta['PH3_Weekend_Getup_Time']).astype(str)
        df_meta['Sleep_Hours_Weekday'] = self.h.calculate_sleep_durations(df_meta['PH3_Weekday_Bed_Time'], df_meta['PH3_Weekday_Getup_Time'])
        df_meta['Sleep_Hours_Weekend'] = self.h.calculate_sleep_durations(df_meta['PH3_Weekend_Bed_Time'], df_meta['PH3_Weekend_Getup_Time'])
        df_meta['Sleep_Hours_Diff'] = df_meta['Sleep_Hours_Weekend'] - df_meta['Sleep_Hours_Weekday']
#        df_meta['PreSleep_Alcohol_Beverage_Quantity'] = df_meta['PreSleep_Alcohol_Beverage_Quantity'].astype(str).apply(self.h.convert_n_beverages).astype(float)
#        df_meta['PreSleep_Caffeinated_Beverage_Quantity'] = df_meta['PreSleep_Caffeinated_Beverage_Quantity'].astype(str).apply(self.h.convert_n_beverages).astype(float)
#        df_meta = self.h.combine_time_columns(df_meta, 'PostSleep_Fall_Asleep_Hours', 'PostSleep_Fall_Asleep_Minutes', 'PostSleep_Fall_Asleep')
#        df_meta = self.h.combine_time_columns(df_meta, 'PostSleep_Slept_Hours', 'PostSleep_Slept_Minutes', 'PostSleep_Slept')
#        df_meta['TST_Misperception'] = df_meta['TST'] - df_meta['PostSleep_Slept']
#        df_meta['SOL_Misperception'] = df_meta['SOL'] - df_meta['PostSleep_Fall_Asleep']
#        df_meta['Awakenings_Misperception'] = (df_meta['AI_Awakenings'] * (df_meta['TST']/60)) - df_meta['PostSleep_Wakeup_Comments']
        df_meta = self.h.combine_oa_hyp(df_meta)
        df_meta = self.h.compute_at(df_meta)
        df_meta = self.h.compute_shiftwork(df_meta)
#        df_meta['Antihistamines'] = df_meta[['Antihistamine_Pain', 'Antihistamine_Pure']].max(axis=1)
        return df_meta


if __name__ == '__main__':
#    excel_path = 'C:/Code/projects/somno/cerebra/Data/Cerebra_Dataset_All.csv'
    excel_path = 'C:/Code/projects/somno/morpheus/Data/Morpheus_Data_All2.csv'
    self = MorpheusDataset(excel_path=excel_path)
    df = self.data
