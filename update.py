from github import Github
import json
import os

with open(os.path.join("info.json")) as f:
    dct = json.load(f)
    version_launcher = dct["version"]

def update():

    g = Github()

    repo = g.get_repo("WhCreating/INLauncher")
    latest = repo.get_latest_release()

    print(latest.name)

if __name__ == "__main__":
    update()