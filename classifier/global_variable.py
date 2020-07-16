import os
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

os.environ['download_path'] = "/home/shujain/Downloads/"
os.environ['upload_path'] = "/home/shujain/Downloads/"
upload_dir_name = os.environ.get('upload_path')
download_dir_name = os.environ.get('download_path')
    
    
