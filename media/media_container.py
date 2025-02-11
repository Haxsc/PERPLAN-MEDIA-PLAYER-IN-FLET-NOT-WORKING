import flet as ft


def create_container_media(media, controls, page, playlist, video_path):
    return ft.Container(
        content=ft.Column(
            controls=[media, controls],
        ),
        width=page.width * 0.80 - 2,
        margin=2,
        alignment=ft.alignment.center,
    )
