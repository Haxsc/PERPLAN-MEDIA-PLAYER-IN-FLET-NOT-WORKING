import flet as ft


def create_seek_bar(video_player):
    return ft.Slider(
        min=0,
        value=0,
        interaction=ft.SliderInteraction.SLIDE_THUMB,
        thumb_color="white",
        on_change_start=lambda _: video_player.start_seek_interaction(),
        on_change_end=lambda _: video_player.end_seek_interaction(),
        adaptive=False,
        expand_loose=False,
        expand=False,
    )
