##

import docker
from docker.errors import APIError
from docker.models.containers import Container
from typing import Union
import io
import os
import tarfile
import warnings
import logging

warnings.filterwarnings("ignore")
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
logging.getLogger("docker").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def copy_to_container(container_id: Container, src: str, dst: str):
    print(f"Copying {src} to {dst}")
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w|') as tar, open(src, 'rb') as file:
        info = tar.gettarinfo(fileobj=file)
        info.name = os.path.basename(src)
        tar.addfile(info, file)

    container_id.put_archive(dst, stream.getvalue())


def start_container(image: str) -> Container:
    client = docker.from_env()

    print(f"Starting {image} container")

    try:
        container_id = client.containers.run(image,
                                             detach=True,
                                             name="pytest",
                                             command=["tail", "-f", "/dev/null"]
                                             )
    except docker.errors.APIError as e:
        if e.status_code == 409:
            container_id = client.containers.get('pytest')
        else:
            raise

    print("Container started")
    print("Done.")
    return container_id


def run_in_container(container_id: Container, directory: str, command: Union[str, list[str]]):
    exit_code, output = container_id.exec_run(command, workdir=directory)
    for line in output.split(b'\n'):
        print(line.decode("utf-8"))
    assert exit_code == 0
    print("Done.")


def get_container_id(name: str = "pytest"):
    client = docker.from_env()
    return client.containers.get(name)


def stop_container(container_id: Container):
    print("Stopping container")
    container_id.stop()
    print("Removing test container")
    container_id.remove()
    print("Done.")
