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
    if dct["debug"] == "false":
        g = Github()

        repo = g.get_repo("WhCreating/INLauncher")
        latest = repo.get_latest_release()

        if latest.name.strip() != version_launcher.strip():

            for i in latest.assets:
                if i.name == "patch.zip":

                    response = requests.get(i.browser_download_url)
                    
                    in_mem = io.BytesIO(response.content)
                    
                    try :
                        with zipfile.ZipFile(in_mem, 'r') as file:
                            file.extractall(".")
                    except Exception as e:
                        print(f"Что-то не так: {e}")
                    
        else :
            print("обновление пропущено")
    else :
        return

                

if __name__ == "__main__":
    update()