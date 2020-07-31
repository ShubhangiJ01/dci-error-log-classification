import pandas as pd
import numpy as np
import logging
import traceback
import nltk
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher
import spacy
import en_core_web_sm
import sys
sys.path.append('../')
from api.main import test_data

pd.set_option('mode.chained_assignment', None)
nlp = spacy.load("en_core_web_sm")

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def create_new_rule(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_message,Job_ID):
    #data = test_data(Job_ID)
    data = pd.read_csv('jobs_20200729-131646.csv')
    matcher = PhraseMatcher(nlp.vocab)
    
    if((Is_user_text==data.loc[0,'Is_user_text.yml']) and (Is_SUT== data.loc[0,'Is_SUT.yml']) and (Is_install== data.loc[0,'Is_install.yml']) and (Is_logs==data.loc[0,'Is_logs.yml']) and (Is_install== data.loc[0,'Is_install.yml']) and (Is_dci_rhel_cki== data.loc[0,'Is_dci_rhel_cki'])):
        if(Stage_of_Failure!="0"):
            if(data[0,'Stage_of_Failure'] == Stage_of_Failure):
                if(Error_message !="0"):
                    message = Error_message
                    matcher.add("temp", None, nlp(message))
                    data['Error_Message'][0] = data['Error_Message'][0].replace('u\'', '').replace('\'', '')
                    doc = nlp(data['Error_Message'][0])
                    matches = matcher(doc)
                    if (len(matches) > 0):
                        print("Doing fine")
                    else:
                        logging.info('Error message not matching')
                        sys.exit(1)
            else:
                logging.info('Failure stage not matching')
                sys.exit(1)
    else:
        logging.info('Incorrect Rule')
        sys.exit(1)

    print("Success")