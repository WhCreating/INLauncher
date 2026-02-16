import flet as ft
from gui.auth import auth_ely
from gui.menu import menu

# page_name == "menu" or "auth_ely"
def rout_pages(page: ft.Page, page_name):
    if page_name == "menu":
        menu(page)
    else :
        auth_ely(page)













