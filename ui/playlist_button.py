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
        content=ft.Icon(name=ft.Icons.PLAYLIST_PLAY),
        width=35,
        height=35,
        margin=ft.margin.only(right=2),
        border_radius=8,
        bgcolor="#191c20",  # Cor padrão
        alignment=ft.alignment.center,
        on_click=lambda e: control_playlist_button(e, video_player, playlist_btn),
    )

    # Função para mudar a aparência ao passar o mouse
    def on_hover(e):
        if e.data == "true":
            playlist_btn.bgcolor = "#242a31"  # Cinza claro no hover
            playlist_btn.update()
        else:
            playlist_btn.bgcolor = "#191c20"  # Volta ao normal
            playlist_btn.update()

    playlist_btn.on_hover = on_hover  # Adiciona o evento de hover

    return playlist_btn
