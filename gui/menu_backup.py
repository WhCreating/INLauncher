import flet as ft
from mine_api.craft_api import MllApi
import json
import os
import configparser
from github import Github
import webbrowser
from gui.parse_server import Servers
from nbt import nbt
import asyncio
import threading
from plyer import notification
import platform

# Classes
class Image_shot():
    def __init__(self, page: ft.Page, img):
        foto = ft.AlertDialog(
            content=ft.Stack(
                controls= [ 
                    ft.Image(
                        src=img, 
                        expand=True, 
                        width=5000
                    ), 
                    ft.Row(
                        controls=[
                             ft.Column(
                                controls=[
                                        ft.IconButton( 
                                        icon=ft.Icons.CANCEL_OUTLINED, 
                                        on_click=lambda e: page.close(foto) 
                                    ) 
                                ]
                             )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ]
            
            ), 
            bgcolor=ft.Colors.TRANSPARENT, 
            modal=True
        )


        self.gallery = ft.Container(
            content=ft.Image(
                src=img,
                border_radius=10,
                width=373,
                fit="contain",
            ),
            on_click=lambda e: page.open(foto)
        )


    def retur_gal(self):

        return self.gallery
    
class Accounts_Card():
    def __init__(self, type_acc: str = "ely.by", nickname = "", col: ft.Column | None = None, page: ft.Page | None = None):
        def delete_accs(e):
            with open(user_profiles, "r", encoding="utf-8") as jss:
                jss = json.load(jss)

                for i, acc in enumerate(jss["users"]):
                    if acc["username"] == nickname:
                        jss["users"].pop(i)
                        

        
            with open(user_profiles, "w", encoding="utf-8") as jssw:
                json.dump(jss, jssw, ensure_ascii=False)

            osnv.content = accounts_pg(page)
            page.update()
            

        self.edit = ft.IconButton(icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED)

        # Color - accounts_page
        self.card_accounts = ft.Card(
            content=ft.Container(content=ft.Row(
                    controls=[
                        ft.Image(src=os.path.join("gui", "images", "ely.png"), width=50) if type_acc == "ely.by" else ft.Icon(name=ft.Icons.PERSON_ROUNDED, size=50),
                        ft.Text(value=nickname, color="#E2E2E2", expand=5),
                        ft.IconButton(icon=ft.Icons.DELETE_ROUNDED, icon_color="#B02020", tooltip="Удалить аккаунт", on_click=delete_accs)
                    ],
                    spacing=5,
                    expand=True
                ),
                padding=10,
                expand=True,
                width=230
                
            ),
            height=70,
            color="#282727"
        )

    def return_accs(self):
        return self.card_accounts  
    
class Social(ft.ElevatedButton):
    def __init__(self, src: str, url: str, size: int):
        super().__init__()

        self.content = ft.Image(src=src, width=size - 5)
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        self.width = size
        self.height = size
        self.on_click = lambda e: webbrowser.open(url)

class ServerCard(ft.Card):
    def __init__(self, ip: str):
        super().__init__()
        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.ProgressRing(),
                    ft.ListTile(
                        title=ft.Row([ft.Text("Загрузка данных", overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, expand=True)], expand=True),
                        subtitle=ft.Text(f"..."),
                        adaptive=True,
                        expand=True,
                    ),
                ],
                spacing=5,
                expand=True
            ),
            padding=ft.Padding(10, 0, 0, 0),
            expand=True,
            width=400
        )

        def run():
            asyncio.run(self._server_init(ip))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()

    async def _server_init(self, ip: str):

        self.servers = Servers()
        self.status = await self.servers.get_status_server(ip=ip)
        self.margin = 5
        print(self.status)
        self.padding = ft.padding.only(left=5)
        self.height=70,
        self.color="#1A1A1A"

        if self.status != "none":
            try:
                self.tooltip = self.status["name"]

                self.content = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(src_base64=f"{self.status["icon"].split("base64,")[1]}", width=30),
                            ft.ListTile(
                                title=ft.Row([ft.Text(self.status["name"], overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, expand=True)], expand=True),
                                subtitle=ft.Text(f"{self.status["online"]}/{self.status["max_online"]}"),
                                adaptive=True,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.ADD_ROUNDED,
                                icon_color="#E2E2E2",
                                icon_size=30,
                                adaptive=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.REMOVE_ROUNDED,
                                icon_color="#B02020",
                                icon_size=30,
                                adaptive=True,
                                visible=False
                            )
                        ],
                        spacing=5,
                        expand=True
                    ),
                    padding=ft.Padding(10, 0, 0, 0),
                    expand=True,
                    width=400
                )
            except Exception:
                self.tooltip = "Не удалось получить информацию об сервере"

                self.content = ft.Container(
                content=ft.Row(
                        controls=[
                            ft.ProgressRing(),
                            ft.ListTile(
                                title=ft.Row([ft.Text("Не удалось получить информацию об сервере", overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, expand=True)], expand=True),
                                subtitle=ft.Text(f"..."),
                                adaptive=True,
                                expand=True,
                            ),
                        ],
                        spacing=5,
                        expand=True
                    ),
                    padding=ft.Padding(10, 0, 0, 0),
                    expand=True,
                    width=400
                )
        else :
            self.tooltip = "Не удалось получить информацию об сервере"

            self.content = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.ProgressRing(),
                        ft.ListTile(
                            title=ft.Row([ft.Text("Не удалось получить информацию об сервере", overflow=ft.TextOverflow.ELLIPSIS, max_lines=1, expand=True)], expand=True),
                            subtitle=ft.Text(f"..."),
                            adaptive=True,
                            expand=True
                        ),
                    ],
                    spacing=5,
                    expand=True
                ),
                padding=ft.Padding(10, 0, 0, 0),
                expand=True,
                width=400
            )

        self.page.update()

    def read_servers_mine(self):
        file = nbt.NBTFile(os.path.join(ma.get_directory(), "servers.dat"), "rb", compression='uncompressed')

        print(file.pretty_tree())

        
    
# Пути
launcher_options = os.path.join("configs", "launcher_options.ini")
jvm_args_path = os.path.join("configs", "jvmArgs.json")
user_profiles = os.path.join("configs", "usersProfile.json")

abspath = os.path.abspath(__file__)

config_ini = configparser.ConfigParser()
config_ini.read(launcher_options)

# Поле с путями
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


def home_bar(ma: MllApi):
    

    file = "https://github.com/WhCreating/inl_project/blob/main/home_page_info/home_page.txt"

    try :
        g = Github()

        repo = g.get_repo("WhCreating/inl_project")

        file = repo.get_contents("home_page_info/home_page.txt")

        value = file.decoded_content.decode()
    except Exception :
        value = "Нет соединения с интернетом"

    mark = ft.Markdown(
        value=value
    )

    sn = ft.Row(
        controls=[
            Social(src=os.path.join("gui", "images", "telegram.png"), url="https://t.me/inlauncher", size=50)
        ]
    )

    col = ft.Column(
        controls=[
            mark,
            ft.Column(
                controls=[
                    sn
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]
    )
    #print(file.decoded_content.decode("utf-8"))
    return col  
    
def monitoring(page: ft.Page):
    def add_servers(servers):
        for ip in servers:
            new_content.controls[1].controls.append(ServerCard(ip=ip))
            page.update()

    def on_search(e):
        servers = Servers().get_servers(search=search.value)
        new_content.controls[1].controls.clear()
        add_servers(servers)

    servers = Servers().get_servers()
    print(servers)

    content = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center
    )

    search = ft.TextField(
        label="Поиск",
        expand=True
    )
    send_search = ft.IconButton(
        icon=ft.Icons.SEARCH_ROUNDED,
        on_click=on_search
    )

    search_row = ft.Row(
        controls=[
            search,
            send_search
        ],
        expand=True
    )

    new_content = ft.Column(
            controls=[
                search_row,
                ft.Row(
                    controls=[],
                    wrap=True,
                    adaptive=True,
                    scroll=ft.ScrollMode.ADAPTIVE
                )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        adaptive=True,
        expand=True
    )

    content = new_content

    add_servers(servers)

    #abv = ServerCard(ip="mr.aresmine.me").read_servers_mine()

    return content

def accounts_pg(page: ft.Page):
    
    def add_account(e):
        from gui.rout_pages import rout_pages
        page.controls.clear()
        page.update()
        rout_pages(page, "auth_ely")

    accou = ft.Column(
        controls=[
            #Accounts_Card(page).return_accs()
        ],
        spacing=3,
        adaptive=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        wrap=True
    )

    # Color - accounts_page
    add_on_button = ft.IconButton(
        icon=ft.Icons.ADD_ROUNDED,
        icon_color="#E2E2E2",
        icon_size=35,
        on_click=add_account
    )

    column_x2 = ft.Column(
        controls=[
            ft.Row(controls=[add_on_button], alignment=ft.MainAxisAlignment.END)
            
        ],
        alignment=ft.MainAxisAlignment.END
    )

    stack_bro = ft.Stack(
        controls=[
            accou,
            column_x2
        ]
    )

    with open(user_profiles, "r") as f:
        acc_list = json.load(f)

        for acc_iter in acc_list["users"]:
            accou.controls.append(Accounts_Card(acc_iter["type"], acc_iter["username"], accou, page).return_accs())

    return stack_bro
#kasfbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
def screen_shots(page: ft.Page):
    def repeat(e):
        gallery.controls = []
        image = os.listdir(path=os.path.join(ma.get_directory(), "screenshots"))
        for img in image:
            gallery.controls.append(
                Image_shot(page=page, img=f"{ma.get_directory()}\\screenshots\\{img}").retur_gal()
            )
        
        page.update()


    gallery = ft.Row(
        controls=[],
        wrap=True,
        scroll="adaptive",
        expand=True,
        spacing=5
    )

    stack_gallery = ft.Stack(
        controls=[
            gallery,
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.REPLAY_ROUNDED,
                                on_click=repeat
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FOLDER_ROUNDED,
                                on_click=lambda e: os.system(f"explorer.exe {os.path.join(ma.get_directory(), "screenshots")} || xdg-open {os.path.join(ma.get_directory(), "screenshots")}")

                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]
    )
    
        
    # Path_change
    print(ma.get_directory())
    try:
        image = os.listdir(path=os.path.join(ma.get_directory(), "screenshots"))
        print(image)

        for img in image:
            gallery.controls.append(
                Image_shot(page=page, img=os.path.join(ma.get_directory(), "screenshots", img)).retur_gal()
            )

        print(gallery.controls)
        page.update()

        return stack_gallery
    except:

        display = ft.Container(
            content=ft.Text(value="У вас нет скриншотов", scale=2, weight=ft.FontWeight.BOLD,),
            expand=True,
            alignment=ft.alignment.center
        )

        return display

def settings_menu(page: ft.Page):
    # Инциализация конфига
    settings_ini = configparser.ConfigParser()
    settings_ini.read(get_settings_ini())

    # launcher
    width_ui = ft.TextField(value=settings_ini.get("launcher", "width"), expand=False)
    height_ui = ft.TextField(value=settings_ini.get("launcher", "height"), expand=False)
    ru_ui = settings_ini.get("launcher", "language")
    # mainecraft
    ram_ui = ft.TextField(value=settings_ini.get("minecraft", "ram"), expand=False, width=40)
    path_game_ui = ft.TextField(value=settings_ini.get("minecraft", "path_game"), expand=False)
    jvm_ui = ft.TextField(value=get_jvm_args(), expand=False)
    path_java_ui = ft.TextField(value=settings_ini.get("minecraft", "path_java"))
    authlib_ui = ft.TextField(value=settings_ini.get("minecraft", "authlib"))

    def apply_settings(e):
        try :
            settings_ini.set("launcher", "width", width_ui.value)
            settings_ini.set("launcher", "height", height_ui.value)
            settings_ini.set("launcher", "language", ru_ui)
            settings_ini.set("minecraft", "ram", ram_ui.value)
            settings_ini.set("minecraft", "path_game", path_game_ui.value)
            settings_ini.set("minecraft", "path_java", path_java_ui.value)
            ma.set_directory(dir=settings_ini.get("minecraft", "path_game"))
            set_jvm_args(jvm_ui.value)
            options["executablePath"] = path_java_ui.value
            print(options)
            with open(get_settings_ini(), 'w') as configfile:
                settings_ini.write(configfile)

            notification.notify(title="INLauncher", message="Настройки были успешно применены", app_name="INLauncher", app_icon="icon.ico")
        except Exception as e:
            notification.notify(title="INLauncher", message="Неудалось сохранить изменения", app_name="INLauncher", app_icon="icon.ico")


    column_settings = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text(
                        value="launcher"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(value="Width: "),
                            width_ui
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Height: "),
                            height_ui
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Language: "),
                            ft.Dropdown(
                                options=[
                                    ft.DropdownOption(
                                        key=settings_ini.get("launcher", "language"),
                                        text=settings_ini.get("launcher", "language")
                                    )
                                ],
                                expand=False,
                                value=ru_ui
                                
                            )
                        ]
                    ),
                ],
                wrap=True,
                scroll="adaptive",
                expand=True,
            ),
            
            ft.Row(
                controls=[
                    ft.Text(
                        value="minecraft"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(value="Ram: "),
                            ram_ui,
                            ft.Text(value="gb")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Path_games: "),
                            path_game_ui
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="JVM-Args: "),
                            jvm_ui
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Path_java: "),
                            path_java_ui
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Authlib: "),
                            authlib_ui
                        ]
                    )
                ],
                wrap=True
            ),
            
        ]  
    )
    


    #apply_button = ft.ElevatedButton(
    #    content=ft.Text(value="Применить", scale=2, color="#E2E2E2"),
    #    expand=True,
    #    height=80,
    #    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    #    disabled=False,
    #    bgcolor="#1A1A1A", # Default: #1A1A1A
    #    data="apply_button"

    #)

    # Color - settings_page
    apply_icon_button = ft.IconButton(
        icon=ft.Icons.CHECK_ROUNDED,
        on_click=apply_settings,
        icon_size=35,
        icon_color="#E2E2E2"
    )

    chained_column = ft.Column(
        controls=[
            column_settings,
            
        ]
    )

    stack_menu = ft.Stack(
        controls=[
            chained_column,
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            apply_icon_button
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]
    )

    return stack_menu

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

                play_but.disabled = True
                play_but.content.value = "Установка"
                play_but.data = "download"
                page.update()


                #callback = {"setProgress": lambda e: print(e)}
                #callback = {"setStatus": lambda e: print(e)}
                callback = {
                    "setProgress": lambda x: print(x)
                }

                if mod_loader.value == "Vanilla":
                    ma.install_version(version=versions.value, callback=callback)
                elif mod_loader.value == "Fabric":
                    ma.install_version(version=versions.value, callback=callback, prefix="fabric")
                elif mod_loader.value == "Quilt":
                    ma.install_version(version=versions.value, callback=callback, prefix="quilt")
                else :
                    ma.install_version(version=versions.value, callback=callback, prefix="forge")

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
                osnv.content = home_bar(ma)
                page.update()
            case 1:
                osnv.content = screen_shots(page)
                page.update()
            case 2:
                print("лаботает")
                osnv.content = monitoring(page)
                page.update()
            case 4:
                osnv.content = accounts_pg(page)
                page.update()
            case 5:
                osnv.content = settings_menu(page)
                page.update()

    def papka(e):
        os.system(f"explorer.exe {ma.get_directory()} || xdg-open {ma.get_directory()}")
    
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
        content=home_bar(ma),
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