import os
import pyedflib
import shutil
import glob
import numpy as np
from scipy.signal import resample
from channel_names import *
from helper_functions import Helper
import pandas as pd


class CerebraDataset:
    def __init__(self, path):
        self.path = path
        self.excel_path = os.path.join(self.path, 'Excel')
        self.oak_edf_path = '/oak/stanford/groups/mignot/psg/Bioserenity/edf'
        self.groups = ['Control', 'Insomnia', 'OSA', 'COMISA']
        self.h = Helper()

    def get_files_group(self, group, file_type='predictions'):
        if file_type == 'edfs':
            edfs_path = os.path.join(self.path, group)
        elif file_type == 'predictions':
            edfs_path = os.path.join(self.path, group + '_Predictions')
        files = os.listdir(edfs_path)
        return files

    def get_files_group2(self, group):
        df = pd.read_csv(os.path.join(self.excel_path, 'Subjects_All.csv'))
        df_group = df[df['Group'] == group]
        files = df_group['ID'].astype(str).tolist()
        return files

    def transfer_edfs_group(self, group):
        files = self.get_files_group2(group)
        for file in files:
            edf_files = glob.glob(os.path.join(self.oak_edf_path, file + '*'))
            if len(edf_files) > 1:
                for edf_file in edf_files:
                    output_edf = os.path.join(self.path, group, os.path.basename(edf_file))
                    if not os.path.exists(output_edf):
                        shutil.copy(edf_file, output_edf)
            else:
                edf_file = edf_files[0]
                output_edf = os.path.join(self.path, group, os.path.basename(edf_file))
                if not os.path.exists(output_edf):
                    shutil.copy(edf_file, output_edf)

    def transfer_all_edfs(self):
        for group in self.groups:
            self.transfer_edfs_group(group)

    def resample_signals_all(self):
        for group in self.groups:
            files = os.listdir(os.path.join(self.path, group))
            for file in files:
                self.resample_signals(file, group)

    def resample_signals(self, file, group):
        f = pyedflib.EdfReader(os.path.join(self.path, group, file))
        start_time, duration, fs, signal_labels, units, physical_min, physical_max, digital_min, digital_max, transducer, prefilter, startdatetime = self.h.get_recording_info(f)
        body = {}
        for channel in ['eeg_left', 'eeg_right', 'eye_left', 'eye_right', 'chin', 'ekg', 'resp_cannula', 'resp_thermistor', 'resp_chest', 'resp_abdomen', 'oxygen_sat']:
            label, idx = self.h.get_channel_labels(f, channel)
            body[channel] = {'channel_name': label[0], 'channel_index': idx}

        remove_keys = []
        for key in body.keys():
            if np.isnan(body[key]['channel_index']):
                remove_keys.append(key)

        if len(remove_keys) > 0:
            for key in remove_keys:
                del body[key]

        new_data = []
        new_freqs = []
        new_signal_labels = []
        n = len(fs)

        if fs[body['eeg_left']['channel_index']] >= 120:
            return None

        for i in range(n):
            signal = f.readSignal(i)
            label = signal_labels[i]
            freq = fs[i]

            if label in [body['eeg_left']['channel_name'], body['eeg_right']['channel_name'],
                         body['eye_left']['channel_name'], body['eye_right']['channel_name'],
                         body['chin']['channel_name'], body['ekg']['channel_name']] and freq < 120:

                new_length = int(duration * 120)
                upsampled_signal = resample(signal, new_length)
                new_freq = 120
            else:
                upsampled_signal = signal
                new_freq = freq

            new_data.append(upsampled_signal)
            new_freqs.append(new_freq)
            new_signal_labels.append(label)
        f.close()

        output_file = os.path.join(self.path, group, file)
        with pyedflib.EdfWriter(output_file, len(new_signal_labels)) as out_f:
            out_f.setStartdatetime(startdatetime)

            # Create channel information for the header
            channel_info = []
            for label, unit, freq, phys_min, phys_max, dig_min, dig_max, transd, prefilt in zip(new_signal_labels, units, new_freqs, physical_min, physical_max, digital_min, digital_max, transducer, prefilter):
                channel_info.append({'label': label, 'dimension': unit, 'sample_rate': freq, 'physical_min': phys_min,
                                     'physical_max': phys_max, 'digital_min': dig_min, 'digital_max': dig_max,
                                     'transducer': transd, 'prefilter': prefilt})

            out_f.setSignalHeaders(channel_info)

            # Determine the number of records (assuming 1 second per record)
            num_records = int(max([len(data) / freq for data, freq in zip(new_data, new_freqs)]))

            # Write each record
            for record in range(num_records):
                for i, data in enumerate(new_data):
                    start_index = int(record * new_freqs[i])
                    end_index = int(start_index + new_freqs[i])
                    record_data = data[start_index:end_index]

                    # Check if the record is shorter than expected (e.g., at the end of the file)
                    if len(record_data) < new_freqs[i]:
                        # Pad the record_data to the expected length with zeros
                        record_data = np.pad(record_data, (0, new_freqs[i] - len(record_data)), 'constant')

                    out_f.writePhysicalSamples(record_data)


if __name__ == '__main__':
    path = '/scratch/users/umaer/Cerebra'
    group = 'Control'
    self = CerebraDataset(path=path)
    group_files = os.listdir(os.path.join(path, group))
    for file in group_files:
        self.resample_signals(file=file, group=group)

    # path = '/scratch/users/umaer/Cerebra'
    # group = 'Control'
    # self = CerebraDataset(path=path)
    # self.transfer_edfs_group(group)
