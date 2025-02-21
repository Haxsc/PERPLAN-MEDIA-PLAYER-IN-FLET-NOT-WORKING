import flet as ft


def create_skip_button(video_player):
    return ft.ElevatedButton(
        content=ft.Icon(name=ft.Icons.SKIP_NEXT),
        # bgcolor="white",
        autofocus=False,
        on_focus=False,
        style=ft.ButtonStyle(
            # color="#505050",
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=lambda _: video_player.skip_video(),
    )
