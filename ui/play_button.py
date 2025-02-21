import flet as ft


def create_play_button(video_player):
    play_button = ft.ElevatedButton(
        content=ft.Icon(name=ft.Icons.PLAY_ARROW),  # color="#505050"
        # bgcolor="white",
        autofocus=False,
        on_focus=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(
                radius=8
            ),  #            color="black",bgcolor="white",
        ),
    )
    play_button.on_click = lambda _: video_player.control_pause()

    return play_button
