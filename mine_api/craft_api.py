import minecraft_launcher_lib as mll
import os
from mine_api.exceptions.mine_api_error import PathIsNone, IDontKnowVersion
import subprocess
from datetime import datetime, timezone
import re
from typing import Any

class MllApi:
    def __init__(self) -> None:
        self.__directory = mll.utils.get_minecraft_directory()
        print(self.__directory)
    
    def rename_path(self, minecraft_version, loader_version_id, path, loader_name):
        os.rename(os.path.join(path, "versions", loader_version_id), os.path.join(path, "versions", f"{minecraft_version} {loader_name}"))
        os.rename(os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{loader_version_id}.jar"), os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{minecraft_version} {loader_name}.jar"))
        os.rename(os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{loader_version_id}.json"), os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{minecraft_version} {loader_name}.json"))
        import json

        with open(os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{minecraft_version} {loader_name}.json"), "r") as f:
            data = json.load(f)

        data["id"] = f"{minecraft_version} {loader_name}"

        with open(os.path.join(path, "versions", f"{minecraft_version} {loader_name}", f"{minecraft_version} {loader_name}.json"), "w") as j:
            json.dump(data, j, indent=2)    
 

    #Получение директории майнкрафта
    def get_directory(self, dir: str = "minecraft") -> str:
        if dir == "minecraft":
            return self.__directory
    def set_directory(self, dir: str | None, is_none=False) -> None:
        if os.path.exists(dir):
            self.__directory = dir
        else :
            if is_none is False:
                raise PathIsNone(f"The path '{dir}' you specified does not exist, if the path has not yet been created, then change the is_none parameter to True")
            else :
                self.__directory = dir

    def get_version(self, optifine: bool = False, forge: bool = False, fabric: bool = False, quilt: bool = False, vanilla: bool = True, all: bool = False, downloads: bool = False) -> Any:
        print(mll.forge.find_forge_version("1.16.5"))
        print(mll.fabric)
        print(mll.forge.find_forge_version("1.16.5"))

        if downloads:
            return mll.utils.get_installed_versions(self.get_directory())
        elif vanilla:
            ver = []
            for i in mll.utils.get_version_list():
                i["moders"] = "Версия"
                ver.append(i)
            return ver
        elif fabric:
            ver = []
            for i in mll.fabric.get_all_minecraft_versions():
                i["moders"] = "Fabric"
                ver.append(i)
            print(ver)
            return ver
        elif forge:
            fr = mll.forge.list_forge_versions()
            print(fr)
            return fr
        elif quilt:
            ver = []
            for i in mll.quilt.get_all_minecraft_versions():
                i["moders"] = "Quilt"
                ver.append(i)
            return ver
        elif all:
            try:
                vers = []

                for i in mll.utils.get_version_list():
                    if i["type"] == "snapshot":
                        i["moders"] = "Snapshot"
                    else :
                        i["moders"] = "Версия"
                        vers.append(i)
                for j in mll.fabric.get_all_minecraft_versions():
                    j["moders"] = "Fabric"
                    vers.append(j)
                for k in mll.quilt.get_all_minecraft_versions():
                    print(k)
                    k["moders"] = "Quilt"
                    vers.append(k)
                '''for l in mll.forge.list_forge_versions():
                    k["moders"] = "Forge"
                    vers.append(l)'''

                def get_version_str(item):
                    return item.get("version") or item.get("id") or ""

                # Функция для преобразования версии в кортеж чисел
                def version_key(v):
                    parts = re.findall(r'\d+', v)
                    return tuple(map(int, parts))

                # Сортируем по версии (самые новые в начале)
                sorted_items = sorted(
                    vers,
                    key=lambda item: version_key(get_version_str(item)),
                    reverse=True
                )

                return sorted_items
            except :
                return
        
        

    
    def install_version(self, version: str, callback: dict, prefix: str = "") -> None:
        match prefix:
            case "":
                mll.install.install_minecraft_version(versionid=version, minecraft_directory=self.get_directory(), callback=callback)
            case "forge":
                mll.forge.install_forge_version(versionid=mll.forge.find_forge_version(vanilla_version=version), path=self.get_directory(), callback=callback)
                self.rename_path(version, mll.forge.find_forge_version(version), self.get_directory(), "Forge")
            case "fabric":
                mll.fabric.install_fabric(minecraft_version=version, minecraft_directory=self.get_directory(), callback=callback)
                self.rename_path(version, f"fabric-loader-{mll.fabric.get_latest_loader_version()}-{version}", self.get_directory(), "Fabric")
            case "quilt":
                mll.quilt.install_quilt(minecraft_version=version, minecraft_directory=self.get_directory(), callback=callback)
                self.rename_path(version, f"quilt-loader-{mll.quilt.get_latest_loader_version()}-{version}", self.get_directory(), "Quilt")
            case _:
                raise IDontKnowVersion(f"I don't know this mod loader")
    # def get_and_set_command(self, version: str, ):
    def run_mine(self, version: str, options: str) -> None:

        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        print(mll.utils.get_installed_versions(self.get_directory()))
        command = mll.command.get_minecraft_command(version=version, minecraft_directory=self.get_directory(), options=options)

        
        #subprocess.run(
        #   command,
        #    errors='replace'
        #)

        self.proc = subprocess.Popen(
            command, 
            start_new_session=True,
            bufsize=1,
            universal_newlines=False,
            encoding="UTF-8"
        )


        self.proc.wait()
        

    def stop_mine(self):
        self.proc.terminate()

    def get_jre_vers(self) -> Any:
        return mll.runtime.get_jvm_runtimes()
    def install_jre(self, jvm_ver: str, callback: dict, is_path: bool = False) -> Any:
        mll.runtime.install_jvm_runtime(jvm_version=jvm_ver, minecraft_directory=self.get_directory(), callback=callback)
        if is_path is True:
            return mll.runtime.get_executable_path(jvm_version=jvm_ver, minecraft_directory=self.get_directory())
        
        return
    
    def news(self) -> Any:
        return mll.news.get_minecraft_news()
        


if __name__ == "__main__":
    ma = MllApi()

    '''import subprocess
    path="C:\\Users\\Pasha\\Documents\\mine"
    import requests

    version = "1.16.5"


    #mll.install.install_minecraft_version(versionid=version, minecraft_directory=path, callback={"setProgress": lambda e: print(e)})
    username = input("Введите свой логин: ")
    passwords = input("Введите свой пароль: ")
    

    url_auth = f"https://authserver.ely.by/auth/authenticate"

    param = {
        "username": username,
        "password": passwords,
        "clientToken": "inlauncher1"
    }

    print(url_auth)

    opt = requests.post(url_auth, json=param).json()

    print(opt)

    options = {
        "username": opt["selectedProfile"]["name"],
        "id": opt["selectedProfile"]["id"],
        "accessToken": opt["accessToken"],
        "skins": [{
            "state": "ACTIVE",
            "url": "http://ely.by/storage/skins/c32ba4f5df2f3716f63a2a05f8cfafea.png",
            "alias" : "STEVE"
        }],
        "jvmArguments": [
            "-Xms1G",
            "-Xmx8G",
            "-javaagent:C:\\Users\\Pasha\\Documents\\mine\\authlib-injector.jar=https://ely.by",

        ],
        "executablePath": "C:\\Program Files\\Java\\latest\\jre-1.8\\bin\\java.exe"
    }


    command = mll.command.get_minecraft_command(version=version, minecraft_directory=path, options=options)
    subprocess.run(command)'''

    print(ma.get_jre_vers())

    #print(mll.forge.list_forge_versions())      