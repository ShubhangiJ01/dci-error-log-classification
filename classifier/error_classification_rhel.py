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
import classifier.settings as settings

pd.set_option('mode.chained_assignment', None)
nlp = spacy.load("en_core_web_sm")

def classifier_rules(data):
  index_exists = settings.client.indices.exists(index=settings.INDEX_NAME)
  
  if index_exists == False:
    logging.exception("No rule to match: Database not found")
    sys.exit(1)
  else:
    try:
      rules = settings.client.search(index=settings.INDEX_NAME)
      count = settings.client.count(index=settings.INDEX_NAME)['count']
      if(count > 0):
        if(data.loc['Error_Type']=="None"):
          for rule in rules['hits']['hits']:
              if((rule["_source"]['Is_user_text']!=data.loc['Is_user_text.yml'].item()) or (rule["_source"]['Is_SUT']!= data.loc['Is_SUT.yml'].item()) or (rule["_source"]['Is_install']!= data.loc['Is_install.yml'].item()) or (rule["_source"]['Is_logs']!=data.loc['Is_logs.yml'].item()) or (rule["_source"]['Is_dci_rhel_cki']!=data.loc['Is_dci_rhel_cki'].item()) ):
                continue
              
              if((rule["_source"]['Stage_of_Failure']!="0") and (rule["_source"]['Stage_of_Failure']!=data.loc['Stage_of_Failure'])):
                continue
              
              if(rule["_source"]['Error_Message'] !="0"):
                matcher = PhraseMatcher(nlp.vocab)
                message = rule["_source"]['Error_Message']
                matcher.add("gathering_facts", None, nlp(message))
                data.loc['Error_Message'] = data.loc['Error_Message'].replace('u\'', '').replace('\'', '')
                doc = nlp(data.loc['Error_Message'])
                matches = matcher(doc)
                if (len(matches) == 0):
                  continue
                  
              data.loc['Error_Type'] = rule["_source"]['Error_Type']
              break
      else:
          logging.exception("No rule to match: Database is empty")
          sys.exit(1)
    except Exception as err:
      logging.error(traceback.format_exc())
      sys.exit(1)
  
  return data