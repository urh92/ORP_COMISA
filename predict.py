import requests
from datetime import datetime, timedelta
import pandas as pd
import json
from preprocessing import CerebraDataset
import os
import pyedflib
from helper_functions import Helper
import numpy as np

# refresh_token = 'AMf-vBzK16vlAGAyJarjvnteu4IdVHReSINvhsWlkJHRzcpTOZhCwzmEaHd1CUEe9uPcO0TpHzAZNlf-2qtDJVhb31HeNzwoo6m1jLRQLpNfxY08Ki_QzZIYgdylQ7CEW0dCsbFD0Dn2LyH6l4hjL0jjsAehQJE4kvlZWT9mg-rz5NOpcuCvCFM_zGJ6-j6lr7yG6Rey4UgXAddD0sjAKMSpUqRB3eyiUPUUEMGOKQ5mivIAbjG59nM'
# DOMAIN = "https://mysleepscoring-api-staging.cerebramedical.com"
#refresh_token = 'AMf-vBxBqgBhcVKM2FvEyYXbhLpQi_ZWRbgIClmmaOhnUXGRwAgNTVp7M10mw53U6QE8wmjIH6FYd-CS13LqGxfW2bei35T-Al4k62y0_HUukwJbW9cIgSGzlb-SlQpSe0hYPLlAvD84m1Q4mU3GcJHKg4dIgPkZlv-QTy2J3Zv7czUc8frHRT9qAoKdpFXCVjO4JQzHu_DdUYrCWwhc0QBfTdkR9e5kqO6fvCZtRms84_58Z-o7SH8'
refresh_token = 'AMf-vBy47Uad5sjpdgb31I9sdmSZC4EMB_q3f00Hfh6Pn9yKrB-ndA4K8No25nE5SLQGdHegiP9m5r27GmN3tAV1Bfxp5YxxbC__d-JynzwHzBZJPwi5rtWHqmWlXVaw0UX4MInYK1Xepu29Ht-86DN_epycmBkyte9XHZbUyWWWjN0XzLa8szv7kB2EX5uguPCBCES-_kv1AKaS_7epCilnNK5cteVj3NHWdZSF4bsNNDSmb2qML-E'
DOMAIN = "https://mysleepscoring-api.cerebramedical.com"


class ORP:
    def __init__(self, path):
        self.path = path
        self.h = Helper()

    def getAccessToken(self):
        '''
        returns the active bearer token for the user
        '''
        data = {"refresh_token": refresh_token}
        url = f"{DOMAIN}/api/token"

        r = requests.post(url=url, json=data)
        r.raise_for_status()
        result = r.json()['access_token']
        return result

    def getFiles(self, bearer_token):
        '''
        gets files for a user
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/file"

        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        result = r.json()
        return result

    def createStudy(self, data, bearer_token):
        '''
        creates a study object
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/study/"

        r = requests.post(url=url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        return result

    def createFile(self, data, bearer_token):
        '''
        creates a file object
        type = ['Raw EDF','RPSGT Edits']
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/file/"

        r = requests.post(url=url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        return result

    def createChannelMapping(self, data, bearer_token):
        '''
        creates a channel mapping object
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/channelmapping/"

        r = requests.post(url=url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        return result

    def getChannelMappings(self, bearer_token):
        '''
        creates a channel mapping object
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/channelmapping"

        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        result = r.json()
        return result

    def patchFileAndChannelMapping(self, data, file_id, bearer_token):
        '''
        creates the association between a file and a channel mapping object
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/file/{file_id}"

        r = requests.patch(url=url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        return result

    def getFile(self, file_id, bearer_token):
        '''
        get a file object, used to get the scoring run id
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/file/{file_id}"

        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        result = r.json()
        return result

    def patchScoringRun(self, start_epoch, end_epoch, scoringrun_id, bearer_token):
        '''
        creates the association between a file and a channel mapping object
        '''
        data = {"lights_off_epoch": start_epoch, "lights_on_epoch": end_epoch, "prefilter": 1, "collection_system": "Alice G3"}
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/scoringrun/{scoringrun_id}"

        r = requests.patch(url=url, headers=headers, json=data)
        r.raise_for_status()
        result = r.json()
        return result

    def uploadEDF(self, edf_file, presigned_url, bearer_token):
        '''
        upload an edf file to the URL
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        files = {'file': open(edf_file, 'rb')}
        r = requests.post(url=presigned_url, files=files)
        print(f"upload file to gcs status_code:{r.status_code}")
        return r.status_code

    def downloadAutoScoringJson(self, file_id, bearer_token):
        '''
        get the json results for MY Sleep Scoring from Cerebra
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/file/{file_id}/download"

        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        data = r.json()
        return data

    def getScoringRun(self, scoringrun_id, bearer_token):
        '''
        get a file object, used to get the scoring run id
        '''
        headers = {"Authorization": f"Bearer {bearer_token}"}
        url = f"{DOMAIN}/api/scoringrun/{scoringrun_id}"

        r = requests.get(url=url, headers=headers)
        r.raise_for_status()
        result = r.json()
        return result

    def get_lights(self, start_time, duration, df, study_id):
        if start_time.hour == 0 and start_time.minute == 0 and start_time.second == 0:
            start_epoch = 0
            end_epoch = int(duration / 30)
        else:
            lights = df[df['ID'] == int(study_id)][['Lights_Off', 'Lights_On']]

            if lights.size == 0:
                start_epoch = 0
                end_epoch = int(duration / 30)
            else:
                time_format = '%I:%M %p'
                lights_off_time = datetime.strptime(lights['Lights_Off'].item(), time_format).time()
                lights_on_time = datetime.strptime(lights['Lights_On'].item(), time_format).time()

                lights_off = datetime.combine(start_time.date(), lights_off_time)
                lights_on = datetime.combine(start_time.date(), lights_on_time)

                if lights_on < start_time:
                    lights_on += timedelta(days=1)

                time_difference = (lights_on - start_time).seconds
                time_difference2 = (lights_off - start_time).seconds
                if time_difference2 > 30000:
                    time_difference2 = (start_time-lights_off).seconds
                start_epoch = int(time_difference2 / 30)
                end_epoch = int(time_difference / 30)
        return start_epoch, end_epoch

    def get_channel_mappings(self, study_id, f):
        ch_body = {}
        for channel in ['eeg_left', 'eeg_right', 'eye_left', 'eye_right', 'chin', 'ekg', 'resp_cannula',
                        'resp_thermistor', 'resp_chest', 'resp_abdomen', 'oxygen_sat']:
            label, idx = self.h.get_channel_labels(f, channel)
            ch_body[channel] = {'channel_index': idx}

        remove_keys = []
        for key in ch_body.keys():
            if np.isnan(ch_body[key]['channel_index']):
                remove_keys.append(key)

        if len(remove_keys) > 0:
            for key in remove_keys:
                del ch_body[key]

        ch_body['name'] = study_id
        return ch_body

    def get_study_details(self, study_id, token):
        body = {"description": study_id}
        study_details = self.createStudy(body, token)
        return study_details

    def get_file_details(self, study_details, token):
        body = {"name": f"{study_details['id']}.edf", "description": "Baseline PSG", "study_id": study_details['id'], "type": "Raw EDF"}
        file_details = self.createFile(body, token)
        return file_details

    def upload_file(self, group, file):
        study_id = file.split('.')[0]
        f = pyedflib.EdfReader(os.path.join(self.path, group, file))
        start_time, duration, fs, _, _, _, _, _, _, _, _, _ = self.h.get_recording_info(f)
        ch_body = self.get_channel_mappings(study_id, f)
        f.close()
        token = self.getAccessToken()
        study_details = self.get_study_details(study_id, token)
        file_details = self.get_file_details(study_details, token)
        url_val = self.createChannelMapping(ch_body, token)
        body = {"channelmapping_id": url_val['id']}
        file_id = file_details['id']
        url_val = self.patchFileAndChannelMapping(body, file_id, token)
        upload_url = url_val['upload_url']
        file_id_val = file_id
        file_info = self.getFile(file_id_val, token)
        default_scoring_run_id = file_info['scoringruns'][0]['id']
        start_epoch, end_epoch = self.get_lights(start_time, duration, df, study_id)
        _ = self.patchScoringRun(start_epoch, end_epoch, default_scoring_run_id, token)
        file_to_upload = os.path.join(self.path, group, file)
        _ = self.uploadEDF(file_to_upload, upload_url, token)
        return default_scoring_run_id

    def download_file(self, group, file):
        df_codes = pd.read_csv(os.path.join(self.path, group + '_Codes.csv'))
        token = self.getAccessToken()
        download_types = ['Autoscoring Events', 'Report Data']
        scoringrun_id_val = df_codes[df_codes['Files'] == file]['Codes']
        if scoringrun_id_val.size == 0:
            return None
        scoringrun_id_val = scoringrun_id_val.item()
        scoring_run_info = self.getScoringRun(scoringrun_id_val, token)
        if scoring_run_info['status'] == 'Reporting Complete':
            print("Found file")
            for file in scoring_run_info['files']:
                file_id = file['id']
                f_type = file['type']
                file_name = file['study']['description']  # this should be your folder name
                out_file_folder = os.path.join(self.path, group + '_Predictions', file_name)
                if not os.path.exists(out_file_folder):
                    os.mkdir(out_file_folder)
                if file['type'] in ['Autoscoring Events', 'Report Data'] and file['type'] in download_types:
                    print(f'\tfrom {file_name} downloading {f_type}')
                    out_f = os.path.join(out_file_folder, f'{file_name}_{f_type}.json')
                    if not os.path.exists(out_f):
                        my_json = self.downloadAutoScoringJson(file_id, token)
                        with open(out_f, 'w') as out_file:
                            json.dump(my_json, out_file)
        else:
            print("Not found")
            return None


if __name__ == '__main__':
    # path = '/scratch/users/umaer/Cerebra'
    # group = 'Control'
    # dataset = CerebraDataset(path=path)
    # self = ORP(path=path)
    # files = dataset.get_files_group(group, file_type='edfs')
    # files.sort()
    # df = pd.read_csv(os.path.join(path, 'Excel', 'Stages_PSG_all.csv'), low_memory=False)
    # i = 0
    # studies = []
    # codes = []
    # for file in files:
    #     print('Loading {}'.format(i))
    #     i += 1
    #     study_id = file.split('.')[0]
    #     if os.path.exists(os.path.join(path, group + '_Predictions', study_id)):
    #         continue
    #     default_scoring_run_id = self.upload_file(group, file)
    #     studies.append(study_id)
    #     codes.append(default_scoring_run_id)
    # df_codes = pd.DataFrame({'Files': studies, 'Codes': codes})
    # df_codes.to_csv(os.path.join(path, group + '_Codes.csv'), index=False)

    path = '/scratch/users/umaer/Cerebra'
    group = 'Control'
    dataset = CerebraDataset(path=path)
    self = ORP(path=path)
    df_codes = pd.read_csv(os.path.join(path, group + '_Codes.csv'))
    files = df_codes['Files'].tolist()
    for file in files:
        self.download_file(group, file)
