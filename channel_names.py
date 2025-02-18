channel_alias = {'eeg_left': ['C3M2', 'C3A2', 'C3-M2', 'EEG C3-A2', 'C3M1', 'CZM2', 'C3:M2'],
                 'eeg_right': ['C4M1', 'C4A1', 'C4-M1', 'EEG C4-A1', 'C4M2', 'CZM2', 'C4:M1'],
                 'eye_left': ['LOC', 'LEOG', 'E1-M2', 'EOG LOC-A2', 'EOG1:M2'],
                 'eye_right': ['ROC', 'REOG', 'E2-M2', 'EOG ROC-A1', 'EOG ROC-A2', 'EOG2:M1'],
                 'chin': ['Chin', 'CHIN', 'chin', 'EMG', 'CHINEMG', 'ChinEMG', 'EMG Chin', 'Chin1-Chin2', 'Chin 1-Chin 2'],
                 'ekg': ['ECG', 'EKG', 'ECG1-ECG2'],
                 'resp_cannula': ['PFlo', 'Pflo', 'PFLO', 'PTAF', 'Nasal Pressure', 'PAP Flow', 'Pflow', 'PFlow', 'Ptaf', 'Flow Patient'],
                 'resp_thermistor': ['TFlo', 'Tflo', 'TFLO', 'Flow', 'Thermistor', 'FLOW', 'Thermist', 'Airflow', 'Therm', 'Flow Patient'],
                 'resp_chest': ['Tho', 'THO', 'Thorax', 'Thor', 'THOR', 'Effort THO'],
                 'resp_abdomen': ['Abd', 'ABD', 'Abdomen', 'Abdo', 'ABDM', 'Effort ABD'],
                 'oxygen_sat': ['SAO2', 'SpO2']
                 }


unref_channel_alias = {'eeg_left': ['C3'],
                       'eeg_right': ['C4'],
                       'eye_left': ['E1'],
                       'eye_right': ['E2'],
                       'chin': ['ChinL', 'Chin-L', 'ChinR', 'Chin-R'],
                       'ekg': ['ECG2', 'ECGII', 'ECG II'],
                       'resp_cannula': [],
                       'resp_thermistor': [],
                       'resp_chest': [],
                       'resp_abdomen': [],
                       'oxygen_sat': []
                       }

ref_channel_alias = {'eeg_left': ['M2'],
                     'eeg_right': ['M1'],
                     'eye_left': ['M2'],
                     'eye_right': ['M1'],
                     'chin': ['ChinA', 'Chin-A'],
                     'ekg': ['ECG1', 'ECGI', 'ECG I'],
                     'resp_cannula': [],
                     'resp_thermistor': [],
                     'resp_chest': [],
                     'resp_abdomen': [],
                     'oxygen_sat': []
                     }

channel_units_alias = {'eeg_left': 'uV', 'eeg_right': 'uV', 'eye_left': 'uV', 'eye_right': 'uV', 'chin': 'uV', 'ekg': 'uV',
                       'resp_cannula': 'uV', 'resp_thermistor': 'uV', 'resp_chest': 'uV', 'resp_abdomen': 'uV', 'oxygen_sat': '%'}

unit_alias = {'uV': ['uV', 'u'],
         'mV': ['mV', 'm'],
         'cmH2O': ['cmH20', 'cmH2O', 'CmH20', 'CmH2O', 'cm H2O', 'cm'],
         'L/min': ['l/min', 'L/min', 'LPM', 'Lpm', 'l/m', 'lpm'],
         'bpm': ['bmp', 'bpm', 'Bpm'],
         'mmHg': ['mmHg', 'mmHG']}

des_fs = {'C3': 120, 'C4': 120, 'LEOG': 120, 'REOG': 120, 'Chin': 120,
          'ECG': 120}

hp_fs = {'F3': [0.3, 45.0], 'F4': [0.3, 45.0], 'C3': [0.3, 45.0], 'C4': [0.3, 45.0], 'O1': [0.3, 45.0],
         'O2': [0.3, 45.0], 'LEOG': [0.3, 45.0], 'REOG': [0.3, 45.0], 'Chin': 10.0, 'ECG': 0.3}