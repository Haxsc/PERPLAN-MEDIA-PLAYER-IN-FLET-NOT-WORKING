import flet as ft


def control_playlist_button(e, video_player, playlist_btn):
    video_player.control_playlist()
    playlist_btn.border = ft.border.all(
        2 if video_player.proceed_playlist else 0,
        "green" if video_player.proceed_playlist else "#505050",
    )

    playlist_btn.update()


def create_playlist_button(video_player):
    playlist_btn = ft.Container(
        content=ft.Icon(name=ft.Icons.PLAYLIST_PLAY, color="#505050"),
        width=35,
        height=35,
        margin=ft.margin.only(right=2),
        border_radius=8,
        bgcolor="white",
        alignment=ft.alignment.center,
        on_click=lambda e: control_playlist_button(e, video_player, playlist_btn),
    )
    return playlist_btn
