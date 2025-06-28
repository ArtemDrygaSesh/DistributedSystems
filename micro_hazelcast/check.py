from typing import Optional
import docker

def check_container(container_name):
    docker_client = docker.from_env()
    try:
        container = docker_client.containers.get(container_name)
    except docker.errors.NotFound as exc:
        print(f"Problem with container name\n{exc.explanation}")
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == "running"