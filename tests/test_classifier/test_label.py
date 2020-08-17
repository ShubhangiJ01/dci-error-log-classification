from classifier.error_classification_rhel import classifier_rules

def test_user_text_yml(test_data):
    result = classifier_rules(test_data.loc[0]) 
    assert result.loc['Error_Type'] == "non DCI"

def test_pre_run_hook_failure(test_data):
    result = classifier_rules(test_data.loc[1]) 
    assert result.loc['Error_Type'] == "non DCI"
    
def test_sut_beaker_server(test_data):
    result = classifier_rules(test_data.loc[2]) 
    assert result.loc['Error_Type'] == "non DCI"

def test_sut_undefined_variable(test_data):
    result = classifier_rules(test_data.loc[3]) 
    assert result.loc['Error_Type'] == "non DCI"

def test_dci_rhel_step(test_data):
    result = classifier_rules(test_data.loc[4]) 
    assert result.loc['Error_Type'] == "DCI"

def test_gathering_fact_step(test_data):
    result = classifier_rules(test_data.loc[5]) 
    assert result.loc['Error_Type'] == "DCI"

def test_install_yml(test_data):
    result = classifier_rules(test_data.loc[6]) 
    assert result.loc['Error_Type'] == "DCI"

def test_sut_http_error(test_data):
    result = classifier_rules(test_data.loc[7]) 
    assert result.loc['Error_Type'] == "non DCI"

def test_logs_yml(test_data):
    result = classifier_rules(test_data.loc[8]) 
    assert result.loc['Error_Type'] == "non DCI"
