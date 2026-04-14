from github import Github
import json
import os
import requests
import io
import zipfile
import flet as ft

with open(os.path.join("info.json")) as f:
    dct = json.load(f)
    version_launcher: str = dct["version"]

def loading(page: ft.Page, precent: int, update_latest: str):
    page.controls.clear()

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([ft.Text(value=f"Update {update_latest}")], alignment=ft.MainAxisAlignment.CENTER)
                ]
            ),
            alignment=ft.alignment.center
        )
    )

def update(page: ft.Page):
    if dct["debug"] == "false":
        try :
            g = Github()

            repo = g.get_repo("WhCreating/INLauncher")
            latest = repo.get_latest_release()

            if latest.name.strip() != version_launcher.strip():

                for i in latest.assets:
                    if i.name == "patch.zip":
                        loading(page, 100, latest)

                        response = requests.get(i.browser_download_url)
                        
                        in_mem = io.BytesIO(response.content)
                        
                        try :
                            with zipfile.ZipFile(in_mem, 'r') as file:
                                file.extractall(".")
                        except Exception as e:
                            print(f"Что-то не так: {e}")
            else :
                print("обновление пропущено")
        except Exception as e:
            print(e)
    else :
        return

                

if __name__ == "__main__":
    update()