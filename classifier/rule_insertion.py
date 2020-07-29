import sys
import logging
import argparse
import traceback
from elasticsearch import Elasticsearch
from rule_creation import create_new_rule
import requests

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def database_insertion(Stage_of_failure,Col_val,Error_Message,Error_Type):
    client = Elasticsearch("http://localhost:9200")

    rule={
        "Stage_of_failure": sys.argv[1],
        "Column_Val = 1": sys.argv[2],
        "Error_Message": sys.argv[3],
        "Error_Type": sys.argv[4]
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
    parser.add_argument('Stage_of_failure', type=str, help='Stage_of_failure')
    parser.add_argument('Column_Val', type=str, help='column value equal to 1')
    parser.add_argument('Error_Message', type=str, help='Error content')
    parser.add_argument('Error_Type', type=str, choices=['non DCI','DCI'],help='Error label')
    parser.add_argument('Job_id', type=str, help='Test job id')
    args = parser.parse_args()
    
    Stage_of_failure = args.Stage_of_failure
    Column_Val = args.Column_Val
    Error_Message = args.Error_Message
    Error_Type = args.Error_Type
    Job_id = args.Job_id
        
    try:
        logging.info('Creating new rule')
        create_new_rule(Stage_of_failure,Column_Val,Error_Message,Job_id)
    except Exception:
        LOG.error(traceback.format_exc())
        sys.exit(1)
    logging.info('Entering database insertion ')
    database_insertion(Stage_of_failure,Column_Val,Error_Message,Error_Type)

if __name__ == "__main__":
    main()
