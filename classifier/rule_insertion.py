import sys
import logging
import argparse
import traceback
from elasticsearch import Elasticsearch
from rule_creation import create_new_rule
import requests

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def database_insertion(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_Message,Error_Type):
    client = Elasticsearch("http://localhost:9200")

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

    INDEX_NAME = "rule_classification"
    client.index(index=INDEX_NAME,body=rule)
    client.indices.refresh(index=INDEX_NAME)

    index_exists = client.indices.exists(index=INDEX_NAME)

    if index_exists == False:
        print("Index not created")
        sys.exit(1)
    else:
        try:
            response = client.search(index=INDEX_NAME)
            for hit in response['hits']['hits']:
                print(hit["_source"])

        except Exception as err:
            print ("search(index) ERROR", err)
            response = {"error": err}
        
def main():
    
    parser = argparse.ArgumentParser(description='New rule creation')

    parser.add_argument('Error_Type', type=str, choices=['non DCI','DCI'],help='Error label')
    parser.add_argument('Job_ID', type=str, help='Test job id')
    parser.add_argument('--Stage_of_Failure', type=str, default="0",help='Stage_of_Failure')
    parser.add_argument('--Error_Message', type=str, default="0",help='Error content')
    parser.add_argument('--Is_user_text', type=int,choices=[0,1],default=0, help='user_text.yml in failed bucket')
    parser.add_argument('--Is_SUT', type=int,choices=[0,1],default=0, help='SUT.yml in failed bucket')
    parser.add_argument('--Is_install', type=int,choices=[0,1],default=0, help='install.yml in failed bucket')
    parser.add_argument('--Is_logs', type=int,choices=[0,1],default=0, help='logs.yml in failed bucket')
    parser.add_argument('--Is_dci_rhel_cki', type=int,choices=[0,1],default=0, help='Failed task dci-rhel-cki')
    args = parser.parse_args()
    
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
        logging.info('Creating new rule')
        create_new_rule(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_Message,Job_ID)
    except Exception:
        LOG.error(traceback.format_exc())
        sys.exit(1)
    logging.info('Entering database insertion')
    database_insertion(Stage_of_Failure,Is_user_text,Is_SUT,Is_install,Is_logs,Is_dci_rhel_cki,Error_Message,Error_Type)

if __name__ == "__main__":
    main()
