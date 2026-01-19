import io
import os
import requests
import zipfile
import shutil
import json

source = "https://github.com/WhCreating/INLauncher/archive/refs/heads/main.zip"
install_path = os.path.join("done_build")
inlauncher_source = os.path.join(install_path, "INLauncher-main")

def json_import() -> None:
    #jvmArgs
    shutil.copy2(os.path.join(inlauncher_source, "configs", "jvmArgs.example.json"), os.path.join(inlauncher_source, "configs", "jvmArgs.json"))

    #launcher_options
    shutil.copy2(os.path.join(inlauncher_source, "configs", "launcher_options.example.ini"), os.path.join(inlauncher_source, "configs", "launcher_options.ini"))

    #themes
    shutil.copy2(os.path.join(inlauncher_source, "configs", "themes.example.json"), os.path.join(inlauncher_source, "configs", "themes.json"))

    #userProfiles
    shutil.copy2(os.path.join(inlauncher_source, "configs", "userProfile.example.json"), os.path.join(inlauncher_source, "configs", "userProfile.json"))

def move_exe() -> None:
    shutil.move(os.path.join(inlauncher_source, "_internal"), inlauncher_source)
    shutil.move(os.path.join(inlauncher_source, "INLauncher.exe"), inlauncher_source)

def install_req() -> None:
    os.system(f"pip install -r {os.path.join(inlauncher_source, "requirements.txt")}")

def build() -> None:
    os.makedirs(install_path, exist_ok=True)

    response = requests.get(source, stream=True)

    in_memory = io.BytesIO(response.content)

    with zipfile.ZipFile(in_memory, 'r') as zip_ref:
        zip_ref.extractall(install_path)


    install_req()
    os.system(f"flet pack -n INLauncher -i {os.path.join(inlauncher_source, "icon.ico")} -D {os.path.join(inlauncher_source, "main.py")}")
    move_exe()
    json_import()

    print("Билдинг готов!")

    
if __name__ == "__main__":
    build()