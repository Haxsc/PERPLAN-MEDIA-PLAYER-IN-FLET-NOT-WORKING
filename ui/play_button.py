import flet as ft

def control_pause_button(e, video_player, play_button):
    video_player.control_pause()
    play_button.content = ft.Icon(
        name=ft.Icons.PAUSE if video_player.playing else ft.Icons.PLAY_ARROW,
        color="#505050"
    )
    play_button.update()
    
def create_play_button(video_player):
    play_button = ft.ElevatedButton(
        content=ft.Icon(name=ft.Icons.PLAY_ARROW, color="#505050"),
        bgcolor="white",
        autofocus=False,
        on_focus=False,
        style=ft.ButtonStyle(
            color="black",
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    play_button.on_click = lambda e: control_pause_button(e, video_player, play_button)
    return play_button