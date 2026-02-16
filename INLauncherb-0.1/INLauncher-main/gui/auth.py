import flet as ft
import webbrowser
from gui.auth_api import AuthApiIntegration
from uuid import uuid4
import json
import os

user_profiles = os.path.join("configs", "usersProfile.json")
images = os.path.join("gui", "images")

def auth_ely(page: ft.Page):

    auths = AuthApiIntegration()

    def chg_based(e):
        login.disabled = False
        password.disabled = False
        page.update()

        if sign_in_based.value == "Microsoft":
            micro_text.visible = True
            login.visible = False
            password.visible = False
            nan_account.visible = False
            sign_in_butt.visible = False
            totp_token.visible = False
            sign_in_butt.visible = False


            login.value = ""
            password.value = ""
            totp_token.value = None

            page.update()
        elif sign_in_based.value == "Ely.by":
            micro_text.visible = False
            login.visible = True
            password.visible = True
            nan_account.visible = True
            sign_in_butt.visible = True
            totp_token.visible = True


            login.label = "login"
            password.password = True
            password.label = "password"

            login.value = ""
            password.value = ""
            totp_token.value = None


            page.update()
        else :
            micro_text.visible = False
            login.visible = True
            password.visible = False
            nan_account.visible = False
            sign_in_butt.visible = True
            totp_token.visible = False


            login.label = "username"
            password.password = False
            password.label = "UUID (Не обязательно)"

            login.value = ""
            password.value = ""
            totp_token.value = None


            page.update()

    def login_account(e):
        if sign_in_based.value == "Ely.by":
            loads_bar.visible = True
            page.update()

            result = auths.elyby_auth(login=login.value, password=password.value,totp_token=totp_token.value)
            print(result)
            if result == "error_data":
                error_text.value = "Неверный логин/пароль"
                error_text.visible = True
                page.update()
            elif result == "two_factor":
                error_text.value = "У вас двухфакторная система аунтификации, введите TOTP токен из Microsoft Authenticator"
                error_text.visible = True
                page.update()
            else :
                user = {
                    "uuid": result["selectedProfile"]["id"],
                    "token": result["accessToken"],
                    "username": result["selectedProfile"]["name"],
                    "type": "ely.by"
                }

                with open(user_profiles, "r", encoding="utf-8") as f:
                    users_js = json.load(f)

                    users_js["users"].append(user)
                
                with open(user_profiles, "w", encoding="utf-8") as n:
                    json.dump(users_js, n, ensure_ascii=False)

            page.update()
        else :
            uuids = str(uuid4())
            user = {
                "uuid": uuids,
                "token": "off",
                "username": login.value,
                "type": "offline"
            }

            with open(user_profiles, "r", encoding="utf-8") as f:
                users_js = json.load(f)

                users_js["users"].append(user)
                
            with open(user_profiles, "w", encoding="utf-8") as n:
                json.dump(users_js, n, ensure_ascii=False)

        from gui.rout_pages import rout_pages
        page.controls.clear()
        page.update()
        rout_pages(page, "menu")

    def back_butt(e):
        from gui.rout_pages import rout_pages
        page.controls.clear()
        page.update()
        rout_pages(page, "menu")

    sign_in_based = ft.Dropdown(
        options=[
            ft.DropdownOption(
                key="Microsoft",
                content=ft.Row(
                    controls=[
                        ft.Image(src=f"{os.path.join(images, "microsoft.png")}", width=20),
                        ft.Text(value="Microsoft")
                    ]
                )
            ),
            ft.DropdownOption(
                key="Ely.by",
                content=ft.Row(
                    controls=[
                        ft.Image(src=f"{os.path.join(images, "ely.png")}", width=20),
                        ft.Text(value="Ely.by")
                    ]
                )
            ),
            ft.DropdownOption(
                key="Offline",
                content=ft.Row(
                    controls=[
                        ft.Icon(name=ft.Icons.PERSON_ROUNDED, size=20),
                        ft.Text(value="Offline")
                    ]
                )
            )
        ],
        label="Вариант входа",
        width=300,
        on_change=chg_based
    )

    login = ft.TextField(
        label="login",
        width=300,
        disabled=True,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )

    password = ft.TextField(
        label="password",
        password=True,
        width=300,
        disabled=True,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )

    totp_token = ft.TextField(
        value=None,
        label="TOTP (если есть, вводить без пробелов)",
        width=300,
        visible=False,
        cursor_color="#E2E2E2",
        focused_border_color="#E2E2E2",
        selection_color="#E2E2E2",
        label_style=ft.TextStyle(color="#E2E2E2")
    )

    nan_account = ft.TextButton(
        text="У меня нет аккаунта/Забыл(а) пароль",
        on_click=lambda e: webbrowser.open("https://account.ely.by/register"),
        visible=False,
        style=ft.ButtonStyle(color="#E2E2E2")
    )
    
    micro_text = ft.Markdown(
        value="""Авторизация через microsoft не добавлена,  
                 cледите за новостями в телеграмм канале: [@inlauncher](https://www.t.me/inlauncher)""",
        scale=1,
        visible=False,
        on_tap_link=lambda e: webbrowser.open(e.data),
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        width=300
    )

    error_text = ft.Text(
        value="",
        visible=False,
        color=ft.Colors.RED,
        weight=ft.FontWeight.W_800,
        width=300

    )

    sign_in_butt = ft.ElevatedButton(
        content=ft.Text(value="Войти", scale=1, color="#E2E2E2"),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        width=300,
        height=50,
        on_click=login_account,
        visible=False,
        bgcolor="#1A1A1A"
    )

    loads_bar = ft.ProgressBar(
        visible=False,
        width=300
    )

    #page.vertical_alignment = ft.MainAxisAlignment.CENTER

    col = ft.Stack(
        controls=[
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                sign_in_based,
                                login,
                                password,
                                totp_token,
                                error_text,
                                nan_account,
                                sign_in_butt,
                                micro_text,
                                loads_bar
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=100
                ),
                alignment=ft.alignment.center,
                expand=True
            ),
            ft.Column(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED,
                        on_click=back_butt,
                        icon_color="#E2E2E2"
                    )
                ], 
                alignment=ft.MainAxisAlignment.START
            )
        ],
        expand=True
    )

    #page.add(ft.Column(controls=[ft.IconButton(icon=ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED)], alignment=ft.MainAxisAlignment.START))
    page.add(col)

if __name__ == "__main__":
    ft.app(auth_ely)
