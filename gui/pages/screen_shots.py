from mine_api.craft_api import MllApi
import flet as ft
import os

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

def screen_shots(page: ft.Page, ma: MllApi):
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