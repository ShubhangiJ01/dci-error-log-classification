import argparse
import sys
import logging
import traceback
import os

sys.path.append('../')
from classifier.shell_commands.runner import run
from classifier.settings import parse_argument

LOG = logging.getLogger(__name__)

def main():
    args = parse_argument()    
    try:
        run(args)
    except Exception:
        LOG.error(traceback.format_exc())
        sys.exit(1)

