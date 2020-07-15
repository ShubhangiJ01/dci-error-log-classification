
import pandas as pd
import nltk
import csv
import sys
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import spacy
import en_core_web_sm
import argparse
import logging
import os
import sys
import traceback
import time
sys.path.append('../')


from api.main import api_main

os.environ['download_path'] = "/home/shujain/Downloads/"
os.environ['upload_path'] = "/home/shujain/Downloads/"

pd.set_option('mode.chained_assignment', None)
LOG = logging.getLogger(__name__)
#LOG.setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.INFO)

nlp = spacy.load("en_core_web_sm")
timestr = time.strftime("%Y%m%d-%H%M%S")
download_dir_name = os.environ.get('download_path')
upload_dir_name = os.environ.get('upload_path')


def data_load():
  file_name = api_main(download_dir_name)
  data = pd.read_csv(file_name)
  #data = pd.read_csv('/home/shujain/Downloads/jobs_7_6_2020_red_hat4.csv')
  return data

def feature_generation(data):
  data.insert(len(data.columns),"Pre_Run_hook",0)
  data.insert(len(data.columns),"SUT_beaker_server",0)
  data.insert(len(data.columns),"SUT_undefined",0)
  data.insert(len(data.columns),"dci_rhel_cki_failure_step",0)
  data.insert(len(data.columns),"Installation_failure",0)
  data.insert(len(data.columns),"SUT_HTTP_Error",0)
  data.insert(len(data.columns),"logs_parsing_error",0)
  data.insert(len(data.columns),"install_no_distro_match",0)
  data.insert(len(data.columns),"Error_Type","None")
  return data

def classifier_rules(data):
  for row in range(len(data)):
    matcher = PhraseMatcher(nlp.vocab)
    if(data.loc[row,'Stage of Failure'] == 'Run the pre-run hook'):
      data['Pre_Run_hook'][row] = 1
      data['Error_Type'][row] = "non DCI"

    elif(data['Is_SUT.yml'][row]==1):
      matcher.add("beaker server", None, nlp("'ansible_host': u'beaker_server'"))
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['SUT_beaker_server'][row] = 1
        data['Error_Type'][row] = "non DCI"
        

    elif(data['Is_SUT.yml'][row]==1):
      matcher.add("undefined_variable", None, nlp("undefined variable"))
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['SUT_undefined'][row] = 1
        data['Error_Type'][row] = "non DCI"
        
    
    elif(data['Stage of Failure'][row] in ('Gathering Facts','Wait system to be installed')):
      matcher.add("gathering_facts", None, nlp("/distribution/check-install"))
      data['Error Message'][row] = data['Error Message'][row].replace('u\'', '').replace('\'', '')
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['Installation_failure'][row] = 1
        data['Error_Type'][row] = "DCI"
        
    elif(data['Stage of Failure'][row] =='Get SUT details'):
      matcher.add("SUT_HTTP_Error", None, nlp("HTTP error"))
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['SUT_HTTP_Error'][row] = 1
        data['Error_Type'][row] = "non DCI"
        
    elif(data['Is_logs.yml'][row] ==1):
      matcher.add("logs_parsing_error", None, nlp("An error while parsing the output occured"))
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['logs_parsing_error'][row] = 1
        data['Error_Type'][row] = "non DCI"
        
    elif(data['Is_install.yml'][row] ==1):
      matcher.add("install_no_distro_match", None, nlp("distro tree matches"))
      data['Error_Type'][row] = "DCI"
      doc = nlp(data['Error Message'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['install_no_distro_match'][row] = 1
        data['Error_Type'][row] = "DCI"
        
    else:
      matcher.add("dci_rhel_cki_failure_step", None, nlp("dci-rhel-cki"))
      doc = nlp(data['Stage of Failure'][row])
      matches = matcher(doc)
      if (len(matches) > 0):
        data['dci_rhel_cki_failure_step'][row] = 1
        data['Error_Type'][row] = "DCI"
        
  return data

def classification_storage(data):
  data_json = data.loc[:,['Job ID', 'Error_Type' ]]
  upload_file_name = upload_dir_name + "Label_Rhel_" + timestr + ".json"
  data_json.to_json(upload_file_name)
