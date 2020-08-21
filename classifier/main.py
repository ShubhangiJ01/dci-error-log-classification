import argparse
import sys
import logging
import traceback
import os

sys.path.append('../')
from classifier.error_classification_data_load import data_load
from classifier.error_classification_rhel import classifier_rules
from api.main import add_clasification

LOG = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

def main(args):
    if(args['product'] == "rhel"):
        try:
            logging.info('Loading data for RHEL')
            data = data_load()
        except Exception:
            LOG.error(traceback.format_exc())
            sys.exit(1)
        
        try:    
            logging.info('Calling classifier')
            for row in range(len(data)):
                classified_data = classifier_rules(data.loc[row])
                add_clasification(classified_data.loc['Job_ID'], {"error_type":classified_data.loc['Error_Type']})
        except Exception:
            LOG.error(traceback.format_exc())
            sys.exit(1)

    else:
        LOG.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()