import flet as ft

def create_seek_bar(video_player):
    return ft.Slider(
        min=0,
        max=1,
        value=0,
        expand=True,
        autofocus=False,
        interaction=ft.SliderInteraction.SLIDE_THUMB,
        thumb_color="white",
        on_change_start=lambda _: video_player.start_seek_interaction(),
        on_change_end=lambda _: video_player.end_seek_interaction(),
    )