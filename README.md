# Distributed CI Error Classifier

![](https://img.shields.io/badge/license-Apache2.0-blue.svg?style=flat) ![](https://img.shields.io/badge/python-2.7,3.5-green.svg?style=flat) ![](https://img.shields.io/badge/elasticsearch-7.8.0-red.svg?style=flat) ![](https://img.shields.io/badge/Flask-1.1.2-orange.svg?style=flat)

## Table of Contents

- [Objective](#objective)
- [Installation](#installation)
- [Configuration](#configuration)
- [Classifier](#classifier)
- [Rules table Schema](#rulestableschema)
- [New Rule creation](#newrulecreation)
- [Testing new rule](#testingnewrule)
- [Search existing rules](#searchexistingrules)

# Objective

In the current setup when a job fails we don’t know if it failed because of DCI issue or issue is at partners end. As test cases are executed at partners end, error can be specifically caused because of issues in partners systems or networks. All these jobs have to be first checked by an RH developer and based on the error it is decided if it is an RH issue or partner issue.

To save time, we build an error log classification model using machine learning and NLP techniques . This model reads the job data and automatically classifies the failed log into DCI or non DCI. Once the job is classified, RH resources have to invest time only for jobs which are marked as DCI error type and all other jobs are redirected to corresponding partners.

## Installation

- clone this repository

- use the package manager [pip](https://pip.pypa.io/en/stable/) to install dciclient:
```console
$ pip install python-dciclient
```
The package provides the API: a python module one can use to interact with a control server (`dciclient.v1.api.*`)

## Configuration

### Remoteci creation

DCI is connected to the Red Hat SSO. You need to log in `https://www.distributed-ci.io` with your redhat.com SSO account. Your user account will be created in our database the first time you connect.

After the first connection you can create a remoteci. Go to [https://www.distributed-ci.io/remotecis](https://www.distributed-ci.io/remotecis) and click `Create a new remoteci` button. Once your `remoteci` is created, you can retrieve the connection information in the `Authentication` column. Save this information in `remoteci.rc` file.

At this point, you can validate your credentials with the following commands:

```console
$ source remoteci.rc
```

If you see your remoteci in the list, everything is working great so far.

## Classifier

The classifier is built using a rule based system in NLP. Rules are stored in the elasticsearch database. Below is the pipeline for the model development.  
<img src="DCI_Classifier_Model.png" width="950" height="400">

To run the classifier: 
```console
$ dci-classifier job-labelling --product="<product_name>"
```

## Rule table schema:

'Error_Type', type=str, default="None",choices=['non DCI','DCI'],help='Error label'  
'Job_ID', type=str, default="0", help='Test job id'  
'Stage_of_Failure', type=str, default="0",help='Task name at which job failed'  
'Error_Message', type=str, default="0",help='Error content'  
'Is_user_text', type=int,choices=[0,1],default=0, help='user_text.yml in failed bucket'  
'Is_SUT', type=int,choices=[0,1],default=0, help='SUT.yml in failed bucket'  
'Is_install', type=int,choices=[0,1],default=0, help='install.yml in failed bucket'  
'Is_logs', type=int,choices=[0,1],default=0, help='logs.yml in failed bucket'  
'Is_dci_rhel_cki', type=int,choices=[0,1],default=0, help='Failed task dci-rhel-cki'  

## New rule creation

Flask API is created to create new rule. Entry point for the new rule creation is app.py @app.route('/rules', methods=['POST'])  
To create new rule, run the API : 
```console
http POST http://0.0.0.0:1234/rules <parameter_1="value>-----<parameter_n="value">  
```
New rule can be created using CLI as well :  
```console
dci-classifier rule-insertion <parameter_1="value>-----<parameter_n="value">  
```  
Sample for parameters in above command:  
Stage_of_Failure = "Run the pre-run hook"   
Error_Type = "non DCI"   
Is_SUT = "1"  

## Testing new rule

Entry point for the rule testing is app.py @app.route('/rules/test', methods=['POST'])  
Command to test the rule : 
```console
http POST http://0.0.0.0:1234/rules/test <parameter_1="value>-----<parameter_n="value">  
```  
Through CLI :
```console
dci-classifier rule-testing <parameter_1="value>-----<parameter_n="value">  
```  
Parameters should be corresponding to the job id passed for testing the rule. 

## Search existing rules

Entry point for the getting list of all rules present in database is app.py @app.route('/rules', methods=['GET'])  
Command to search the rule : 
```console
http GET http://0.0.0.0:1234/rules
```
## License  
Apache 2.0
