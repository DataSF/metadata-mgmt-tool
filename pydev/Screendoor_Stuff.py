# coding: utf-8
from __future__ import division
from ConfigUtils import *
from Utils import *
import pycurl
import requests
from io import BytesIO
import json
from Wkbk_Json import *



class ScreenDoorStuff:
    '''class to handle screen door stuff'''
    def __init__(self, configItems):
        self._config_dir =  configItems['config_dir']
        self._screendoor_config_file = configItems['screendoor_config_file']
        self._screendoor_configs = ConfigUtils.setConfigs(self._config_dir, self._screendoor_config_file)
        self._api_key = self._screendoor_configs['api_key']
        self._projectid = str(self._screendoor_configs['projectid'])
        self._responses_url = self.set_responsesUrl()
        self._attachment_url = self._screendoor_configs['attachment_url']
        self._responses = self.set_reponses()
        self._pickle_dir = configItems['pickle_dir']
        self._wkbk_uploads_dir = self._screendoor_configs['wkbk_uploads_dir']
        self._files_to_download = self.set_FileInfo()
        self._wkbk_uploads_json_fn = self._screendoor_configs['wkbk_uploads_json_fn']
        #self._current_date = datetime.datetime.now().strftime("%Y_%m_%d_")
        self._current_date = DateUtils.get_current_date_year_month_day()


    def set_responsesUrl(self):
        responses_url = self._screendoor_configs['responses_url']
        responses_url =  responses_url % (self._projectid,self._api_key)
        return responses_url

    def set_reponses(self):
        responses = ""
        # set the per page for screendoor, max is 100
        per_page = 100
        try:
            r = requests.get(self._responses_url + '&per_page=' + str(per_page))
            num_records = int(r.headers['total'])
            num_pages = math.ceil(num_records/per_page)
            responses = r.json()
            for page in range(2, num_pages + 1):
                r = requests.get(self._responses_url + '&per_page=' + str(per_page) + '&page=' + str(page))
                responses = responses + r.json()
        except Exception, e:
            print str(e)
        return responses

    def set_FileInfo(self):
        files_to_download = []
        for response in self._responses:
            #print "********"
            #print response
            #print response.keys()
            submitted_dt =  response['submitted_at']
            response_items =  response['responses'].keys()
            #print response_items
            for item in response_items:
              response_file_dictList = response['responses'][item]
              #print response_file_dictList
              if isinstance(response_file_dictList, list):
                for file_info in response_file_dictList:
                    #print file_info
                    file_info['submitted_at'] = response['submitted_at']
                    files_to_download.append(file_info)
        print "*****downloading " + str(len(files_to_download)) +" files from screendoor*****"
        return files_to_download

    def setDownloadUrl(self, fileId):
        return self._attachment_url % (fileId)

    def getAttachment(self, fileId, filename):
        '''downloads an attachment from screen door using the fileid and filename'''
        #equivelent to: curl -L "https://screendoor.dobt.co/attachments/s5wflD750Nxhai9MfNmxes4TR-0xoDyw/download" > whateverFilename.csv
        # As long as the file is opened in binary mode, can write response body to it without decoding.
        download_url = self.setDownloadUrl(fileId)
        downloaded = False
        try:
            with open(self._wkbk_uploads_dir + filename, 'wb') as f:
                c = pycurl.Curl()
                c.setopt(c.URL, download_url)
                # Follow redirect.
                c.setopt(c.FOLLOWLOCATION, True)
                c.setopt(c.WRITEDATA, f)
                c.perform()
                c.close()
                downloaded = True
        except Exception, e:
            print str(e)
        return downloaded


    def get_attachments(self):
        '''downloads a list of files'''
        downloaded_files = { "uploaded_workbooks": []}
        #remove any existing files in the dir
        remove_files = FileUtils.remove_files_on_regex(self._wkbk_uploads_dir, "*.xlsx")
        for file in self._files_to_download:
            downloaded_files[ "uploaded_workbooks"].append( { 'file_name': file['id']+"_"+file['filename'], 'downloaded': self.getAttachment(file['id'], file['id']+"_"+file['filename']), 'submitted_at': file['submitted_at']})
        number_of_wkbks_to_load = len(downloaded_files[ "uploaded_workbooks"])
        wrote_file = WkbkJson.write_json_object(downloaded_files, self._pickle_dir, self._wkbk_uploads_json_fn)
        return wrote_file,number_of_wkbks_to_load



if __name__ == "__main__":
    main()
