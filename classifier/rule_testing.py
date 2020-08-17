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

def test_new_rule(args):
    
    Stage_of_Failure = args['Stage_of_Failure']
    Error_Message = args['Error_Message']
    Job_ID = args['Job_ID']
    Is_user_text = args['Is_user_text']
    Is_SUT = args['Is_SUT']
    Is_install = args['Is_install']
    Is_logs = args['Is_logs']
    Is_dci_rhel_cki = args['Is_dci_rhel_cki']
    
    if(Job_ID == "0"):
        LOG.exception("No Job id passed to test the rule")
        sys.exit(1)
    
    data = test_data(Job_ID)
    matcher = PhraseMatcher(nlp.vocab)
    
    if((Is_user_text==data.loc[0,'Is_user_text.yml']) and (Is_SUT== data.loc[0,'Is_SUT.yml']) and (Is_install== data.loc[0,'Is_install.yml']) and (Is_logs==data.loc[0,'Is_logs.yml']) and (Is_install== data.loc[0,'Is_install.yml']) and (Is_dci_rhel_cki== data.loc[0,'Is_dci_rhel_cki'])):
        if(Stage_of_Failure!="0"):
            if(data.loc[0,'Stage_of_Failure'] == Stage_of_Failure):
                if(Error_Message !="0"):
                    message = Error_Message
                    matcher.add("temp", None, nlp(message))
                    data['Error_Message'][0] = data['Error_Message'][0].replace('u\'', '').replace('\'', '')
                    doc = nlp(data['Error_Message'][0])
                    matches = matcher(doc)
                    if (len(matches) > 0):
                        print("Doing fine")
                    else:
                        LOG.exception('Error message not matching')
                        sys.exit(1)
            else:
                LOG.exception('Failure stage not matching')
                sys.exit(1)

        if(Error_Message !="0"):
            message = Error_Message
            matcher.add("temp", None, nlp(message))
            data['Error_Message'][0] = data['Error_Message'][0].replace('u\'', '').replace('\'', '')
            doc = nlp(data['Error_Message'][0])
            matches = matcher(doc)
            if (len(matches) > 0):
                print("Doing fine")
            else:
                LOG.exception('Error message not matching')
                sys.exit(1)
    else:
        LOG.exception('Incorrect Rule')
        sys.exit(1)

    print("Success")