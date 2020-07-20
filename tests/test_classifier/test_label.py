from tests.conftest import test_data
from classifier.error_classification_rhel import classifier_rules

def test_pre_run_hook_failure():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[0,'Error_Type'] == "non DCI"
    
def test_SUT_beaker_server():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[1,'Error_Type'] == "non DCI"

def test_SUT_undefined_variable():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[2,'Error_Type'] == "non DCI"