#!/usr/bin/env python3

import os
import logging
import warnings
import pytest
from common import start_container, stop_container, copy_to_container, run_in_container

warnings.filterwarnings("ignore")
logger = logging.getLogger()
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)


@pytest.mark.parametrize("container", ["redhat/ubi8",
                                       "redhat/ubi9",
                                       "rockylinux:8",
                                       "rockylinux:9",
                                       "oraclelinux:8",
                                       "oraclelinux:9",
                                       "fedora:latest",
                                       "ubuntu:focal",
                                       "ubuntu:jammy",
                                       "debian:bullseye",
                                       "opensuse/leap:latest",
                                       "registry.suse.com/suse/sle15:latest",
                                       "registry.suse.com/suse/sle15:15.3",
                                       "amazonlinux:2",
                                       "amazonlinux:2023"])
@pytest.mark.parametrize("script", ["python_setup.sh"])
@pytest.mark.parametrize("post_script", ["post_setup.sh"])
@pytest.mark.parametrize("script_arg", [None, ["-s"], ["-g", "https://github.com/mminichino/python-test-package"]])
def test_1(container, script, post_script, script_arg):
    global parent
    test_dir = os.path.join(parent, 'test')
    requirements_file = os.path.join(parent, 'requirements.txt')
    script_file = os.path.join(parent, script)
    post_script_file = os.path.join(test_dir, post_script)
    destination = f"/var/tmp"
    script = [f"./{os.path.basename(script_file)}"]
    if script_arg:
        script.extend(script_arg)

    container_id = start_container(container)
    try:
        copy_to_container(container_id, script_file, destination)
        copy_to_container(container_id, requirements_file, destination)
        copy_to_container(container_id, post_script_file, destination)
        run_in_container(container_id, destination, script)
        stop_container(container_id)
    except Exception:
        stop_container(container_id)
        raise
