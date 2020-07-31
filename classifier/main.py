import argparse
import sys
import logging
import traceback
import os
from error_classification_rhel import data_load
from error_classification_rhel import classifier_rules
from json_generator import classification_storage

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='DCI error log classification')
    parser.add_argument('product',type=str, help='Product value')
    args = parser.parse_args()
    
    if(args.product == "rhel"):
        try:
            logging.info('Loading data for RHEL')
            data = data_load()
        except Exception:
            LOG.error(traceback.format_exc())
            sys.exit(1)
        
        try:    
            logging.info('Calling classifier')
            classified_data = classifier_rules(data)
        except Exception:
            LOG.error(traceback.format_exc())
            sys.exit(1)

        try:
            logging.info('Writing labeled data in a json file')
            classification_storage(classified_data)
        except Exception:
            LOG.error(traceback.format_exc())
            sys.exit(1)
    else:
        LOG.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()