from github import Github
import flet as ft
import webbrowser
import os

class Social(ft.ElevatedButton):
    def __init__(self, src: str, url: str, size: int):
        super().__init__()

        self.content = ft.Image(src=src, width=size - 5, height=size - 5, expand=True)
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        self.width = size
        self.height = size
        self.on_click = lambda e: webbrowser.open(url)

def home_bar(page: ft.Page, osnv: ft.Container):
    
    content = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center
    )

    osnv.content = content
    page.update()

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