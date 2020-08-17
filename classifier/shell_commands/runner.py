from classifier import main
from classifier import rule_testing
from classifier import rule_insertion

command_function={
    "rule-insertion": rule_insertion.main,
    "rule-testing": rule_testing.test_new_rule,
    "job-labelling": main.main
}

def run(args):
    return command_function[args.task](args.__dict__)
