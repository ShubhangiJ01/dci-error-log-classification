import pytest
import pandas as pd

def test_data():
  data = pd.read_csv('/home/shujain/Downloads/jobs_20200720-164946.csv')
  data.insert(len(data.columns),"Pre_Run_hook",0)
  data.insert(len(data.columns),"SUT_beaker_server",0)
  data.insert(len(data.columns),"SUT_undefined",0)
  data.insert(len(data.columns),"dci_rhel_cki_failure_step",0)
  data.insert(len(data.columns),"Installation_failure",0)
  data.insert(len(data.columns),"SUT_HTTP_Error",0)
  data.insert(len(data.columns),"logs_parsing_error",0)
  data.insert(len(data.columns),"install_no_distro_match",0)
  data.insert(len(data.columns),"Error_Type","None")
  return data

