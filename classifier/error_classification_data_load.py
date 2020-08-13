import pandas as pd
from api.main import api_main
import classifier.settings as settings

def data_load():
  file_name = api_main(settings.DOWNLOAD_DIR_NAME)
  data = pd.read_csv(file_name)
  return data