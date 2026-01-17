import flet as ft
from mine_api.craft_api import MllApi
import json
import os
import configparser

from gui.pages.home_bar import home_bar
from gui.pages.monitoring import monitoring
from gui.pages.accounts_pg import accounts_pg
from gui.pages.screen_shots import screen_shots
from gui.pages.settings_menu import settings_menu
        
    
# Переменные
launcher_options = os.path.join("configs", "launcher_options.ini")
jvm_args_path = os.path.join("configs", "jvmArgs.json")
user_profiles = os.path.join("configs", "usersProfile.json")

abspath = os.path.abspath(__file__)

config_ini = configparser.ConfigParser()
config_ini.read(launcher_options)

path_game = config_ini.get("minecraft", "path_game")

def get_java() -> list:
    return os.listdir("C:\\Program Files\\Java\\")

ma = MllApi()
ma.set_directory(dir=path_game, is_none=True)
print(ma.get_directory())


options = {
    "uuid": "123456789",
    "token": "demo-demo-token",
    "username": "DemoTest",
    "jvmArguments": [],
    "executablePath": config_ini.get("minecraft", "path_java"),
    "demo": True
}

def get_settings_ini() -> str:
    return launcher_options

def get_jvm_args() -> str:
    with open(jvm_args_path, "r") as f:
        jvmArgs = json.load(f)

    return jvmArgs

def set_jvm_args(new_jvm) -> None:
    with open(jvm_args_path, "w") as rs:
        jvmArgs = json.dump(new_jvm, rs)
    
    return

# Тут описываются функции, свойства и т.д., относящиеся к меню
def menu(page: ft.Page):

    #ma.install_version(version="1.16", callback={"setProgress": lambda e: print(e)}, prefix="quilt")
    
    # Запуск майнкрафта
    def run_mines(e):
        #options["executablePath"] = config_ini.get("minecraft", "path_java")

        if len(options["executablePath"].split("\\")) < 4:
            alert_err = ft.AlertDialog(
                title=ft.Text(value="Упс...", scale=1, weight=ft.FontWeight.BOLD),
                content=ft.Text(value="Кажется у вас не установлен Java JDK, если же он установлен, \nто укажите путь в настройках \nк файлу javaw.exe, например: C:\\Program Files\\Java\\Java-17\\bin\\javaw.exe")
            )

            page.open(alert_err)
        else:
            # ------------------------------------------------------------------------------------------
            # Присваевыем джава аргументы перед запуском
            settings_ini_run = configparser.ConfigParser()
            settings_ini_run.read(get_settings_ini())


            options["jvmArguments"] = get_jvm_args().split()
            options["jvmArguments"].append(f"-Xmx{settings_ini_run.get("minecraft", "ram")}G")
            options["jvmArguments"].append(f"-javaagent:{settings_ini_run.get("minecraft", "authlib")}=ely.by")

            # Проверяем состояние кнопки запуска play/cancel/download/nan
            # Color - panel_bottom
            if play_but.data == "play":
                play_but.content.value = "Отмена"
                play_but.data = "cancel"
                play_but.bgcolor = "#A71515"
                #play_but.disabled = True
                page.update()
                if mod_loader.value != "Vanilla":
                    ma.run_mine(version=f"{versions.value} {mod_loader.value}", options=options)
                else:
                    ma.run_mine(version=f"{versions.value}", options=options)
                play_but.content.value = "Играть"
                play_but.data = "play"
                play_but.bgcolor = "#3D891C"
                play_but.disabled = False
                page.update()
            elif play_but.data == "cancel":
                play_but.content.value = "Играть"
                play_but.data = "play"
                play_but.bgcolor = "#3D891C"
                page.update()

                ma.stop_mine()
            else :
                try :
                    def progs_set(e):
                        progress_bar.value = e / 100
                        page.update()

                    def status_set(e):
                        status_bar.value = f"{e} {progress_bar.value}%/100%"
                        page.update()

                    status_bar = ft.Text(
                        value="0"
                    )

                    progress_bar = ft.ProgressBar(
                        color="#E2E2E2",
                        value=0.0
                    )

                    page.add(status_bar)
                    page.add(progress_bar)

                    play_but.disabled = True
                    play_but.content.value = "Установка"
                    play_but.data = "download"
                    page.update()


                    #callback = {"setProgress": lambda e: print(e)}
                    #callback = {"setStatus": lambda e: print(e)}
                    callback = {
                        "setProgress": lambda e: progs_set(e),
                        "setStatus": lambda e: status_set(e)
                    }

                    if mod_loader.value == "Vanilla":
                        ma.install_version(version=versions.value, callback=callback)
                    elif mod_loader.value == "Fabric":
                        ma.install_version(version=versions.value, callback=callback, prefix="fabric")
                    elif mod_loader.value == "Quilt":
                        ma.install_version(version=versions.value, callback=callback, prefix="quilt")
                    else :
                        ma.install_version(version=versions.value, callback=callback, prefix="forge")
                    
                    progress_bar.visible = False
                    status_bar.visible = False

                    play_but.content.value = "Отмена"
                    play_but.data = "cancel"
                    play_but.disabled = True
                    page.update()
                    if mod_loader.value != "Vanilla":
                        ma.run_mine(version=f"{versions.value} {mod_loader.value}", options=options)
                    else:
                        ma.run_mine(version=f"{versions.value}", options=options)
                    play_but.content.value = "Играть"
                    play_but.data = "play"
                    play_but.disabled = False

                    page.update()

                except Exception as e:
                    print("установка не удалась", e)
            # ------------------------------------------------------------------------------------------


    def chg_ver(e):
        def play_button_game():
            play_but.content.value = "Играть"
            play_but.data = "play"
            page.update()

        def play_button_nan():
            play_but.content.value = "Нет версии"
            play_but.data = "nan"
            play_but.disabled = True
            page.update()

        def play_button_download():
            play_but.content.value = "Установить"
            play_but.data = "download"
            page.update()

        vers = [i["id"] for i in ma.get_version(downloads=True, vanilla=False)]
        print(vers)

        play_but.disabled = False
        
        if mod_loader.value == "Vanilla":
            if f"{versions.value}" in vers:
                play_button_game()
            else :
                play_button_download()
        else :
            if f"{versions.value} {mod_loader.value}" in vers:
                play_button_game()
            else :
                match mod_loader.value:
                    case "Forge":
                        ver_forge = [j.split("-")[0] for j in ma.get_version(vanilla=False, forge=True)]
                        if versions.value in ver_forge:
                            play_button_download()
                        else:
                            play_button_nan()
                    case "Fabric":
                        ver_fabric = [j["version"] for j in ma.get_version(vanilla=False, fabric=True)]
                        if versions.value in ver_fabric:
                            play_button_download()
                        else:
                            play_button_nan()
                    case "Quilt":
                        ver_quilt = [j["version"] for j in ma.get_version(vanilla=False, quilt=True)]
                        if versions.value in ver_quilt:
                            play_button_download()
                        else:
                            play_button_nan()

                page.update()
        
    def chg_bar(e):
        print(navigation.selected_index)
        match navigation.selected_index:
            case 0:
                osnv.content = home_bar(page, osnv)
                page.update()
            case 1:
                osnv.content = screen_shots(page, ma)
                page.update()
            case 2:
                print("лаботает")
                osnv.content = monitoring(page, osnv)
                page.update()
            case 4:
                osnv.content = accounts_pg(page, user_profiles, osnv)
                page.update()
            case 5:
                osnv.content = settings_menu(page, get_settings_ini, get_jvm_args, set_jvm_args, get_java, ma, options)
                page.update()

    def papka(e):
        os.system(f"explorer.exe {ma.get_directory()}")
    
    def filt(e):
        versions.options = []
        versions.value = ""

        def get_version_str(item):
            return item.get("version") or item.get("id") or ""

        if radio_filter.value == "all":
            ver = ma.get_version(vanilla=True)
    
            for i in ver:
                if "id" in i:

                    versions.options.append(
                        ft.DropdownOption(
                            key=f"{i["id"]}",
                            text=f"{i["id"]}"
                        )
                    )
                else :
                    versions.options.append(
                        ft.DropdownOption(
                            key=f"{i["version"]}",
                            text=f"{i["version"]}"
                        )
                    )

            page.update()
        else :
            ver = ma.get_version(downloads=True)
            check_list = []
    
            for i in ver:
                if i["id"].split()[0] in check_list:
                    continue
                
                check_list.append(i["id"].split()[0])

                versions.options.append(
                    ft.DropdownOption(
                        key=i["id"].split()[0],
                        text=i["id"].split()[0]
                    )
                )


            page.update()

    def type_account(type: str):
        match type:
            case "ely.by":
                return ft.Image(src=os.path.join("gui", "images", "ely.png"), width=20)
            case "offline":
                return ft.Icon(name=ft.Icons.PERSON_ROUNDED, size=20)
            case "microsoft":
                return ft.Image(src=os.path.join("gui", "images", "microsoft.png"), width=20)

    def chg_accounts(e):
        data = accounts.options[int(accounts.value.split(":")[1])].data

        options["username"] = data["username"]
        options["uuid"] = data["uuid"]
        options["token"] = data["token"]
        options["demo"] = False


    # Color - panel_bottom - radio_filter
    radio_filter = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(
                    label="Все",
                    value="all",
                    active_color="#E2E2E2"
                ),
                ft.Radio(
                    label="Установленные",
                    value="tk_ust",
                    active_color="#E2E2E2"
                )
            ],
            expand=20,
            height=50,
            spacing=-5,
        ),
        value="all",
        on_change=filt
    )

    # Color - panel_bottom - checkbox
    client_obn = ft.Checkbox(
        label="Обновить клиент",
        active_color="#E2E2E2"
    )

    versions = ft.Dropdown(  
        label="Версия",
        options=[],
        expand=30,
        width=195,
        on_change=chg_ver,
        menu_width=200,
        menu_height=200
    )

    mod_loader = ft.Dropdown(  
        label="Mod-loader",
        options=[
            ft.DropdownOption(
                key="Vanilla",
                text="Vanilla"
            ),
            ft.DropdownOption(
                key="Forge",
                text="Forge"
            ),
            ft.DropdownOption(
                key="Fabric",
                text="Fabric"
            ),
            ft.DropdownOption(
                key="Quilt",
                text="Quilt"
            )
        ],
        expand=30,
        width=150,
        on_change=chg_ver,
        menu_width=200,
        value="Vanilla"
    )

    accounts = ft.Dropdown(
        label="Accounts",
        options=[],
        expand=30,
        width=150,
        menu_width=200,
        on_change=chg_accounts
    )
    

    with open(user_profiles, "r") as f:
        acc_list = json.load(f)

        i = 0
        for acc_iter in acc_list["users"]:
            accounts.options.append(
                ft.DropdownOption(
                    key=f"{acc_iter["username"]}:{i}",
                    text=acc_iter["username"],
                    content=ft.Row(
                        controls=[
                            type_account(acc_iter["type"]),
                            ft.Text(value=acc_iter["username"])
                        ]
                        
                    ),
                    data=acc_iter
                )
            )

            i+=1


    def reload(e):
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        err_row.visible = False
        prgrs.visible = True
        page.update()
        load()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    err_row = ft.Row([ft.Text("Не удалось получить список версий!", color=ft.Colors.RED), ft.IconButton(icon=ft.Icons.REPLAY_ROUNDED, on_click=reload)])
    prgrs = ft.ProgressRing()
    page.add(prgrs)
    page.add(err_row)
    err_row.visible = False
    page.update()
    


    def load():
        


        try:
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            prgrs.visible = True
            page.update()
            ver = ma.get_version(vanilla=True)
            prgrs.visible = False
            page.update()

            return ver
        except :
            err_row.visible = True
            prgrs.visible = False
            page.update()
            ver = ma.get_version(downloads=True, vanilla=False)
            return ver

    ver = load()
    for i in ver:
        versions.options.append(
            ft.DropdownOption(
                key=f"{i["id"]}",
                text=f"{i["id"]}"
            )
        )

    #data = "play" or "download" or "cancel" or "nan"
    # Color - panel_bottom
    play_but = ft.ElevatedButton(
        content=ft.Text(value="Играть", scale=2, color="#E2E2E2"),
        expand=True,
        height=80,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=run_mines,
        disabled=True,
        bgcolor="#3D891C", # Default: #1A1A1A
        data="play"
    )

    # Color - panel_bottom
    buttons = ft.Container(
        content=ft.Row(
            controls=[
                play_but,
                ft.Column(
                    controls=[
                        # Color - panel_bottom - open_explorer
                        versions,
                        ft.ElevatedButton(
                            text="Папка",
                            icon=ft.Icons.FOLDER_COPY,
                            expand=20,
                            width=195,
                            on_click=papka,
                            bgcolor="#1A1A1A",
                            color="#E2E2E2"
                        ),
                    ],
                    spacing=5,
                    height=80
                ),
                ft.Column(
                    controls=[
                        mod_loader,
                        accounts
                    ],
                    spacing=5,
                    height=80
                ),

                ft.Column(
                    controls=[
                        radio_filter,
                        client_obn
                        
                    ],
                    spacing=5,
                    height=80
                ),
                ft.ElevatedButton(
                    content=ft.Text(value="Контейнер", scale=2, color="#E2E2E2"),
                    expand=1,
                    height=80,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    bgcolor="#1A1A1A"
                ),

            ]
        ),
        bgcolor="#121212",
        border_radius=10,
        padding=5
    )


    navigation = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME_ROUNDED,
                label="Home"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CAMERA_ALT_OUTLINED,
                selected_icon=ft.Icons.CAMERA_ALT_ROUNDED,
                label="Screenshots"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MONITOR_OUTLINED,
                selected_icon=ft.Icons.MONITOR_ROUNDED,
                label="Monitoring"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ABC_OUTLINED,
                selected_icon=ft.Icons.ABC_ROUNDED,
                label="Mods"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PERSON_OUTLINED,
                selected_icon=ft.Icons.PERSON_ROUNDED,
                label="Account"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS_ROUNDED,
                label="Settings"
            ),
            
        ],
        bgcolor="#121212",
        indicator_color="#292929",
        on_change=chg_bar
    )
    
    global osnv
    osnv = ft.Container(
        content=home_bar(
            page, 
            ft.Container(
                content=ft.ProgressRing(),
                alignment=ft.alignment.center
            )
        ),
        bgcolor="#121212",
        expand=100,
        margin=5,
        border_radius=10,
        height=1000,
        padding=5
    )

    nav_view = ft.Row(
        controls=[
            navigation,
            osnv
        ]
    )

    view = ft.Container(
        content=nav_view,
        height=500,
        bgcolor="#121212",
        expand=10,
        border_radius=10
    )


    column = ft.Column(
        controls=[
            view,
            buttons
        ],
        alignment=ft.MainAxisAlignment.END,
        adaptive=True,
        expand=True
    )

    page.add(column)