import os
import random
import requests
import configparser

from docmesh_cli.logos import LOGOS


RC_FILE = os.path.expanduser("~/.docmeshrc")
PARSER = configparser.ConfigParser()


class TermColor:
    blue = "\033[94m"
    green = "\033[92m"
    red = "\033[96m"
    end = "\033[0m"


def _create_profile() -> tuple[str, str]:
    server = input("docmesh server: ")
    access_token = input("docmesh token: ")
    profile = input("profile name: ")

    PARSER[profile] = {}
    PARSER[profile]["server"] = server
    PARSER[profile]["access_token"] = access_token

    with open(RC_FILE, "w", encoding="utf-8") as f:
        PARSER.write(f)

    return server, access_token


def _profile_management() -> tuple[str, str]:
    # setup parser

    if not os.path.exists(RC_FILE):
        print(f"You have not set up {RC_FILE}, create a new profile.")
        return _create_profile()
    else:
        print(f"Load profiles from {RC_FILE}.")
        PARSER.read(RC_FILE)

        profiles: dict[int, str] = dict(enumerate(PARSER.sections()))
        msg = "\n".join(f"{k}: {v}" for k, v in profiles.items())

        print(msg)
        option = int(input("Select you profile (if selection is not available, you can create a new profile): "))

        if option in profiles:
            server = PARSER[profiles[option]]["server"]
            access_token = PARSER[profiles[option]]["access_token"]

            return server, access_token
        else:
            return _create_profile()


def client() -> None:
    print(random.choice(LOGOS))

    # load server and access_token from profiles
    server, access_token = _profile_management()

    # setup headers
    headers = {"Authorization": f"Bearer {access_token}"}

    # retreive entity_name and session_id
    rsp = requests.post(url=f"{server}/login", headers=headers, timeout=300)
    if rsp.status_code == 200:
        data = rsp.json()["data"]
        entity_name = data["entity_name"]
        session_id = data["session_id"]
        print(f"{TermColor.green}You are logined in as: {entity_name} at {server}{TermColor.end}")
    if rsp.status_code == 401:
        detail = rsp.json()["detail"]
        print(f"{TermColor.red}{detail}{TermColor.end}")
        rsp.raise_for_status()
    else:
        rsp.raise_for_status()

    # send query
    while True:
        query = input(f"{TermColor.blue}query: {TermColor.end}")

        if query == "/end":
            # a special input to end the loop
            break

        data = {"session_id": session_id, "query": query}
        rsp = requests.post(url=f"{server}/agent", headers=headers, json=data, timeout=300)

        output = rsp.json()["data"]["output"]
        if rsp.status_code == 200:
            print(f"{TermColor.green}{output}{TermColor.end}")
        else:
            print(f"{TermColor.red}{output}{TermColor.end}")
