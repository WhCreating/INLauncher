from github import Github
import json
import os
import requests
import io
import zipfile

with open(os.path.join("info.json")) as f:
    dct = json.load(f)
    version_launcher: str = dct["version"]

def update():

    g = Github()

    repo = g.get_repo("WhCreating/INLauncher")
    latest = repo.get_latest_release()

    if latest.name.strip() != version_launcher.strip():
        response = requests.get("https://github.com/WhCreating/INLauncher/archive/refs/heads/main.zip")
        
        in_mem = io.BytesIO(response.content)

        try :
            with zipfile.ZipFile(in_mem, 'wb') as file:
                for i in file.namelist():
                    if i.startswith("INLauncher-main"):
                        file.extract(i, os.path.join("."))
                        print(file.namelist())
        except Exception as e:
            print(f"Что-то не так: {e}")
    else :
        print("обновление пропущено")

                

if __name__ == "__main__":
    update()