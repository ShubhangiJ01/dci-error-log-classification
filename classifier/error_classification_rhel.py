
import pandas as pd
import nltk
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import spacy
import en_core_web_sm
from elasticsearch import Elasticsearch
import sys
import logging
import traceback
sys.path.append('../')
from api.main import api_main
from api.main import add_clasification
import classifier.settings as settings


pd.set_option('mode.chained_assignment', None)
nlp = spacy.load("en_core_web_sm")
LOG = logging.getLogger(__name__)

def data_load():
  file_name = api_main(settings.DOWNLOAD_DIR_NAME)
  data = pd.read_csv(file_name)
  return data

def classifier_rules(data):
  index_exists = settings.client.indices.exists(index=settings.INDEX_NAME)
  
  if index_exists == False:
    LOG.exception("No rule to match: Database not found")
    sys.exit(1)
  else:
    try:
      rules = settings.client.search(index=settings.INDEX_NAME)
      count = settings.client.count(index=settings.INDEX_NAME)['count']
      if(count > 0):
        for job in range(len(data)):
          if(data.loc[job,'Error_Type']=="None"):
            for rule in rules['hits']['hits']:
              if((rule["_source"]['Is_user_text']!=data.loc[job,'Is_user_text.yml'].item())and (rule["_source"]['Is_SUT']!= data.loc[job,'Is_SUT.yml'].item()) and (rule["_source"]['Is_install']!= data.loc[job,'Is_install.yml'].item()) and (rule["_source"]['Is_logs']!=data.loc[job,'Is_logs.yml'].item()) and (rule["_source"]['Is_dci_rhel_cki']!=data.loc[job,'Is_dci_rhel_cki'].item()) ):
                continue
              
              if((rule["_source"]['Stage_of_Failure']!="0") and (rule["_source"]['Stage_of_Failure']!=data.loc[job,'Stage_of_Failure'])):
                continue
              
              if(rule["_source"]['Error_Message'] !="0"):
                matcher = PhraseMatcher(nlp.vocab)
                message = rule["_source"]['Error_Message']
                matcher.add("gathering_facts", None, nlp(mesage))
                data.loc[job,'Error_Message'] = data.loc[job,'Error_Message'].replace('u\'', '').replace('\'', '')
                doc = nlp(data.loc[job,'Error_Message'])
                matches = matcher(doc)
                if (len(matches) == 0):
                  continue
              
              data.loc[job,'Error_Type'] = rule["_source"]['Error_Type']
              add_clasification(data.loc[job,'Job_ID'], {"error_type":data.loc[job,'Error_Type']})
              break
      else:
          LOG.exception("No rule to match: Database is empty")
          sys.exit(1)
    except Exception as err:
      LOG.error(traceback.format_exc())
      sys.exit(1)
  
  return data