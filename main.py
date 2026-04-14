import flet as ft
from gui.menu import menu
import sys
from update import update

def main(page: ft.Page):
    update(page)

    page.title = "INLauncher"
    page.bgcolor = "#1E1E1E"
    page.adaptive = True
    page.theme_mode = ft.ThemeMode.DARK
    #rint(page.width, page.height)

    menu(page)

    page.update()
    

if __name__ == "__main__":
    ft.app(target=main)