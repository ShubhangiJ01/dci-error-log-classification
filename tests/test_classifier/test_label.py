from tests.conftest import test_data
from classifier.error_classification_rhel import classifier_rules

def test_user_text_yml():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[0,'Error_Type'] == "non DCI"

def test_pre_run_hook_failure():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[1,'Error_Type'] == "non DCI"
    
def test_sut_beaker_server():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[2,'Error_Type'] == "non DCI"

def test_sut_undefined_variable():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[3,'Error_Type'] == "non DCI"

def test_dci_rhel_step():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[4,'Error_Type'] == "DCI"

def test_gathering_fact_step():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[5,'Error_Type'] == "DCI"

def test_install_yml():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[6,'Error_Type'] == "DCI"

def test_sut_http_error():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[7,'Error_Type'] == "non DCI"

def test_logs_yml():
    data = test_data()
    result = classifier_rules(data) 
    assert result.loc[8,'Error_Type'] == "non DCI"
