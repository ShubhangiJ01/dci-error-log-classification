import pandas as pd
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


def create_new_rule(Stage_of_failure,Col_val,Error_message,Job_id):
    data = test_data(Job_id)
    matcher = PhraseMatcher(nlp.vocab)
        
    if (Stage_of_failure!="0"):
        if(Error_message !="0"):
            message = Error_message
            matcher.add("temp", None, nlp(message))
            data['Error_Message'][0] = data['Error_Message'][0].replace('u\'', '').replace('\'', '')
            doc = nlp(data['Error_Message'][0])
            matches = matcher(doc)
            if (len(matches) > 0):
                print("Success")
            else:
                logging.info('Error message not matching')
                sys.exit(1)
        else:
            if(data['Stage_of_Failure'][0] == Stage_of_failure):
                print("Success")
            else:
                logging.info('Failure stage not matching')
                sys.exit(1)
    
    if(Col_val!="0"):
        if(data[Col_val][0]==1):
            if(Error_message !="0"):
                message = Error_message
                matcher.add("temp", None, nlp(message))
                data['Error_Message'][0] = data['Error_Message'][0].replace('u\'', '').replace('\'', '')
                print(data['Error_Message'][0])
                doc = nlp(data['Error_Message'][0])
                matches = matcher(doc)
                if (len(matches) > 0):
                    print("Success")
                
                else:
                    logging.info('Error message not matching')
                    sys.exit(1)
            else:
                print("Success")

