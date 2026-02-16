import flet as ft
import os
import asyncio
import threading
import nbt
from gui.parse_server import Servers
from mine_api.craft_api import MllApi

class ServerCard(ft.Card):
    def __init__(self, ip: str, page: ft.Page):
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
            asyncio.run(self._server_init(ip, page))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        page.update()

    async def _server_init(self, ip: str, page: ft.Page):

        self.servers = Servers()
        self.status = await self.servers.get_status_server(ip=ip)
        self.margin = 5
        print(self.status)
        self.padding = ft.padding.only(left=5)
        self.height=70
        self.color="#1A1A1A"

        if self.status != "none":
            try:
                self.tooltip = self.status["name"]

                self.content = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Image(src_base64=f"{self.status["icon"].split("base64,")[-1]}", width=30),
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

                page.update()
            except Exception as e:
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
                print(e)
                page.update()
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

        page.update()

    def read_servers_mine(self, ma: MllApi):
        file = nbt.NBTFile(os.path.join(ma.get_directory(), "servers.dat"), "rb", compression='uncompressed')

        print(file.pretty_tree())




def monitoring(page: ft.Page, osnv: ft.Container):
    def add_servers(servers):
        for ip in servers:
            new_content.controls[1].controls.append(ServerCard(ip=ip, page=page))
            page.update()

    def on_search(e):
        servers = Servers().get_servers(search=search.value)
        new_content.controls[1].controls.clear()
        add_servers(servers)

    content = ft.Container(
        content=ft.ProgressRing(),
        alignment=ft.alignment.center,
    )

    osnv.content = content
    page.update()

    servers = Servers().get_servers()
    print(servers)

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