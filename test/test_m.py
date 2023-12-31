#!/usr/bin/env python3

import os
import argparse
import logging
import warnings
from common import start_container, stop_container, copy_to_container, run_in_container, get_container_id

warnings.filterwarnings("ignore")
logger = logging.getLogger()
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)


class Params(object):

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--container", action="store", help="Container", default="redhat/ubi8")
        parser.add_argument("--script", action="store", help="Script", default="python_setup.sh")
        parser.add_argument("--log", action="store", help="Script", default="setup.log")
        parser.add_argument("--run", action="store_true")
        parser.add_argument("--start", action="store_true")
        parser.add_argument("--stop", action="store_true")
        parser.add_argument("--system", action="store_true")
        parser.add_argument("--git", action="store_true")
        parser.add_argument("--refresh", action="store_true")
        self.args = parser.parse_args()

    @property
    def parameters(self):
        return self.args


def manual_1(args: argparse.Namespace):
    global parent
    requirements = f"{parent}/requirements.txt"
    destination = f"/var/tmp"
    output = f"cat {args.log}"
    script = f"{parent}/python_setup.sh"
    post_script = f"{parent}/test/post_setup.sh"
    if args.system:
        cmd = [f"./{os.path.basename(script)}", "-s"]
    elif args.git:
        cmd = [f"./{os.path.basename(script)}", "-g", "https://github.com/mminichino/python-test-package"]
    else:
        cmd = f"./{os.path.basename(script)}"

    container_id = start_container(args.container)
    try:
        copy_to_container(container_id, script, destination)
        copy_to_container(container_id, requirements, destination)
        copy_to_container(container_id, post_script, destination)
        run_in_container(container_id, destination, cmd)
        stop_container(container_id)
    except Exception:
        run_in_container(container_id, destination, output)
        raise


def manual_2(args: argparse.Namespace):
    global parent
    requirements = f"{parent}/requirements.txt"
    destination = f"/var/tmp"
    script = f"{parent}/python_setup.sh"
    post_script = f"{parent}/test/post_setup.sh"

    container_id = start_container(args.container)
    try:
        copy_to_container(container_id, script, destination)
        copy_to_container(container_id, requirements, destination)
        copy_to_container(container_id, post_script, destination)
    except Exception:
        raise


def refresh():
    global parent
    requirements = f"{parent}/requirements.txt"
    destination = f"/var/tmp"
    script = "python_setup.sh"
    post_script = "post_setup.sh"
    source = f"{parent}/{script}"

    container_id = get_container_id()
    try:
        copy_to_container(container_id, source, destination)
        copy_to_container(container_id, requirements, destination)
        copy_to_container(container_id, post_script, destination)
    except Exception:
        raise


p = Params()
options = p.parameters

try:
    debug_level = int(os.environ['DEBUG_LEVEL'])
except (ValueError, KeyError):
    debug_level = 3

if debug_level == 0:
    logger.setLevel(logging.DEBUG)
elif debug_level == 1:
    logger.setLevel(logging.ERROR)
elif debug_level == 2:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.CRITICAL)

logging.basicConfig()

if options.stop:
    container = get_container_id()
    stop_container(container)

if options.run:
    manual_1(options)

if options.start:
    manual_2(options)

if options.refresh:
    refresh()
