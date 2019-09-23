#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
from mag2elasticsearch.maker import *


def load_config():
    global config
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
    return config


if __name__ == "__main__":
    pparser = argparse.ArgumentParser()
    pparser.add_argument('-p','--PaperAuthorAffiliations', required=False, help='output path', action='store_true')
    pparser.add_argument('--limit', required=False, default=0, type=int)
    pparser.add_argument('-f','--onlyInstitutions', nargs='+', help='<Required> Set flag', required=False, default=None)

    args = pparser.parse_args()
    print (args)
    config= load_config()

    if args.PaperAuthorAffiliations:
        authors2elastic(config,args)

