
import pandas as pd
import nltk
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import spacy
import en_core_web_sm
from elasticsearch import Elasticsearch
import sys
sys.path.append('../')
from api.main import api_main
import classifier.settings as settings

pd.set_option('mode.chained_assignment', None)
nlp = spacy.load("en_core_web_sm")

client = Elasticsearch("http://localhost:9200")
INDEX_NAME = "rule_classification"

def data_load():
  # file_name = api_main(settings.DOWNLOAD_DIR_NAME)
  # data = pd.read_csv(file_name)
  data = pd.read_csv('jobs_20200729-131646.csv')
  return data

def classifier_rules(data):
  index_exists = client.indices.exists(index=INDEX_NAME)
  
  if index_exists == False:
    print("Index not present")
    sys.exit(1)
  else:
    try:
      data.insert(len(data.columns),"Error_Type","None")
      response = client.search(index=INDEX_NAME)
      for job in range(len(data)):
        if(data.loc[job,'Error_Type']=="None"):
          for hit in response['hits']['hits']:
            if((hit["_source"]['Is_user_text']!=data.loc[job,'Is_user_text.yml'].item())and (hit["_source"]['Is_SUT']!= data.loc[job,'Is_SUT.yml'].item()) and (hit["_source"]['Is_install']!= data.loc[job,'Is_install.yml'].item()) and (hit["_source"]['Is_logs']!=data.loc[job,'Is_logs.yml'].item()) and (hit["_source"]['Is_dci_rhel_cki']!=data.loc[job,'Is_dci_rhel_cki'].item()) ):
              continue
            if((hit["_source"]['Stage_of_Failure']!="0") and (hit["_source"]['Stage_of_failure']!=data.loc[job,'Stage_of_failure'])):
              continue
            if(hit["_source"]['Error_Message'] !="0")and (hit["_source"]['Stage_of_Failure']!=data.loc[job,'Stage_of_Failure']):
              matcher = PhraseMatcher(nlp.vocab)
              message = hit["_source"]['Error_Message']
              matcher.add("gathering_facts", None, nlp(mesage))
              data.loc[job,'Error_Message'] = data.loc[job,'Error_Message'].replace('u\'', '').replace('\'', '')
              doc = nlp(data.loc[job,'Error_Message'])
              matches = matcher(doc)
              if (len(matches) == 0):
                continue
            data.loc[job,'Error_Type'] = hit["_source"]['Error_Type']
            break
    except Exception as err:
      print ("search(index) ERROR", err)
      response = {"error": err}
  
  return data