import flet as ft
from ui.play_button import create_play_button
from ui.previous_button import create_previous_button
from ui.skip_button import create_skip_button
from ui.speed_button import speed_button

def create_controls(video_player, seek_bar):
    play_button = create_play_button(video_player)
    speed_btn = speed_button(video_player)
    skip_btn = create_skip_button(video_player)
    previous_btn = create_previous_button(video_player)
    
    left = ft.Row(
        controls=[
            play_button,
            previous_btn,
            skip_btn,
        ],
    )

    controls_main = ft.Column(
        controls=[
            seek_bar,
            ft.Row(
                controls=[
                    left,
                    speed_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
    )

    return {
        "play_button": play_button,
        "seek_bar": seek_bar,
        "controls": controls_main,
    }