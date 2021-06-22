# -*- coding: utf-8 -*-

"""The command line for `tiny-render`

There are few environment variables are required

- TR_PARAM_BASE 
the directory of your parameter files, and your parameter file should be name as
<env>.yaml

- TR_INPUT_BASE
The directory of the files with placeholders, the file should be name as
<filename>.j2.<suffix>, eg. step1.j2.sql

- TR_OUTPUT_BASE (Optional)
The output directory of the parsed (renderred) files, if not specify, use the
same directory of TR_INPUT_BASE

usage: tiny [-h] [-f FILENAME [FILENAME ...]] env

positional arguments:
  env                   The environment name, eg. dev or prod

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME [FILENAME ...], --filename FILENAME [FILENAME ...]
                        the filename(s) to be renderred
"""

from argparse import ArgumentParser
import os

from . import Render

def get_parser():
    p = ArgumentParser(prog="tiny")

    p.add_argument("env", 
        help="The environment name, eg. dev or prod")
    p.add_argument("-f", 
        "--filename", 
        required=True,
        nargs="+", 
        help="the filename(s) to be renderred")

    return p


def runner():

    param_base = os.environ.get("TR_PARAM_BASE")
    input_base = os.environ.get("TR_INPUT_BASE")

    if param_base is None or input_base is None:
        raise SystemExit("Please ensure TR_PARAM_BASE and TR_INPUT_BASE are set")

    output_base = os.environ.get("TR_OUTPUT_BASE") or input_base


    for d in ():
        os.path.isdir(d)



    parser = get_parser()
    args = parser.parse_args()

    print(args.env)
    print(args.filename)
