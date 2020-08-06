import argparse
import sys
import logging
import traceback
import os
from classifier.error_classification_rhel import data_load
from classifier.error_classification_rhel import classifier_rules
from classifier.json_generator import classification_storage

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def main(args):
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

    else:
        LOG.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()