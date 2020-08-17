import os
import time
import argparse
import logging
from elasticsearch import Elasticsearch

tracer = logging.getLogger('elasticsearch')
tracer.setLevel(logging.CRITICAL)

timestr = time.strftime("%Y%m%d-%H%M%S")

DOWNLOAD_DIR_NAME = os.environ.get('DCI_CLASSIFIER_DOWNLOAD_PATH', '/home/shujain/Downloads/')

client = Elasticsearch("http://localhost:9200")
INDEX_NAME = "rule_classifications"

def parse_argument():
    parser = argparse.ArgumentParser(description='DCI error log classification')
    parser.add_argument('task',type=str,choices=['rule-insertion','rule-testing','job-labelling'])
    parser.add_argument('--product',type=str,default="0", help='Product value')
    parser.add_argument('--Error_Type', type=str, default="None",choices=['non DCI','DCI'],help='Error label')
    parser.add_argument('--Job_ID', type=str, default="0", help='Test job id')
    parser.add_argument('--Stage_of_Failure', type=str, default="0",help='Stage_of_Failure')
    parser.add_argument('--Error_Message', type=str, default="0",help='Error content')
    parser.add_argument('--Is_user_text', type=int,choices=[0,1],default=0, help='user_text.yml in failed bucket')
    parser.add_argument('--Is_SUT', type=int,choices=[0,1],default=0, help='SUT.yml in failed bucket')
    parser.add_argument('--Is_install', type=int,choices=[0,1],default=0, help='install.yml in failed bucket')
    parser.add_argument('--Is_logs', type=int,choices=[0,1],default=0, help='logs.yml in failed bucket')
    parser.add_argument('--Is_dci_rhel_cki', type=int,choices=[0,1],default=0, help='Failed task dci-rhel-cki')

    args = parser.parse_args()
    return args
