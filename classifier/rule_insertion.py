import sys
import logging
import argparse
import traceback
import classifier.settings as settings
from classifier.rule_testing import test_new_rule


LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def database_insertion(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_Message,Error_Type):
    
    rule={
        "Stage_of_Failure": Stage_of_Failure,
        "Error_Message": Error_Message,
        "Error_Type": Error_Type,
        "Is_user_text": Is_user_text,
        "Is_SUT": Is_SUT,
        "Is_install": Is_install,
        "Is_logs": Is_logs,
        "Is_dci_rhel_cki" : Is_dci_rhel_cki
    }

    index_exists = settings.client.indices.exists(index=settings.INDEX_NAME)
    settings.client.index(index=settings.INDEX_NAME,body=rule)
    settings.client.indices.refresh(index=settings.INDEX_NAME)
    
    if index_exists == False:
        logging.info("Index not created")
        sys.exit(1)
    else:
        try:
            response = settings.client.search(index=settings.INDEX_NAME)
        except Exception as err:
            print ("search(index) ERROR", err)
        
def main(args):
    
    Stage_of_Failure = args.Stage_of_Failure
    Error_Message = args.Error_Message
    Error_Type = args.Error_Type
    Job_ID = args.Job_ID
    Is_user_text = args.Is_user_text
    Is_SUT = args.Is_SUT
    Is_install = args.Is_install
    Is_logs = args.Is_logs
    Is_dci_rhel_cki = args.Is_dci_rhel_cki 
        
    try:
        logging.info('Testing new rule')
        test_new_rule(args)
    except Exception:
        LOG.error(traceback.format_exc())
        sys.exit(1)
    try:
        logging.info('Entering database insertion')
        database_insertion(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_Message,Error_Type)
    except Exception:
        LOG.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
