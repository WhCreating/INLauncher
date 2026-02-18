import flet as ft
import configparser
from typing import Any
from mine_api.craft_api import MllApi
from plyer import notification

def settings_menu(page: ft.Page, get_settings_ini: Any, get_jvm_args: Any, set_jvm_args: Any, get_java: Any, ma: MllApi, options: dict):
    def update_choice_java(e = None):
        for java in get_java():
            choice_java.options.append(
                ft.DropdownOption(
                    text=f"C:\\Program Files\\Java\\{java}\\bin\\javaw.exe",
                    content=ft.Text(
                        value=java
                    )
                )
            )

        choice_java.value = path_java_ui.value
        page.update()
    
    def chg_path(e):
        path_java_ui.value = choice_java.value
        page.update()
        print(choice_java.value)

    def folder_check(e: ft.FilePickerResultEvent):
        if e.path:
            choice_java.options.append(
                ft.DropdownOption(
                    text=e.path
                )
            )
        else :
            pass

        page.update()
    
    def edit_path_func(e):
        path_java_ui.visible = True
        choice_java.visible = False
        edit_path.visible = False
        apply_path.visible = True


        page.update()
    
    def apply_path_func(e):
        if path_java_ui.value in choice_java.options:
            choice_java.value = path_java_ui.value
        else :
            choice_java.options.append(
                ft.DropdownOption(
                    text=path_java_ui.value
                )
            )

            choice_java.value = path_java_ui.value

        path_java_ui.visible = False
        choice_java.visible = True
        edit_path.visible = True
        apply_path.visible = False

        page.update()


    # Инциализация конфига
    settings_ini = configparser.ConfigParser()
    settings_ini.read(get_settings_ini())

    # launcher
    width_ui = ft.TextField(
        value=settings_ini.get("launcher", "width"), 
        expand=False,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )
    height_ui = ft.TextField(
        value=settings_ini.get("launcher", "height"), 
        expand=False,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )
    ru_ui = settings_ini.get("launcher", "language")
    # mainecraft
    ram_ui = ft.TextField(
        value=settings_ini.get("minecraft", "ram"), 
        expand=True, 
        width=40,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )
    path_game_ui = ft.TextField(
        value=settings_ini.get("minecraft", "path_game"), 
        expand=True,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )
    jvm_ui = ft.TextField(
        value=get_jvm_args(), 
        expand=True,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )
    #   path_java
    path_java_ui = ft.TextField(
        value=settings_ini.get("minecraft", "path_java"),
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2"),
        visible=False,
        expand=True
    )
    choice_java = ft.Dropdown(
        on_change=chg_path,
        expand=True
    )
    update_java = ft.IconButton(
        icon=ft.Icons.REPLAY_ROUNDED,
        on_click=update_choice_java,
        icon_color="#E2E2E2"
    )

    edit_path = ft.IconButton(
        icon=ft.Icons.EDIT_ROUNDED,
        on_click=edit_path_func,
        icon_color="#E2E2E2"
    )

    apply_path = ft.IconButton(
        icon=ft.Icons.CHECK_ROUNDED,
        icon_color="#E2E2E2",
        visible=False,
        on_click=apply_path_func
    )

    folder = ft.FilePicker(
        on_result=folder_check
    )

    folder_java = ft.IconButton(
        icon=ft.Icons.FOLDER_ROUNDED,
        on_click=lambda e: folder.pick_files(allow_multiple=False),
        icon_color="#E2E2E2"
    )

    update_choice_java()

    # Other
    authlib_ui = ft.TextField(
        value=settings_ini.get("minecraft", "authlib"),
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2"),
        expand=True
    )

    def apply_settings(e):
        try :

            print(path_java_ui.value)
            settings_ini.set("launcher", "width", width_ui.value)
            settings_ini.set("launcher", "height", height_ui.value)
            settings_ini.set("launcher", "language", ru_ui)
            settings_ini.set("minecraft", "ram", ram_ui.value)
            settings_ini.set("minecraft", "path_game", path_game_ui.value)
            settings_ini.set("minecraft", "path_java", path_java_ui.value)
            ma.set_directory(dir=settings_ini.get("minecraft", "path_game"), is_none=True)

            set_jvm_args(jvm_ui.value)
            options["executablePath"] = path_java_ui.value

            with open(get_settings_ini(), 'w') as configfile:
                settings_ini.write(configfile)

            notification.notify(title="INLauncher", message="Настройки были успешно применены", app_name="INLauncher", app_icon="icon.ico")
        except Exception as e:
            notification.notify(title="INLauncher", message=f"Неудалось сохранить изменения, ошибка: {e}", app_name="INLauncher", app_icon="icon.ico")
            print(e)


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
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Path_java: "),
                            path_java_ui,
                            choice_java,
                            update_java,
                            edit_path,
                            apply_path,
                            folder_java
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(value="Authlib: "),
                            authlib_ui
                        ],
                    )
                ],
                wrap=True,
                width=500
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