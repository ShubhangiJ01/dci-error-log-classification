import pytest
import pandas as pd
import os

test_data_job = '%s/%s' % (os.path.dirname(os.path.abspath(__file__)),
                             'test_classifier/classifier_labels_data.csv')
@pytest.fixture
def test_data():
  data = pd.read_csv(test_data_job)
  return data

