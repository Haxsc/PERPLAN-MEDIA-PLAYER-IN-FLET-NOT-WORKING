import flet as ft

def create_media_container(button_file_picker, image_widget, page):
    return ft.Container(
        content=ft.Row(
            controls=[
                button_file_picker,
                image_widget,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
        height=page.height * 0.85,
        width=page.width * 0.85,
    )
