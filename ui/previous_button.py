import flet as ft

def create_previous_button(video_player):
    return ft.ElevatedButton(
        content=ft.Icon(name=ft.Icons.SKIP_PREVIOUS),
        bgcolor="white",
        autofocus=False,
        on_focus=False,
        style=ft.ButtonStyle(
            color="#505050",
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=lambda _: video_player.previous_video()
    )