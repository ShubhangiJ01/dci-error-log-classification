import os
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

DCI_CLASSIFIER_UPLOAD_PATH = '/home/shujain/Downloads/'
DCI_CLASSIFIER_DOWNLOAD_PATH = '/home/shujain/Downloads/'
UPLOAD_DIR_NAME = os.environ.get('DCI_CLASSIFIER_UPLOAD_PATH', '/home/shujain/Downloads/')
DOWNLOAD_DIR_NAME = os.environ.get('DCI_CLASSIFIER_DOWNLOAD_PATH', '/home/shujain/Downloads/')

    
    
