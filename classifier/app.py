import json
import logging
import traceback
import flask
import sys
from flask import Flask
from flask import request
import argparse
from flask_restful import reqparse

sys.path.append('../')
from classifier.search_rules import all_rules
from classifier.rule_insertion import main
from classifier.rule_testing import test_new_rule

app = Flask(__name__)

def arguments():

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('Error_Type', type=str, default="None",choices=['non DCI','DCI'],help='Error label')
    parser.add_argument('Job_ID', type=str, default="0")
    parser.add_argument('Stage_of_Failure', type=str, default="0",help='Stage_of_Failure')
    parser.add_argument('Error_Message', type=str, default="0",help='Error content')
    parser.add_argument('Is_user_text', type=int,choices=[0,1],default=0, help='user_text.yml in failed bucket')
    parser.add_argument('Is_SUT', type=int,choices=[0,1],default=0, help='SUT.yml in failed bucket')
    parser.add_argument('Is_install', type=int,choices=[0,1],default=0, help='install.yml in failed bucket')
    parser.add_argument('Is_logs', type=int,choices=[0,1],default=0, help='logs.yml in failed bucket')
    parser.add_argument('Is_dci_rhel_cki', type=int,choices=[0,1],default=0, help='Failed task dci-rhel-cki')

    arg = parser.parse_args()
    return arg

@app.route('/rules', methods=['GET'])
def show_all_rules():
    rules,flag = all_rules()
    
    if(flag == False):
        return flask.Response(json.dumps(rules), 400, content_type='application/json')
    else:
        return flask.Response(json.dumps(rules), 200, content_type='application/json')


@app.route('/rules', methods=['POST'])
def create_new_rule():
    args = arguments()
    try:
        response,flag=main(args)
        res = flask.request.json
        if(flag == False):
            return flask.Response(json.dumps(response), 400, content_type='application/json')  
        else:
            return flask.Response(json.dumps(res), 201, content_type='application/json')
        
    except Exception as err:
        return flask.Response({"message": "Rule creation failed"}, 400, content_type='application/json')

@app.route('/rules/test', methods=['POST'])
def test_rule():
    args = arguments()
    try:
        response,flag = test_new_rule(args)
        if (flag == False):
            return flask.Response(json.dumps(response), 400, content_type='application/json')
        else:
            res = flask.request.json
            return flask.Response(json.dumps(res),200)
        
    except Exception as err:
        return flask.Response({"message":"Rule testing failed"}, 400, content_type='application/json')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234, use_reloader=True)
