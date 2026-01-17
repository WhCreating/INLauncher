import flet as ft
from typing import Any
import json
import os

class Accounts_Card():
    def __init__(self, type_acc: str = "ely.by", nickname = "", col: ft.Column | None = None, page: ft.Page | None = None, osnv: ft.Container | None = None, user_profiles: os.PathLike = None):
        def delete_accs(e):
            with open(user_profiles, "r", encoding="utf-8") as jss:
                jss = json.load(jss)

                for i, acc in enumerate(jss["users"]):
                    if acc["username"] == nickname:
                        jss["users"].pop(i)
                        

        
            with open(user_profiles, "w", encoding="utf-8") as jssw:
                json.dump(jss, jssw, ensure_ascii=False)

            osnv.content = accounts_pg(page, user_profiles)
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

def accounts_pg(page: ft.Page, user_profiles: os.PathLike = None, osnv: ft.Container = None):
    
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
            accou.controls.append(Accounts_Card(acc_iter["type"], acc_iter["username"], accou, page, osnv, user_profiles).return_accs())

    return stack_bro